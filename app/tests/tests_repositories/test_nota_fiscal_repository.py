


from datetime import datetime
from app.repositories.nota_fiscal_repository import buscar_nome_evento_repository, buscar_pagamento_aprovado_repository, buscar_pedido_repository, buscar_produtos_do_pedido_repository, buscar_usuario_repository, inserir_nota_fiscal_repository


def test_buscar_pedido_repository(conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO usuario (nome, email, CPF, senha, telefone, cep) VALUES ('Usuário', 'u@email.com', '00000000000', 'senha123', '11999999999', '01234-000')""")
    id_usuario = cursor.lastrowid
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES ('Evento', 'Show', 'SP', '2025-10-01')")
    id_evento = cursor.lastrowid
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES ('VIP', 100, 200.0, ?)", (id_evento,))
    id_setor = cursor.lastrowid
    cursor.execute("""
        INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos, valor_total)
        VALUES (?, ?, ?, 'pago', 'VIP', 'A1', 2, 300)
    """, (id_usuario, id_evento, id_setor))
    pedido_id = cursor.lastrowid

    result = buscar_pedido_repository(conn, pedido_id)
    assert result["id_usuario"] == id_usuario
    assert result["setor"] == "VIP"
    assert buscar_pedido_repository(conn, 999) is None


def test_buscar_usuario_repository(conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO usuario (nome, email, CPF, senha, telefone, cep) VALUES ('João', 'u@email.com', '00000000000', 'senha123', '11999999999', '01234-000')""")
    id_usuario = cursor.lastrowid

    result = buscar_usuario_repository(conn, id_usuario)
    assert result["nome"] == "João"
    assert buscar_usuario_repository(conn, 999) is None


def test_buscar_nome_evento_repository(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO evento (nome, descricao, local, data)
        VALUES ('Lollapalooza', 'Festival', 'SP', '2025-09-01')
    """)
    id_evento = cursor.lastrowid

    result = buscar_nome_evento_repository(conn, id_evento)
    assert result == "Lollapalooza"
    assert buscar_nome_evento_repository(conn, 999) is None



def test_buscar_produtos_do_pedido_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produto (nome) VALUES ('Camiseta')")
    id_produto = cursor.lastrowid
    cursor.execute("""INSERT INTO usuario (nome, email, CPF, senha, telefone, cep) VALUES ('Usuário', 'u@email.com', '00000000000', 'senha123', '11999999999', '01234-000')""")
    id_usuario = cursor.lastrowid
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES ('Evento', 'Desc', 'Local', '2025-09-10')")
    id_evento = cursor.lastrowid
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES ('Pista', 100, 120, ?)", (id_evento,))
    id_setor = cursor.lastrowid
    cursor.execute("INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, valor_total) VALUES (?, ?, ?, 200)", (id_usuario, id_evento, id_setor))
    id_pedido = cursor.lastrowid
    cursor.execute("INSERT INTO produto_do_pedido (id_pedido, id_produto, quantidade, preco) VALUES (?, ?, ?, ?)",
                   (id_pedido, id_produto, 2, 50.0))
    conn.commit()

    produtos = buscar_produtos_do_pedido_repository(conn, id_pedido)
    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Camiseta"
    assert produtos[0]["quantidade"] == 2
    assert produtos[0]["preco_unitario"] == 50.0


def test_buscar_pagamento_aprovado_repository(conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO usuario (nome, email, CPF, senha, telefone, cep) VALUES ('Usuário', 'u@email.com', '00000000000', 'senha123', '11999999999', '01234-000')""")
    id_usuario = cursor.lastrowid
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES ('Evento', 'Desc', 'Local', '2025-10-02')")
    id_evento = cursor.lastrowid
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES ('Superior', 60, 180, ?)", (id_evento,))
    id_setor = cursor.lastrowid
    cursor.execute("INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, valor_total) VALUES (?, ?, ?, 250)", (id_usuario, id_evento, id_setor))
    id_pedido = cursor.lastrowid
    cursor.execute("INSERT INTO pagamento (id_pedido, status, data_confirmacao) VALUES (?, 'aprovado', ?)",
                   (id_pedido, datetime.now().isoformat()))
    id_pagamento = cursor.lastrowid

    nota = inserir_nota_fiscal_repository(
        conn,
        id_pedido=id_pedido,
        id_pagamento=id_pagamento,
        link_s3="nota_001.json",
        valor_total=250.0,
        numero="NFS-001",
        emitida_em="2025-06-16T12:00:00"
    )

    assert nota["id_pedido"] == id_pedido
    assert nota["numero"] == "NFS-001"