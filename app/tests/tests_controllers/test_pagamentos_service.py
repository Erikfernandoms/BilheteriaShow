


from app.controllers.pagamentos.pagamento_service import registrar_pagamento
from unittest.mock import patch

from app.tests.conftest import setup_pedido_para_pagamento



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