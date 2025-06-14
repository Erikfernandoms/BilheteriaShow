def listar_produtos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produto")
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def listar_produtos_do_evento(conn, id_evento):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM produto p
        JOIN produto_do_evento pe ON p.id_produto = pe.id_produto
        WHERE pe.id_evento = ? AND p.ativo = 1
    """, (id_evento,))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def associar_produto_ao_evento(conn, id_evento: int, id_produto: int):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO produto_do_evento (id_evento, id_produto)
        VALUES (?, ?)
    """, (id_evento, id_produto))
    conn.commit()
    return {"id_evento": id_evento, "id_produto": id_produto}

def obter_produto(conn, produto_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produto WHERE id_produto = ?", (produto_id,))
    row = cursor.fetchone()
    if row:
        colunas = [desc[0] for desc in cursor.description]
        return dict(zip(colunas, row))
    return None

def criar_produto(conn, produto):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produto (nome, preco, estoque_disponivel, ativo)
        VALUES (?, ?, ?, ?)
    """, (produto.nome, produto.preco, produto.estoque_disponivel, produto.ativo))
    conn.commit()
    return obter_produto(conn, cursor.lastrowid)

def atualizar_produto(conn, produto_id: int, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produto SET nome=?, preco=?, estoque_disponivel=?, ativo=?
        WHERE id_produto=?
    """, (dados.nome, dados.preco, dados.estoque_disponivel, dados.ativo, produto_id))
    conn.commit()
    return obter_produto(conn, produto_id)

def deletar_produto(conn, produto_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produto WHERE id_produto=?", (produto_id,))
    conn.commit()


def adicionar_produto_pedido(conn, pedido_id: int, id_produto: int, quantidade: int):
    cursor = conn.cursor()
    cursor.execute("SELECT estoque_disponivel, preco FROM produto WHERE id_produto = ?", (id_produto,))
    row = cursor.fetchone()
    if not row or row[0] < quantidade:
        return None
    preco_produto = row[1]

    cursor.execute("""
        INSERT INTO produto_do_pedido (id_pedido, id_produto, quantidade, preco)
        VALUES (?, ?, ?, ?)
    """, (pedido_id, id_produto, quantidade, preco_produto))

    cursor.execute("""
        UPDATE produto SET estoque_disponivel = estoque_disponivel - ?
        WHERE id_produto = ?
    """, (quantidade, id_produto))

    # Atualiza o valor_total do pedido
    valor_adicional = preco_produto * quantidade
    cursor.execute("""
        UPDATE pedido SET valor_total = valor_total + ?,
                   SET atualizado_em = CURRENT_TIMESTAMP
        WHERE id_pedido = ?
    """, (valor_adicional, pedido_id))

    conn.commit()
    return {
        "id_pedido_produto": cursor.lastrowid,
        "id_pedido": pedido_id,
        "id_produto": id_produto,
        "quantidade": quantidade
    }