import sqlite3




def init_db():
    conn = sqlite3.connect("bilhetagem.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cadeira (
        id_cadeira INTEGER PRIMARY KEY AUTOINCREMENT,
        identificacao TEXT NOT NULL UNIQUE
    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS cadeira_do_setor (
        id_cadeira INTEGER NOT NULL,
        id_setor_evento INTEGER NOT NULL,
        reservada INTEGER DEFAULT 0,
        PRIMARY KEY (id_cadeira, id_setor_evento),
        FOREIGN KEY (id_cadeira) REFERENCES cadeira(id_cadeira),
        FOREIGN KEY (id_setor_evento) REFERENCES setor_evento(id_setor_evento)
    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS produto_do_evento (
    id_evento INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    PRIMARY KEY (id_evento, id_produto),
    FOREIGN KEY (id_evento) REFERENCES evento(id_evento),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evento (
        id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome  VARCHAR(100) NOT NULL UNIQUE,
        descricao TEXT NOT NULL,
        local VARCHAR(100) NOT NULL,
        data TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS setor_evento (
        id_setor_evento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade_lugares INTEGER,
        preco_base NUMERIC(10,2),
        id_evento INTEGER NOT NULL,
        FOREIGN KEY (id_evento) REFERENCES evento(id_evento),
        UNIQUE (nome, id_evento)  on conflict ignore               
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
    CREATE TABLE IF NOT EXISTS produto (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        preco NUMERIC(10,2),
        estoque_disponivel INTEGER,
        ativo BOOLEAN
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedido (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_evento INTEGER NOT NULL,
        id_setor_evento INTEGER NOT NULL,
        status TEXT,
        setor TEXT,
        cadeira TEXT,
        quantidade_ingressos INTEGER,
        reservado_ate TIMESTAMP,
        valor_total NUMERIC(10,2),
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_evento) REFERENCES evento(id_evento),
        FOREIGN KEY (id_setor_evento) REFERENCES setor_Evento(id_setor_evento)
    );
    """)
   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagamento (
        id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        status TEXT,
        metodo_pagamento TEXT,
        valor_total NUMERIC(10,2),
        data_criacao DATE DEFAULT CURRENT_TIMESTAMP,
        data_confirmacao DATE,
        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
    );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto_do_pedido (
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
    CREATE TABLE IF NOT EXISTS nota_fiscal (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        id_pagamento INTEGER NOT NULL,
        link_s3 TEXT,
        valor_total NUMERIC(10,2),
        numero TEXT UNIQUE,
        emitida_em TIMESTAMP,
        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
    );""")

    """Definindo eventos e setores iniciais"""
    cursor.execute("INSERT OR IGNORE INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Show do Coldplay", "O maior show das americas", "Morumbi", "2025-12-10"))
    cursor.execute("INSERT OR IGNORE INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Rock in Rio", "Venha sentir essa experiência!", "Rio de Janeiro", "2025-09-20"))
    cursor.execute("INSERT OR IGNORE INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Pericles", "Aaaah se eu largar o freio!", "São Paulo - Allianz Parque", "2025-09-10"))

    cursor.execute("""INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Pista", "1000", "125.00", (SELECT id_evento FROM Evento WHERE nome = "Show do Coldplay"))""")
    cursor.execute("""INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Camarote", "200", "255.00", (SELECT id_evento FROM Evento WHERE nome = "Show do Coldplay"))""")
    cursor.execute("""INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Cadeira Superior", "500", "75.00", (SELECT id_evento FROM Evento WHERE nome = "Show do Coldplay"))""")

    cursor.execute("""INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Pista", "2000", "180.00", (SELECT id_evento FROM Evento WHERE nome = "Rock in Rio"))""")
    cursor.execute(""" INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Camarote", "500", "350.00", (SELECT id_evento FROM Evento WHERE nome = "Rock in Rio"))""")

    cursor.execute("""INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Cadeira Inferior", "250", "80.00", (SELECT id_evento FROM Evento WHERE nome = "Pericles"))""")
    cursor.execute("""INSERT OR IGNORE INTO Setor_Evento (nome, quantidade_lugares, preco_base, id_evento)
    VALUES ("Cadeira Superior", "500", "120.00", (SELECT id_evento FROM Evento WHERE nome = "Pericles"))""")

    """Definindo produtos iniciais"""
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Combo Pipoca + Refrigerante', 35.00, 200, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Camiseta Oficial', 80.00, 100, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Copo Personalizado', 25.00, 300, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Boné do Evento', 40.00, 80, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Combo Cerveja + Batata', 45.00, 150, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Chaveiro Exclusivo', 15.00, 250, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Pulseira Neon', 10.00, 500, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Combo Água + Sanduíche', 30.00, 180, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Água', 10.00, 100, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Ice', 15.00, 100, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Combo Vodka + Energetico', 40.00, 50, 1)""")
    cursor.execute("""INSERT OR IGNORE INTO produto (nome, preco, estoque_disponivel, ativo) VALUES ('Refrigerante', 8.00, 200, 1)""")


    """Associando produtos aos eventos"""
    cursor.execute("""
        INSERT OR IGNORE INTO produto_do_evento (id_evento, id_produto)
        VALUES 
            ((SELECT id_evento FROM evento WHERE nome = "Show do Coldplay"), (SELECT id_produto FROM produto WHERE nome = "Camiseta Oficial")),
            ((SELECT id_evento FROM evento WHERE nome = "Show do Coldplay"), (SELECT id_produto FROM produto WHERE nome = "Copo Personalizado")),
            ((SELECT id_evento FROM evento WHERE nome = "Show do Coldplay"), (SELECT id_produto FROM produto WHERE nome = "Combo Pipoca + Refrigerante")),
            ((SELECT id_evento FROM evento WHERE nome = "Show do Coldplay"), (SELECT id_produto FROM produto WHERE nome = "Pulseira Neon"))
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO produto_do_evento (id_evento, id_produto)
        VALUES 
            ((SELECT id_evento FROM evento WHERE nome = "Rock in Rio"), (SELECT id_produto FROM produto WHERE nome = "Boné do Evento")),
            ((SELECT id_evento FROM evento WHERE nome = "Rock in Rio"), (SELECT id_produto FROM produto WHERE nome = "Combo Cerveja + Batata")),
            ((SELECT id_evento FROM evento WHERE nome = "Rock in Rio"), (SELECT id_produto FROM produto WHERE nome = "Chaveiro Exclusivo")),
            ((SELECT id_evento FROM evento WHERE nome = "Rock in Rio"), (SELECT id_produto FROM produto WHERE nome = "Ice"))
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO produto_do_evento (id_evento, id_produto)
        VALUES 
            ((SELECT id_evento FROM evento WHERE nome = "Pericles"), (SELECT id_produto FROM produto WHERE nome = "Combo Água + Sanduíche")),
            ((SELECT id_evento FROM evento WHERE nome = "Pericles"), (SELECT id_produto FROM produto WHERE nome = "Refrigerante")),
            ((SELECT id_evento FROM evento WHERE nome = "Pericles"), (SELECT id_produto FROM produto WHERE nome = "Água")),
            ((SELECT id_evento FROM evento WHERE nome = "Pericles"), (SELECT id_produto FROM produto WHERE nome = "Pulseira Neon"))
    """)

    """Definindo as cadeiras iniciais"""
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("A1")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("A2")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("A3")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("A4")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("A5")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("B1")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("B2")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("B3")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("B4")')
    cursor.execute('INSERT OR IGNORE INTO cadeira (identificacao) VALUES ("B5")')

    """Associando cadeiras aos setores"""
    cursor.execute("""
        INSERT OR IGNORE INTO cadeira_do_setor (id_cadeira, id_setor_evento)
        SELECT c.id_cadeira, se.id_setor_evento
        FROM cadeira c, setor_evento se
        WHERE se.nome IN ('Cadeira Superior', 'Cadeira Inferior')
    """)
    
    conn.commit()
    conn.close()
