from app.tests.conftest import DadosSetor, DummyEvento, delete_memory
from app.repositories.eventos_repository import atualizar_evento_repository, atualizar_setor_evento_repository, deletar_evento_repository, listar_cadeiras_disponiveis_repository, listar_cadeiras_repository, listar_eventos_repository, criar_evento_repository, listar_setores_eventos_repository, obter_evento_repository, obter_setores_eventos_repository

def test_criar_e_listar_eventos(conn):
    evento = DummyEvento("Show", "Musical", "Arena", "2025-12-01")
    id_ = criar_evento_repository(conn, evento)

    eventos = listar_eventos_repository(conn)
    nomes = [e["nome"] for e in eventos]
    assert "Show" in nomes


def test_obter_evento_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)",
                   ("Cinema", "Filme", "Sala A", "2025-11-01"))
    evento_id = cursor.lastrowid
    result = obter_evento_repository(conn, evento_id)
    assert result["local"] == "Sala A"

    result_none = obter_evento_repository(conn, 999)
    assert result_none is None


def test_atualizar_evento_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)",
                   ("Evento", "Desc", "Local", "2025-01-01"))
    evento_id = cursor.lastrowid
    novo = DummyEvento("Atualizado", "Nova desc", "Novo local", "2025-06-01")
    result = atualizar_evento_repository(conn, evento_id, novo)
    assert result is True

    result_none = atualizar_evento_repository(conn, 999, novo)
    assert result_none is None


def test_deletar_evento_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)",
                   ("Excluir", "Remover", "Local", "2025-10-01"))
    evento_id = cursor.lastrowid

    result = deletar_evento_repository(conn, evento_id)
    assert result is True

    result_false = deletar_evento_repository(conn, 999)
    assert result_false is False


def test_listar_setores_eventos_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)",
                   ("Com Setor", "Teste", "Ginásio", "2025-08-08"))
    evento_id = cursor.lastrowid
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES (?, ?, ?, ?)",
                   ("VIP", 100, 150.0, evento_id))
    conn.commit()

    setores = listar_setores_eventos_repository(conn, evento_id)
    assert len(setores) == 1
    assert setores[0]["nome"] == "VIP"


def test_obter_setores_eventos_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES (?, ?, ?, ?)",
                   ("Pista", 300, 100.0, 1))
    setor_id = cursor.lastrowid
    result = obter_setores_eventos_repository(conn, setor_id)
    assert len(result) == 1
    assert result[0]["nome"] == "Pista"


def test_atualizar_setor_evento_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES (?, ?, ?, ?)",
                   ("Velho", 100, 50.0, 1))
    setor_id = cursor.lastrowid

    dados = DadosSetor("Novo", 200, 120.0, 1)
  
    result = atualizar_setor_evento_repository(conn, setor_id, dados)
    assert result is True

    result_none = atualizar_setor_evento_repository(conn, 999, dados)
    assert result_none is None


def test_listar_cadeiras_repository(conn):
    delete_memory(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cadeira (identificacao) VALUES ('A1'), ('A2')")
    conn.commit()

    cadeiras = listar_cadeiras_repository(conn)
    assert len(cadeiras) == 2
    assert cadeiras[0]["identificacao"] == "A1"


def test_listar_cadeiras_disponiveis_repository(conn):
    delete_memory(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cadeira (identificacao) VALUES ('B1')")
    c1 = cursor.lastrowid
    cursor.execute("INSERT INTO cadeira (identificacao) VALUES ('B2')")
    c2 = cursor.lastrowid
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES (?, ?, ?, ?)",
                   ("Mezanino", 2, 80.0, 1))
    setor_id = cursor.lastrowid
    cursor.execute("INSERT INTO cadeira_do_setor (id_cadeira, id_setor_evento) VALUES (?, ?), (?, ?)",
                   (c1, setor_id, c2, setor_id))
    cursor.execute("INSERT INTO usuario (nome, email, CPF, senha, telefone, cep) VALUES (?, ?, ?, ?, ?, ?)",
               ("Teste", "teste@email.com", "12345678900", "senha123", "11999999999", "12345-000"))
    usuario_id = cursor.lastrowid

    cursor.execute("INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, cadeira, status) VALUES (?, ?, ?, ?, ?)",
                    (usuario_id, 1, setor_id, 'B2', 'reservado'))
    conn.commit()

    disponiveis = listar_cadeiras_disponiveis_repository(conn, setor_id)
    assert len(disponiveis) == 1
    assert disponiveis[0]["identificacao"] == "B1"