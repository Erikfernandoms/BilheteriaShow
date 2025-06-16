import pytest
from unittest.mock import patch
from app.interface.eventos import menu_eventos, menu_setores


@patch("builtins.input", side_effect=["0"])  # Nenhuma opção válida, sai do menu
def test_menu_eventos_sem_opcao_valida(mock_input, usuario_mock, capsys):
    menu_eventos(usuario_mock)
    output = capsys.readouterr().out
    assert "=== EVENTOS ===" in output or "Nenhum evento encontrado" in output

@patch("builtins.input", side_effect=["1", ""])  # Listar pedidos
def test_menu_eventos_listar_pedidos_logado(mock_input, usuario_mock, capsys):
    menu_eventos(usuario_mock)
    output = capsys.readouterr().out
    assert "seus pedidos" in output.lower() or "não possui pedidos" in output.lower()

@patch("builtins.input", side_effect=[
    "2",   # Escolher comprar ingresso
    "1",   # ID do evento
    "1",   # ID do setor
    "1",  # Quantidade de ingressos
    "",  # pula adição de produto
    "2" # volta ao menu
])
def test_menu_eventos_compra_ingresso_logado(mock_input, usuario_mock, capsys):
    menu_eventos(usuario_mock)
    output = capsys.readouterr().out
    assert "comprar ingresso" in output.lower() or "setor" in output.lower()
    assert "reservado com sucesso" in output.lower()
    

@patch("builtins.input", side_effect=["2"])  # Tentativa de compra sem login
def test_menu_eventos_compra_sem_login(mock_input, capsys):
    menu_eventos(None)
    output = capsys.readouterr().out
    assert "precisa estar logado" in output.lower()