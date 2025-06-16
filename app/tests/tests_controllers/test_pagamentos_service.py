


from app.controllers.pagamentos.pagamento_service import registrar_pagamento
from unittest.mock import patch

def setup_pedido_para_pagamento(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome, email, CPF, senha, telefone, cep)
        VALUES ('Cliente', 'cliente@email.com', '00000000001', 'senha123', '11999999999', '01234-000')
    """)
    id_usuario = cursor.lastrowid

    cursor.execute("""
        INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos, valor_total)
        VALUES (?, 1, 1, 'pendente', 'VIP', 'A1', 2, 300.0)
    """, (id_usuario,))
    conn.commit()


@patch("app.controllers.pagamentos.pagamento_service.gerar_nota_fiscal")
@patch("app.controllers.pagamentos.pagamento_service.incrementar_metrica")
@patch("app.controllers.pagamentos.pagamento_service.log_info")
def test_registrar_pagamento_aprovado(mock_log, mock_metric, mock_nf, conn, pagamento_aprovado):
    setup_pedido_para_pagamento(conn)

    resultado = registrar_pagamento(conn, pagamento_aprovado)

    assert resultado["id_pagamento"] is not None
    assert resultado["status"] == "aprovado"
    assert resultado["metodo_pagamento"] == "cartao"
    assert resultado["valor_total"] == 300.0

    mock_log.assert_called_once()
    mock_metric.assert_called_with("pagamentos_aprovados")
    mock_nf.assert_called_once()

@patch("app.controllers.pagamentos.pagamento_service.gerar_nota_fiscal")
@patch("app.controllers.pagamentos.pagamento_service.incrementar_metrica")
@patch("app.controllers.pagamentos.pagamento_service.log_error")
def test_registrar_pagamento_recusado(mock_log, mock_metric, mock_nf, conn, pagamento_recusado):
    setup_pedido_para_pagamento(conn)

    resultado = registrar_pagamento(conn, pagamento_recusado)

    assert resultado["id_pagamento"] is not None
    assert resultado["status"] == "recusado"
    assert resultado["metodo_pagamento"] == "boleto"
    assert resultado["valor_total"] == 300.0

    mock_log.assert_called_once()
    mock_metric.assert_called_with("pagamentos_recusados")
    mock_nf.assert_not_called()