from datetime import datetime
from logger import log_info, log_error
from metrics import incrementar_metrica

def criar_pedido(conn, pedido):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COALESCE(SUM(quantidade_ingressos), 0)
            FROM pedido
            WHERE id_usuario = ? AND id_evento = ? AND status IN ('reservado', 'pagamento aprovado')
        """, (pedido.id_usuario, pedido.id_evento))
        total_reservado = cursor.fetchone()[0]
        if total_reservado + pedido.quantidade_ingressos > 3:
            log_error(f"Usuário {pedido.id_usuario} tentou reservar mais de 3 ingressos para o evento {pedido.id_evento}.")
            return {"erro": "Você só pode reservar até 3 ingressos por evento, considerando todos os seus pedidos ativos."}

        conn.execute('BEGIN IMMEDIATE')

        cursor.execute("""
            SELECT quantidade_lugares, nome
            FROM setor_evento 
            WHERE id_setor_evento = ?
        """, (pedido.id_setor_evento,))
        row = cursor.fetchone()
        if not row or row[0] < pedido.quantidade_ingressos:
            conn.rollback()
            log_error(f"Ingressos insuficientes para o setor {pedido.id_setor_evento}. Disponíveis: {row[0] if row else 0}, Solicitados: {pedido.quantidade_ingressos}")
            return {"erro": "Ingressos insuficientes para o setor selecionado."}

        setor_nome = row[1].lower() if row else ""

        if setor_nome in ["cadeira inferior", "cadeira superior"]:
            if not pedido.cadeira:
                conn.rollback()
                log_error("Tentativa de reserva sem informar cadeiras.")
                return {"erro": "É necessário informar as cadeiras desejadas para este setor."}
            identificacoes = [cadeira.strip() for cadeira in pedido.cadeira.split(",") if cadeira.strip()]
            if len(identificacoes) != pedido.quantidade_ingressos:
                conn.rollback()
                log_error("Quantidade de cadeiras não bate com quantidade de ingressos.")
                return {"erro": "A quantidade de cadeiras deve ser igual à quantidade de ingressos."}
            ids_cadeiras = buscar_ids_cadeiras(cursor, identificacoes)
            if len(ids_cadeiras) != len(identificacoes):
                conn.rollback()
                log_error("Uma ou mais cadeiras não existem.")
                return {"erro": "Uma ou mais cadeiras não existem."}
            sucesso, erro = reservar_cadeiras(conn, pedido.id_setor_evento, ids_cadeiras)
            if not sucesso:
                conn.rollback()
                log_error(f"Falha ao reservar cadeiras: {erro}")
                return {"erro": erro}

        cursor.execute("""
            UPDATE setor_evento 
            SET quantidade_lugares = quantidade_lugares - ?
            WHERE id_setor_evento = ?
        """, (pedido.quantidade_ingressos, pedido.id_setor_evento))

        cursor.execute("""
            INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos, reservado_ate, valor_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pedido.id_usuario,
            pedido.id_evento,
            pedido.id_setor_evento,
            pedido.status,
            pedido.setor,
            pedido.cadeira,
            pedido.quantidade_ingressos,
            pedido.reservado_ate,
            pedido.valor_total
        ))

        conn.commit()
        log_info(f"Pedido criado com sucesso: {pedido.id_usuario}, Evento: {pedido.id_evento}, Setor: {pedido.id_setor_evento}, Quantidade: {pedido.quantidade_ingressos}")
        incrementar_metrica("pedidos_criados")
        return {
            "id_pedido": cursor.lastrowid,
            "id_usuario": pedido.id_usuario,
            "id_evento": pedido.id_evento,
            "id_setor_evento": pedido.id_setor_evento,
            "setor": pedido.setor,
            "cadeira": pedido.cadeira,
            "quantidade_ingressos": pedido.quantidade_ingressos,
            "valor_total": pedido.valor_total,
            "reservado_ate": pedido.reservado_ate,
            "status": pedido.status
        }
    except Exception as e:
        conn.rollback()
        log_error(f"Erro ao criar pedido: {str(e)}")
        return {"erro": f"Erro ao criar pedido: {str(e)}"}

def buscar_ids_cadeiras(cursor, identificacoes):
    cursor.execute(
        "SELECT id_cadeira FROM cadeira WHERE identificacao IN ({seq})".format(
            seq=','.join(['?']*len(identificacoes))
        ),
        tuple(identificacoes)
    )
    return [row[0] for row in cursor.fetchall()]

def listar_pedidos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()
    return [_pedido_dict(pedido) for pedido in pedidos]

def listar_produtos_do_pedido(conn, id_pedido: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_produto, p.nome, pp.quantidade, pp.preco, p.estoque_disponivel, p.ativo
        FROM produto_do_pedido pp
        JOIN produto p ON p.id_produto = pp.id_produto
        WHERE pp.id_pedido = ?
    """, (id_pedido,))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def atualizar_pedido(conn, pedido_id, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedido
        SET id_usuario = ?, id_evento = ?, id_setor_evento = ?, status = ?, setor = ?, cadeira = ?, reservado_ate = ?, valor_total = ?, atualizado_em = CURRENT_TIMESTAMP
        WHERE id_pedido = ?
    """, (dados.id_usuario,
        dados.id_evento,
        dados.id_setor_evento,
        dados.status,
        dados.setor,
        dados.cadeira,
        dados.reservado_ate,
        dados.valor_total,
        pedido_id
    ))
    conn.commit()
    if cursor.rowcount == 0:
        log_error(f"Tentativa de atualizar pedido inexistente: {pedido_id}")
        return None
    log_info(f"Pedido {pedido_id} atualizado.")
    return _pedido_dict((pedido_id, dados.id_usuario, dados.id_evento, dados.id_setor_evento, dados.status, dados.setor, dados.cadeira, dados.quantidade_ingressos, dados.reservado_ate, dados.valor_total, None, None))

