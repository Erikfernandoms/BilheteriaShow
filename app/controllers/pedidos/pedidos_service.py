def criar_pedido(conn, pedido):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos,reservado_ate, valor_total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (pedido.id_usuario,
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
        "status": 'solicitado'
    }

def listar_pedidos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()
    return [
        {
            "id_pedido": pedido[0],
            "id_usuario": pedido[1],
            "id_evento": pedido[2],
            "id_setor_evento": pedido[3],
            "status": pedido[4],
            "setor": pedido[5],
            "cadeira": pedido[6],
            "reservado_ate": pedido[7],
            "valor_total": pedido[8],
            "criado_em": pedido[9],
            "atualizado_em": pedido[10]
        } for pedido in pedidos
    ]

def atualizar_pedido(conn, pedido_id, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedido
        SET id_usuario = ?, id_evento = ?, id_setor_evento = ?, status = ?, setor = ?, cadeira = ?, reservado_ate = ?, valor_total = ?
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
        return None

    return {
        "id_pedido": pedido_id,
        "id_usuario": dados.id_usuario,
        "id_evento": dados.id_evento,
        "id_setor_evento": dados.id_setor_evento,
        "status": dados.status,
        "setor": dados.setor,
        "cadeira": dados.cadeira,
        "reservado_ate": dados.reservado_ate,
        "valor_total": dados.valor_total
    }

def deletar_pedido(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido WHERE id_pedido = ?", (pedido_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False

    return True