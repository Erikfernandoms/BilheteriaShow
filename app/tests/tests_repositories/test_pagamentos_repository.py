import pytest
from datetime import datetime
from app.repositories.pagamentos_repository import (
    inserir_pagamento_repository,
    atualizar_status_pedido_repository
)
from app.tests.conftest import DummyPagamento, setup_pedido



def test_inserir_pagamento_repository_aprovado(conn):
    id_pedido = setup_pedido(conn)
    pagamento = DummyPagamento(
        id_pedido=id_pedido,
        status="aprovado",
        metodo_pagamento="cartao",
        valor_total=300.00
    )

    id_pagamento = inserir_pagamento_repository(conn, pagamento)
    assert isinstance(id_pagamento, int)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = ?", (id_pagamento,))
    resultado = cursor.fetchone()

    assert resultado is not None
    assert resultado[1] == id_pedido
    assert resultado[2] == "aprovado"
    assert resultado[3] == "cartao"
    assert resultado[4] == 300.00
    assert resultado[5] is not None
    assert resultado[6] is not None  # data_confirmacao presente

def test_inserir_pagamento_repository_recusado(conn):
    id_pedido = setup_pedido(conn)
    pagamento = DummyPagamento(
        id_pedido=id_pedido,
        status="recusado",
        metodo_pagamento="pix",
        valor_total=250.00
    )

    id_pagamento = inserir_pagamento_repository(conn, pagamento)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = ?", (id_pagamento,))
    resultado = cursor.fetchone()

    assert resultado is not None
    assert resultado[2] == "recusado"
    assert resultado[3] == "pix"
    assert resultado[6] is None  # data_confirmacao ausente

def test_atualizar_status_pedido_repository(conn):
    id_pedido = setup_pedido(conn)

    atualizar_status_pedido_repository(conn, id_pedido, "aprovado")

    cursor = conn.cursor()
    cursor.execute("SELECT status FROM pedido WHERE id_pedido = ?", (id_pedido,))
    status = cursor.fetchone()[0]

    assert status == "aprovado"