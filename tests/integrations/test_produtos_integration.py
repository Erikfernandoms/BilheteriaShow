import pytest
from unittest.mock import patch, MagicMock
from app.interface.produto import oferecer_produtos

@pytest.fixture
def produtos_mock():
    return [
        {"id_produto": 1, "nome": "Camiseta Oficial", "preco": 50.0, "estoque_disponivel": 10, "ativo": True},
        {"id_produto": 2, "nome": "Boné", "preco": 25.0, "estoque_disponivel": 0, "ativo": True},
        {"id_produto": 3, "nome": "Caneca", "preco": 30.0, "estoque_disponivel": 5, "ativo": False}
    ]

@patch("builtins.input", side_effect=[
    "3",   # Escolher produto
    "2", # quantidade produto
    "",
    "2" # volta ao menu
])  # produto 2 (Camiseta Oficial), quantidade 1, depois sair
def test_oferecer_produtos_sucesso(mock_input, capsys):
    oferecer_produtos(pedido_id=999, id_evento=3)
    output = capsys.readouterr().out.lower()

    assert "adicionado ao pedido" in output

@patch("builtins.input", side_effect=[
    "3",   # Escolher produto
    "2000", # quantidade produto
    "",
    "2" # volta ao menu
])  # produto 2 (Camiseta Oficial), quantidade 1, depois sair
def test_oferecer_produtos_quantidade_invalida(mock_input, capsys):
    oferecer_produtos(pedido_id=999, id_evento=3)
    output = capsys.readouterr().out.lower()

    assert "excede" in output

@patch("builtins.input", side_effect=["a", ""])  # Entrada não numérica
def test_oferecer_produtos_input_invalido(mock_input, capsys):
    oferecer_produtos(pedido_id=999, id_evento=3)
    output = capsys.readouterr().out
    assert "Opção inválida" in output
