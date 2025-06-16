import pytest
from unittest.mock import patch, MagicMock, mock_open
from app.controllers.notas_fiscais.nota_fiscal_service import gerar_nota_fiscal



def test_gerar_nota_fiscal_sucesso(conn_mock, pedido_mock, usuario_mock, produtos_mock):
    pedido_id = 123
    nome_evento = "Rock in Rio"
    pagamento_id = 999

    with patch("app.controllers.notas_fiscais.nota_fiscal_service.buscar_pedido_repository", return_value=pedido_mock), \
         patch("app.controllers.notas_fiscais.nota_fiscal_service.buscar_usuario_repository", return_value=usuario_mock), \
         patch("app.controllers.notas_fiscais.nota_fiscal_service.buscar_nome_evento_repository", return_value=nome_evento), \
         patch("app.controllers.notas_fiscais.nota_fiscal_service.buscar_produtos_do_pedido_repository", return_value=produtos_mock), \
         patch("app.controllers.notas_fiscais.nota_fiscal_service.buscar_pagamento_aprovado_repository", return_value=pagamento_id), \
         patch("app.controllers.notas_fiscais.nota_fiscal_service.inserir_nota_fiscal_repository") as inserir_mock, \
         patch("builtins.open", mock_open()) as mocked_file, \
         patch("json.dump") as json_dump:
        
        gerar_nota_fiscal(conn_mock, pedido_id)

        mocked_file.assert_called_once()
        json_dump.assert_called_once()
        inserir_mock.assert_called_once()

        args = inserir_mock.call_args[0]
        assert args[0] == conn_mock
        assert args[1] == pedido_id
        assert args[2] == pagamento_id
        assert "nota_123.json" in args[3]
        assert args[4] == 300.00
        assert args[5] == "NFS-000123"
        assert isinstance(args[6], str)  # data_emissao


def test_gerar_nota_fiscal_pedido_nao_encontrado(conn_mock):
    with patch("app.controllers.notas_fiscais.nota_fiscal_service.buscar_pedido_repository", return_value=None):
        with pytest.raises(Exception, match="Pedido não encontrado"):
            gerar_nota_fiscal(conn_mock, 999)