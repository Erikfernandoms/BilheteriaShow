import pytest
from unittest.mock import patch, MagicMock
from app.interface.produto import oferecer_produtos


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
