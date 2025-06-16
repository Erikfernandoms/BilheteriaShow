import re
import pytest
from unittest.mock import patch
from app.interface.pedido import reserva_ingresso


@patch("builtins.input")
def test_reserva_e_pagamento_pista(mock_input, usuario_mock, evento_mock, setor_mock_pista, capsys):
    dynamic_inputs = []

    def dynamic_input(prompt):
        output = capsys.readouterr().out.lower()
        if "id do pedido" in prompt.lower():
            match = re.search(r"pedido id: (\d+)", output)
            assert match, f"ID do pedido não encontrado no output: {output}"
            return match.group(1)
        elif dynamic_inputs:
            return dynamic_inputs.pop(0)
        else:
            return ""

    dynamic_inputs[:] = [
        "",     # pula produtos
        "1",    # confirma pagamento
        "2",    # método pix
        ""      # fim
    ]

    mock_input.side_effect = dynamic_input

    reserva_ingresso(usuario_mock, evento_mock, setor_mock_pista, 1)

    output = capsys.readouterr().out.lower()
    assert "pagamento aprovado" in output

@patch("builtins.input")
def test_reserva_e_pagamento_cadeiras(mock_input, usuario_mock, evento_mock, setor_mock_cadeiras, capsys):
    dynamic_inputs = []

    def dynamic_input(prompt):
        output = capsys.readouterr().out.lower()
        if "escolha as cadeiras" in prompt.lower():
            # Simula escolha da(s) cadeira(s) disponível(is)
            return "A1"
        elif "id do pedido" in prompt.lower():
            match = re.search(r"pedido id: (\d+)", output)
            assert match, f"ID do pedido não encontrado no output: {output}"
            return match.group(1)
        elif dynamic_inputs:
            return dynamic_inputs.pop(0)
        else:
            return ""

    dynamic_inputs[:] = [
        "",     # pula produtos
        "1",    # confirma pagamento
        "1",    # método cartão
        ""      # fim
    ]

    mock_input.side_effect = dynamic_input

    reserva_ingresso(usuario_mock, evento_mock, setor_mock_cadeiras, 1)

    output = capsys.readouterr().out.lower()
    assert "pagamento aprovado" in output