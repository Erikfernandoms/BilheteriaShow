import re
import pytest
from unittest.mock import patch
from app.interface.pedido import reserva_ingresso, menu_pagamento


@patch("builtins.input")
def test_reserva_e_pagamento_pista(mock_input, usuario_mock, evento_mock, setor_mock_pista, capsys):
    inputs = iter([
        "",     # pular produtos
        "1",    # confirmar pagamento
        "2",    # método pix
        ""      # finalizar
    ])

    pedido_id = {"value": None}  # variável para capturar o ID

    def dynamic_input(prompt):
        if "id do pedido" in prompt.lower():
            assert pedido_id["value"] is not None, "ID ainda não foi capturado"
            return pedido_id["value"]
        return next(inputs)

    mock_input.side_effect = dynamic_input

    # Executa reserva
    reserva_ingresso(usuario_mock, evento_mock, setor_mock_pista, 1)

    # Captura output completo e extrai o ID
    output = capsys.readouterr().out.lower()
    match = re.search(r"pedido id: (\d+)", output)
    assert match, f"ID do pedido não encontrado no output: {output}"
    pedido_id["value"] = match.group(1)

    # Reexecuta pagamento
    menu_pagamento([{
        "id_pedido": int(pedido_id["value"]),
        "id_evento": evento_mock["id_evento"],
        "nome_evento": evento_mock["nome"],
        "id_setor_evento": setor_mock_pista["id_setor_evento"],
        "nome_setor": setor_mock_pista["nome"],
        "qtd_ingressos": 1,
        "total": 125.0,
        "produtos": []
    }])

    output = capsys.readouterr().out.lower()
    assert "pagamento aprovado" in output