def deletar_pedido(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido WHERE id_pedido = ?", (pedido_id,))
    conn.commit()
    if cursor.rowcount > 0:
        log_info(f"Pedido {pedido_id} deletado.")
        return True
    else:
        log_error(f"Tentativa de deletar pedido inexistente: {pedido_id}")
        return False

def listar_pedidos_usuario(conn, usuario_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido WHERE id_usuario = ? and status != 'cancelado'", (usuario_id,))
    pedidos = cursor.fetchall()
    return [_pedido_dict(pedido) for pedido in pedidos] if pedidos else []

def cancelar_reservas_expiradas(conn):
    cursor = conn.cursor()
    agora = datetime.now()
    cursor.execute("""
        SELECT id_pedido, reservado_ate, id_setor_evento, quantidade_ingressos FROM pedido
        WHERE status = 'reservado'
    """)
    pedidos = cursor.fetchall()
    expirados = [
        (pedido[0], pedido[2], pedido[3])  # id_pedido, id_setor_evento, quantidade_ingressos
        for pedido in pedidos
        if datetime.strptime(pedido[1], "%Y-%m-%d %H:%M:%S") < agora
    ]
    for id_pedido, id_setor_evento, quantidade_ingressos in expirados:
        cursor.execute("""
            UPDATE pedido
            SET status = 'expirado', atualizado_em = CURRENT_TIMESTAMP
            WHERE id_pedido = ?
        """, (id_pedido,))
        cursor.execute("""
            UPDATE setor_evento
            SET quantidade_lugares = quantidade_lugares + ?
            WHERE id_setor_evento = ?
        """, (quantidade_ingressos, id_setor_evento))
        cursor.execute("""
            SELECT id_produto, quantidade FROM produto_do_pedido
            WHERE id_pedido = ?
        """, (id_pedido,))
        produtos = cursor.fetchall()
        for id_produto, quantidade in produtos:
            cursor.execute("""
                UPDATE produto
                SET estoque_disponivel = estoque_disponivel + ?
                WHERE id_produto = ?
            """, (quantidade, id_produto))
        cursor.execute("SELECT cadeira FROM pedido WHERE id_pedido = ?", (id_pedido,))
        cadeiras_pedido = cursor.fetchone()[0]
        if cadeiras_pedido:
            identificacoes = [c.strip() for c in cadeiras_pedido.split(",") if c.strip()]
            ids_cadeiras = buscar_ids_cadeiras(cursor, identificacoes)
            liberar_cadeiras(conn, id_setor_evento, ids_cadeiras)
        incrementar_metrica("pedidos_expirados")
        log_info(f"Pedido expirado: {id_pedido}, setor: {id_setor_evento}, cadeiras liberadas: {cadeiras_pedido}")
    if expirados:
        log_info(f"Pedidos expirados: {', '.join(str(p[0]) for p in expirados)}")
        log_info(f"Setores atualizados: {', '.join(str(p[1]) for p in expirados)}")
    conn.commit()

def reservar_cadeiras(conn, id_setor_evento, lista_id_cadeiras):
    cursor = conn.cursor()
    for id_cadeira in lista_id_cadeiras:
        cursor.execute("""
            SELECT reservada FROM cadeira_do_setor
            WHERE id_cadeira = ? AND id_setor_evento = ?
        """, (id_cadeira, id_setor_evento))
        row = cursor.fetchone()
        if not row or row[0] == 1:
            log_error(f"Cadeira {id_cadeira} já está reservada ou não existe neste setor.")
            return False, f"Cadeira {id_cadeira} já está reservada ou não existe neste setor."
    for id_cadeira in lista_id_cadeiras:
        cursor.execute("""
            UPDATE cadeira_do_setor SET reservada = 1
            WHERE id_cadeira = ? AND id_setor_evento = ?
        """, (id_cadeira, id_setor_evento))
        log_info(f"Cadeira {id_cadeira} reservada no setor {id_setor_evento}.")
    return True, None

def liberar_cadeiras(conn, id_setor_evento, lista_id_cadeiras):
    cursor = conn.cursor()
    for id_cadeira in lista_id_cadeiras:
        cursor.execute("""
            UPDATE cadeira_do_setor SET reservada = 0
            WHERE id_cadeira = ? AND id_setor_evento = ?
        """, (id_cadeira, id_setor_evento))
        log_info(f"Cadeira {id_cadeira} liberada no setor {id_setor_evento}.")

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
        "criado_em": pedido_tuple[10] if len(pedido_tuple) > 10 else None,
        "atualizado_em": pedido_tuple[11] if len(pedido_tuple) > 11 else None
    }