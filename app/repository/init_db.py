import sqlite3




def init_db():
    conn = sqlite3.connect("bilhetagem.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evento (
        id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome  VARCHAR(100) NOT NULL,
        descricao TEXT NOT NULL,
        local VARCHAR(100) NOT NULL,
        data TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE setor_evento (
        id_setor_evento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade_lugares INTEGER,
        preco_base NUMERIC(10,2),
        id_evento INTEGER NOT NULL,
        FOREIGN KEY (id_evento) REFERENCES evento(id_evento)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        CPF VARCHAR(11) UNIQUE NOT NULL,
        senha VARCHAR(100) NOT NULL,
        telefone VARCHAR(15) NOT NULL,
        cep VARCHAR(10) NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE produto (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco NUMERIC(10,2),
        estoque_disponivel INTEGER,
        ativo BOOLEAN
    );
    """)

    cursor.execute("""
    CREATE TABLE pedido (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_evento INTEGER NOT NULL,
        id_setor_evento INTEGER NOT NULL,
        status TEXT,
        setor TEXT,
        cadeira TEXT,
        reservado_ate TIMESTAMP,
        valor_total NUMERIC(10,2),
        criado_em TIMESTAMP,
        atualizado_em TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_evento) REFERENCES evento(id_evento),
        FOREIGN KEY (id_setor_evento) REFERENCES setor_Evento(id_setor_evento)
    );
    """)
   
    cursor.execute("""
    CREATE TABLE pagamento (
        id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        status TEXT,
        metodo_pagamento TEXT,
        valor_total NUMERIC(10,2),
        data_criacao DATE,
        data_confirmacao DATE NOT NULL,
        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
    );
    """)
    cursor.execute("""
    CREATE TABLE produto_do_Pedido (
        id_pedido INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER,
        preco NUMERIC(10,2),
        PRIMARY KEY (id_pedido, id_produto),
        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
    );
    """)

    cursor.execute("""
    CREATE TABLE nota_fiscal (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        link_s3 TEXT,
        emitida_em TIMESTAMP,
        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
    );""")

    # Dados iniciais
    cursor.execute("DELETE FROM evento")
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Show do Coldplay", "O maior show das americas", "Morumbi", "2025-12-10"))
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Rock in Rio", "Venha sentir essa experiência!", "Rio de Janeiro", "2025-09-20"))

    conn.commit()
    conn.close()
    print("Banco de dados criado e populado com sucesso.")
