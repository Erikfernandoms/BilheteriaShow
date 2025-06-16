from unittest.mock import patch
from app.interface.eventos import menu_eventos




@patch("builtins.input", side_effect=[
    "2",   # Escolher comprar ingresso
    "1",   # ID do evento
    "1",   # ID do setor
    "1",  # Quantidade de ingressos
    "",  # pula adição de produto
    "1",
    "1"
])
def test_reserva_e_pagamento_pista(mock_input, usuario_mock, capsys):
    menu_eventos(usuario_mock)
    output = capsys.readouterr().out
    assert "pagamento aprovado" in output.lower()



@patch("builtins.input", side_effect=[
    "2",   # Escolher comprar ingresso
    "3",   # ID do evento
    "6",   # ID do setor
    "1",  # Quantidade de ingressos
    "10",  # Cadeira
    "",# pula adição de produto
    "1",
    "1"
])
def test_reserva_e_pagamento_cadeira(mock_input, usuario_mock, capsys):
    menu_eventos(usuario_mock)
    output = capsys.readouterr().out
    assert "pagamento aprovado" in output.lower()