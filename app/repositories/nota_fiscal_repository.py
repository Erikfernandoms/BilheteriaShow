def buscar_pedido_repository(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido WHERE id_pedido = ?", (pedido_id,))
    row = cursor.fetchone()
    if not row:
        return None
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, row))

def buscar_usuario_repository(conn, id_usuario):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,))
    row = cursor.fetchone()
    if not row:
        return None
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, row))

def buscar_nome_evento_repository(conn, id_evento):
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM evento WHERE id_evento = ?", (id_evento,))
    row = cursor.fetchone()
    return row[0] if row else None

def buscar_produtos_do_pedido_repository(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nome, pp.quantidade, pp.preco
        FROM produto_do_pedido pp
        JOIN produto p ON p.id_produto = pp.id_produto
        WHERE pp.id_pedido = ?
    """, (pedido_id,))
    return [
        {"nome": row[0], "quantidade": row[1], "preco_unitario": row[2]}
        for row in cursor.fetchall()
    ]

def buscar_pagamento_aprovado_repository(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_pagamento FROM pagamento
        WHERE id_pedido = ? AND status = 'aprovado'
        ORDER BY data_confirmacao DESC LIMIT 1
    """, (pedido_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def inserir_nota_fiscal_repository(conn, id_pedido, id_pagamento, link_s3, valor_total, numero, emitida_em):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nota_fiscal (id_pedido, id_pagamento, link_s3, valor_total, numero, emitida_em)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_pedido, id_pagamento, link_s3, valor_total, numero, emitida_em))
    conn.commit()
    return {
        "id_nota": cursor.lastrowid,
        "id_pedido": id_pedido,
        "id_pagamento": id_pagamento,
        "link_s3": link_s3,
        "valor_total": valor_total,
        "numero": numero,
        "emitida_em": emitida_em
    }