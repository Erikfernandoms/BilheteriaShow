def obter_total_reservado_repository(conn, id_usuario, id_evento):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(quantidade_ingressos), 0)
        FROM pedido
        WHERE id_usuario = ? AND id_evento = ? AND status IN ('reservado', 'pagamento aprovado')
    """, (id_usuario, id_evento))
    return cursor.fetchone()[0]

def obter_setor_evento_repository(conn, id_setor_evento):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quantidade_lugares, nome
        FROM setor_evento 
        WHERE id_setor_evento = ?
    """, (id_setor_evento,))
    return cursor.fetchone()

def atualizar_quantidade_lugares_repository(conn, id_setor_evento, quantidade):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE setor_evento 
        SET quantidade_lugares = quantidade_lugares - ?
        WHERE id_setor_evento = ?
    """, (quantidade, id_setor_evento))

def inserir_pedido_repository(conn, pedido):
    cursor = conn.cursor()
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
    return cursor.lastrowid

def listar_pedidos_repository(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido")
    return cursor.fetchall()

def listar_produtos_do_pedido_repository(conn, id_pedido):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_produto, p.nome, pp.quantidade, pp.preco, p.estoque_disponivel, p.ativo
        FROM produto_do_pedido pp
        JOIN produto p ON p.id_produto = pp.id_produto
        WHERE pp.id_pedido = ?
    """, (id_pedido,))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def atualizar_pedido_repository(conn, pedido_id, dados):
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
    return cursor.rowcount

def deletar_pedido_repository(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido WHERE id_pedido = ?", (pedido_id,))
    return cursor.rowcount

def listar_pedidos_usuario_repository(conn, usuario_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido WHERE id_usuario = ? and status != 'cancelado'", (usuario_id,))
    return cursor.fetchall()

def buscar_pedidos_reservados_expirados_repository(conn, agora):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_pedido, reservado_ate, id_setor_evento, quantidade_ingressos FROM pedido
        WHERE status = 'reservado'
    """)
    return cursor.fetchall()

def atualizar_status_pedido_expirado_repository(conn, id_pedido):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedido
        SET status = 'expirado', atualizado_em = CURRENT_TIMESTAMP
        WHERE id_pedido = ?
    """, (id_pedido,))

def devolver_lugares_setor_repository(conn, id_setor_evento, quantidade):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE setor_evento
        SET quantidade_lugares = quantidade_lugares + ?
        WHERE id_setor_evento = ?
    """, (quantidade, id_setor_evento))

def listar_produtos_do_pedido_para_expirado_repository(conn, id_pedido):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produto, quantidade FROM produto_do_pedido
        WHERE id_pedido = ?
    """, (id_pedido,))
    return cursor.fetchall()

def devolver_estoque_produto_repository(conn, id_produto, quantidade):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produto
        SET estoque_disponivel = estoque_disponivel + ?
        WHERE id_produto = ?
    """, (quantidade, id_produto))

def obter_cadeiras_pedido_repository(conn, id_pedido):
    cursor = conn.cursor()
    cursor.execute("SELECT cadeira FROM pedido WHERE id_pedido = ?", (id_pedido,))
    row = cursor.fetchone()
    return row[0] if row else None


def reservar_cadeiras_repository(conn, id_setor_evento, lista_id_cadeiras):
    cursor = conn.cursor()
    for id_cadeira in lista_id_cadeiras:
        cursor.execute("""
            UPDATE cadeira_do_setor
            SET reservada = 1
            WHERE id_cadeira = ? AND id_setor_evento = ? AND reservada = 0
        """, (id_cadeira, id_setor_evento))
        if cursor.rowcount == 0:
            raise Exception(f"Cadeira {id_cadeira} já está reservada ou não existe no setor {id_setor_evento}.")
    return True

def liberar_cadeiras_repository(conn, id_setor_evento, lista_id_cadeiras):
    cursor = conn.cursor()
    for id_cadeira in lista_id_cadeiras:
        cursor.execute("""
            UPDATE cadeira_do_setor
            SET reservada = 0
            WHERE id_cadeira = ? AND id_setor_evento = ? AND reservada = 1
        """, (id_cadeira, id_setor_evento))
    return True