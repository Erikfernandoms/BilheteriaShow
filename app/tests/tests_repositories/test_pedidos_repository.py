from app.repositories.pedidos_repository import atualizar_quantidade_lugares_repository, deletar_pedido_repository, inserir_pedido_repository, liberar_cadeiras_repository, listar_pedidos_repository, inserir_pedido_repository, obter_cadeiras_pedido_repository, obter_total_reservado_repository, reservar_cadeiras_repository
from app.tests.conftest import delete_memory


def test_inserir_listar_deletar_pedido_repository(conn, pedido_base):
    pedido_id = inserir_pedido_repository(conn, pedido_base)
    assert isinstance(pedido_id, int)

    pedidos = listar_pedidos_repository(conn)
    assert any(p[0] == pedido_id for p in pedidos)

    count = deletar_pedido_repository(conn, pedido_id)
    assert count == 1

def test_obter_total_reservado_repository(conn):
    total = obter_total_reservado_repository(conn, 1, 1)
    assert isinstance(total, int)

def test_atualizar_quantidade_lugares_repository(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES (?, ?, ?, ?)",
                   ("Pista", 10, 100.0, 1))
    setor_id = cursor.lastrowid

    atualizar_quantidade_lugares_repository(conn, setor_id, 2)

    cursor.execute("SELECT quantidade_lugares FROM setor_evento WHERE id_setor_evento = ?", (setor_id,))
    assert cursor.fetchone()[0] == 8

def test_reservar_e_liberar_cadeiras_repository(conn):
    delete_memory(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cadeira (identificacao) VALUES ('A1'), ('A2')")
    c1, c2 = 1, 2
    cursor.execute("INSERT INTO setor_evento (nome, quantidade_lugares, preco_base, id_evento) VALUES (?, ?, ?, ?)",
                   ("Superior", 100, 100.0, 1))
    setor_id = cursor.lastrowid
    cursor.execute("INSERT INTO cadeira_do_setor (id_cadeira, id_setor_evento) VALUES (?, ?), (?, ?)",
                   (c1, setor_id, c2, setor_id))
    conn.commit()

    assert reservar_cadeiras_repository(conn, setor_id, [c1, c2]) is True
    assert liberar_cadeiras_repository(conn, setor_id, [c1, c2]) is True

def test_obter_cadeiras_pedido_repository(conn, pedido_base):
    pedido_id = inserir_pedido_repository(conn, pedido_base)
    cadeiras = obter_cadeiras_pedido_repository(conn, pedido_id)
    assert cadeiras == pedido_base.cadeira
