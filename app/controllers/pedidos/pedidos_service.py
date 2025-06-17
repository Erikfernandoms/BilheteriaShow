from datetime import datetime, timedelta
from logger import log_info, log_error
from metrics import incrementar_metrica
from app.repositories.pedidos_repository import (
    buscar_pedidos_pagamentos_recusados_repository,
    liberar_cadeiras_repository,
    obter_total_reservado_repository,
    obter_setor_evento_repository,
    atualizar_quantidade_lugares_repository,
    inserir_pedido_repository,
    listar_pedidos_repository,
    listar_produtos_do_pedido_repository,
    atualizar_pedido_repository,
    deletar_pedido_repository,
    listar_pedidos_usuario_repository,
    buscar_pedidos_reservados_expirados_repository,
    atualizar_status_pedido_expirado_repository,
    devolver_lugares_setor_repository,
    listar_produtos_do_pedido_para_expirado_repository,
    devolver_estoque_produto_repository,
    reservar_cadeiras_repository
)

def criar_pedido(conn, pedido):
    try:
        total_reservado = obter_total_reservado_repository(conn, pedido.id_usuario, pedido.id_evento)
        if total_reservado + pedido.quantidade_ingressos > 3:
            return {"erro": "Você só pode reservar até 3 ingressos por evento, considerando todos os seus pedidos ativos."}

        conn.execute('BEGIN IMMEDIATE')

        # Verificação de cadeiras duplicadas
        if pedido.cadeira:
            identificacoes = [c.strip() for c in pedido.cadeira.split(",")]
            cadeiras_ocupadas = []
            for identificacao in identificacoes:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 1 FROM pedido
                    WHERE status IN ('reservado', 'pagamento aprovado')
                    AND id_setor_evento = ?
                    AND instr(',' || cadeira || ',', ',' || ? || ',') > 0
                """, (pedido.id_setor_evento, identificacao))
                if cursor.fetchone():
                    cadeiras_ocupadas.append(identificacao)
            if cadeiras_ocupadas:
                conn.rollback()
                return {"erro": f"As cadeiras {', '.join(cadeiras_ocupadas)} já estão reservadas em outro pedido."}

        setor_evento_infos = obter_setor_evento_repository(conn, pedido.id_setor_evento)
        if not setor_evento_infos or setor_evento_infos[0] < pedido.quantidade_ingressos:
            conn.rollback()
            return {"erro": "Ingressos insuficientes para o setor selecionado."}

        atualizar_quantidade_lugares_repository(conn, pedido.id_setor_evento, pedido.quantidade_ingressos)

        pedido_id = inserir_pedido_repository(conn, pedido)

        conn.commit()
        incrementar_metrica("pedidos_criados")
        log_info(f"Pedido {pedido_id} criado para usuário {pedido.id_usuario}.")
        return {
            "id_pedido": pedido_id,
            "id_usuario": pedido.id_usuario,
            "id_evento": pedido.id_evento,
            "id_setor_evento": pedido.id_setor_evento,
            "status": pedido.status,
            "setor": pedido.setor,
            "cadeira": pedido.cadeira,
            "quantidade_ingressos": pedido.quantidade_ingressos,
            "reservado_ate": pedido.reservado_ate,
            "valor_total": pedido.valor_total
        }
    except Exception as e:
        conn.rollback()
        log_error(f"Erro ao criar pedido: {e}")
        raise e

def buscar_ids_cadeiras(cursor, identificacoes):
    cursor.execute(
        "SELECT id_cadeira FROM cadeira WHERE identificacao IN ({seq})".format(
            seq=','.join(['?']*len(identificacoes))
        ),
        tuple(identificacoes)
    )
    return [row[0] for row in cursor.fetchall()]

def listar_pedidos(conn):
    pedidos = listar_pedidos_repository(conn)
    return [_pedido_dict(pedido) for pedido in pedidos]

def listar_produtos_do_pedido(conn, id_pedido: int):
    return listar_produtos_do_pedido_repository(conn, id_pedido)

def atualizar_pedido(conn, pedido_id, dados):
    rowcount = atualizar_pedido_repository(conn, pedido_id, dados)
    if rowcount == 0:
        log_error(f"Pedido {pedido_id} não encontrado para atualização.")
        return None
    log_info(f"Pedido {pedido_id} atualizado.")
    return _pedido_dict((pedido_id, dados.id_usuario, dados.id_evento, dados.id_setor_evento, dados.status, dados.setor, dados.cadeira, dados.quantidade_ingressos, dados.reservado_ate, dados.valor_total, None, None))

def deletar_pedido(conn, pedido_id):
    rowcount = deletar_pedido_repository(conn, pedido_id)
    if rowcount > 0:
        log_info(f"Pedido {pedido_id} deletado.")
        return True
    else:
        log_error(f"Pedido {pedido_id} não encontrado para deleção.")
        return False

def listar_pedidos_usuario(conn, usuario_id):
    pedidos = listar_pedidos_usuario_repository(conn, usuario_id)
    return [_pedido_dict(pedido) for pedido in pedidos]

def cancelar_reservas_expiradas(conn):
    agora = datetime.now()
    pedidos = buscar_pedidos_reservados_expirados_repository(conn, agora)
    for pedido in pedidos:
        id_pedido, reservado_ate, id_setor_evento, quantidade_ingressos = pedido
        if reservado_ate and datetime.strptime(reservado_ate, "%Y-%m-%d %H:%M:%S") < agora:
            atualizar_status_pedido_expirado_repository(conn, id_pedido)
            devolver_lugares_setor_repository(conn, id_setor_evento, quantidade_ingressos)
            produtos = listar_produtos_do_pedido_para_expirado_repository(conn, id_pedido)
            for id_produto, quantidade in produtos:
                devolver_estoque_produto_repository(conn, id_produto, quantidade)
            log_info(f"Reserva expirada e cancelada para pedido {id_pedido}.")
            log_info(f"Produtos adicionais devolvidos ao estoque para o pedido {id_pedido}.")

def cancelar_pedidos_pagamento_recusado(conn, id_pedido):
    try:
        conn.execute("BEGIN IMMEDIATE")

        pedido = buscar_pedidos_pagamentos_recusados_repository(conn, id_pedido)
        if not pedido:
            return None
        
        id_pedido = pedido[0]
        id_usuario = pedido[1]
        id_evento = pedido[2]
        id_setor_evento = pedido[3]
        status = "cancelado"
        setor = pedido[5]
        cadeiras = pedido[6]
        quantidade_ingressos = pedido[7]
        reservado_ate = pedido[8]
        valor_total = pedido[9]

        # Devolve os lugares
        devolver_lugares_setor_repository(conn, id_setor_evento, quantidade_ingressos)
        log_info(f"Ingressos devolvidos para o setor {id_setor_evento} do pedido {id_pedido}.")

        # Devolve os produtos
        produtos = listar_produtos_do_pedido_para_expirado_repository(conn, id_pedido)
        for id_produto, quantidade in produtos:
            devolver_estoque_produto_repository(conn, id_produto, quantidade)
        log_info(f"Produtos adicionais devolvidos ao estoque para o pedido {id_pedido}.")

        # Libera cadeiras, se houver
        if cadeiras:
            identificacoes = [c.strip() for c in cadeiras.split(",")]
            cursor = conn.cursor()
            ids_cadeiras = buscar_ids_cadeiras(cursor, identificacoes)
            liberar_cadeiras_repository(conn, id_setor_evento, ids_cadeiras)
            log_info(f"Cadeiras {identificacoes} liberadas para o pedido {id_pedido}.")

        # Atualiza status do pedido
        atualizar_pedido_repository(conn, id_pedido, type("Pedido", (), {
            "id_usuario": id_usuario,
            "id_evento": id_evento,
            "id_setor_evento": id_setor_evento,
            "status": status,
            "setor": setor,
            "cadeira": cadeiras,
            "quantidade_ingressos": quantidade_ingressos,
            "reservado_ate": reservado_ate,
            "valor_total": valor_total
        })())

        conn.commit()

        return {
            "id_pedido": id_pedido,
            "id_usuario": id_usuario,
            "id_evento": id_evento,
            "id_setor_evento": id_setor_evento,
            "status": status,
            "setor": setor,
            "cadeira": cadeiras,
            "quantidade_ingressos": quantidade_ingressos,
            "reservado_ate": reservado_ate,
            "valor_total": valor_total,
            "criado_em": None  # ajuste se quiser retornar a data real
        }

    except Exception as e:
        conn.rollback()
        log_error(f"Erro ao cancelar pedido {id_pedido} por pagamento recusado: {e}")
        raise e

def reservar_cadeiras(conn, id_setor_evento, lista_id_cadeiras):
    try:
        conn.execute('BEGIN IMMEDIATE')
        resultado = reservar_cadeiras_repository(conn, id_setor_evento, lista_id_cadeiras)
        conn.commit()
        log_info(f"Cadeiras {lista_id_cadeiras} reservadas no setor {id_setor_evento}.")
        return resultado
    except Exception as e:
        conn.rollback()
        log_error(f"Erro ao reservar cadeiras: {e}")
        raise e

def liberar_cadeiras(conn, id_setor_evento, lista_id_cadeiras):
    try:
        conn.execute('BEGIN IMMEDIATE')
        resultado = liberar_cadeiras_repository(conn, id_setor_evento, lista_id_cadeiras)
        conn.commit()
        log_info(f"Cadeiras {lista_id_cadeiras} liberadas no setor {id_setor_evento}.")
        return resultado
    except Exception as e:
        conn.rollback()
        log_error(f"Erro ao liberar cadeiras: {e}")
        raise e

def _pedido_dict(pedido_tuple):
    return {
        "id_pedido": pedido_tuple[0],
        "id_usuario": pedido_tuple[1],
        "id_evento": pedido_tuple[2],
        "id_setor_evento": pedido_tuple[3],
        "status": pedido_tuple[4],
        "setor": pedido_tuple[5],
        "cadeira": pedido_tuple[6],
        "quantidade_ingressos": pedido_tuple[7],
        "reservado_ate": pedido_tuple[8],
        "valor_total": pedido_tuple[9],
        "criado_em": pedido_tuple[10],
    }