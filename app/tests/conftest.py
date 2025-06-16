from datetime import datetime, timedelta
from types import SimpleNamespace
import pytest
from unittest.mock import MagicMock
import sqlite3

class DummyEvento:
    def __init__(self, nome, descricao, local, data, id_evento=None):
        self.nome = nome
        self.descricao = descricao
        self.local = local
        self.data = data
        self.id_evento = id_evento

class DummyPagamento:
    def __init__(self, id_pedido, status, metodo_pagamento, valor_total):
        self.id_pedido = id_pedido
        self.status = status
        self.metodo_pagamento = metodo_pagamento
        self.valor_total = valor_total


class DadosSetor:
    def __init__(self, nome, quantidade_lugares, preco_base, id_evento):
        self.nome = nome
        self.quantidade_lugares = quantidade_lugares
        self.preco_base = preco_base
        self.id_evento = id_evento



@pytest.fixture
def pagamento_aprovado():
    return DummyPagamento(id_pedido=1, status="aprovado", metodo_pagamento="cartao", valor_total=300.0)

@pytest.fixture
def pagamento_recusado():
    return DummyPagamento(id_pedido=1, status="recusado", metodo_pagamento="boleto", valor_total=300.0)


@pytest.fixture
def conn_mock():
    conn = MagicMock()
    conn.commit = MagicMock()
    conn.rollback = MagicMock()
    return conn

@pytest.fixture
def pedido_mock():
    return {
        "id_usuario": 1,
        "id_evento": 2,
        "setor": "VIP",
        "cadeira": "A1",
        "quantidade_ingressos": 2,
        "valor_total": 300.00
    }

@pytest.fixture
def usuario_mock():
    return {
        "id_usuario": 1,
        "nome": "João da Silva",
        "email": "joao@email.com"
    }



@pytest.fixture
def produtos_mock():
    return [
        {"nome": "Camiseta", "quantidade": 1, "preco_unitario": 80.00},
        {"nome": "Copo", "quantidade": 2, "preco_unitario": 30.00}
    ]


"""
Criação da tabela sem database em memória para testes rápidos
"""

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
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

    # Dados de exemplo mínimos
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES ('Teste', 'Desc', 'Local', '2025-12-01')")
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES ('VIP', 100, 150.0, 1)")
    cursor.execute("INSERT INTO cadeira (identificacao) VALUES ('A1'), ('A2')")
    cursor.execute("INSERT INTO cadeira_do_setor (id_cadeira, id_setor_evento) VALUES (1, 1), (2, 1)")

    conn.commit()
    yield conn
    conn.close()


def delete_memory(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cadeira_do_setor")
    cursor.execute("DELETE FROM cadeira")
    cursor.execute("DELETE FROM setor_evento")
    cursor.execute("DELETE FROM pedido")



def setup_pedido(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome, email, CPF, senha, telefone, cep)
        VALUES ('Usuário', 'user@email.com', '12345678900', 'senha123', '11999999999', '12345-000')
    """)
    id_usuario = cursor.lastrowid

    cursor.execute("""
        INSERT INTO pedido (
            id_usuario, id_evento, id_setor_evento,
            status, setor, cadeira,
            quantidade_ingressos, valor_total
        ) VALUES (?, 1, 1, 'reservado', 'VIP', 'A1', 2, 300.00)
    """, (id_usuario,))
    return cursor.lastrowid

def setup_pedido_para_pagamento(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome, email, CPF, senha, telefone, cep)
        VALUES ('Cliente', 'cliente@email.com', '00000000001', 'senha123', '11999999999', '01234-000')
    """)
    id_usuario = cursor.lastrowid

    cursor.execute("""
        INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos, valor_total)
        VALUES (?, 1, 1, 'reservado', 'VIP', 'A1', 2, 300.0)
    """, (id_usuario,))
    conn.commit()

def criar_usuario_e_pedido(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome, email, CPF, senha, telefone, cep)
        VALUES ('João', 'joao@email.com', '12345678901', 'senha123', '11999999999', '12345-000')
    """)
    id_usuario = cursor.lastrowid

    cursor.execute("""
        INSERT INTO pedido (
            id_usuario, id_evento, id_setor_evento, status,
            setor, cadeira, quantidade_ingressos, valor_total
        ) VALUES (?, 1, 1, 'reservado', 'VIP', 'A1', 2, 300)
    """, (id_usuario,))
    id_pedido = cursor.lastrowid
    return id_usuario, id_pedido

@pytest.fixture
def pedido():
    fake = MagicMock()
    fake.id_usuario = 1
    fake.id_evento = 2
    fake.id_setor_evento = 3
    fake.quantidade_ingressos = 1
    fake.status = "reservado"
    fake.setor = "VIP"
    fake.cadeira = "A1"
    fake.reservado_ate = "2025-01-01 12:00:00"
    fake.valor_total = 100.0
    return fake


@pytest.fixture
def pedido_base():
    return SimpleNamespace(
        id_usuario=1,
        id_evento=1,
        id_setor_evento=1,
        status="reservado",
        setor="VIP",
        cadeira="C1,C2",
        quantidade_ingressos=2,
        reservado_ate=(datetime.now() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
        valor_total=300.0
    )

