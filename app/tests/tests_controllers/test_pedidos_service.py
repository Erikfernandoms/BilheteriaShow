import pytest
from unittest.mock import MagicMock, patch
from app.controllers.pedidos.pedidos_service import (
    criar_pedido,
    listar_pedidos,
    listar_produtos_do_pedido,
    atualizar_pedido,
    deletar_pedido,
    listar_pedidos_usuario,
    cancelar_reservas_expiradas,
    reservar_cadeiras,
    liberar_cadeiras
)



def test_criar_pedido_limite_ingressos(conn_mock, pedido):
    with patch('app.controllers.pedidos.pedidos_service.obter_total_reservado_repository', return_value=3):
        result = criar_pedido(conn_mock, pedido)
        assert "erro" in result
        assert "reservar até 3 ingressos" in result["erro"]

def test_criar_pedido_cadeira_ja_reservada(conn_mock, pedido):
    with patch('app.controllers.pedidos.pedidos_service.obter_total_reservado_repository', return_value=0), \
         patch('app.controllers.pedidos.pedidos_service.obter_setor_evento_repository', return_value=[10]), \
         patch('app.controllers.pedidos.pedidos_service.inserir_pedido_repository', return_value=1):
        # Simula que a cadeira já está reservada
        cursor_mock = MagicMock()
        cursor_mock.fetchone.side_effect = [True]
        conn_mock.cursor.return_value = cursor_mock
        result = criar_pedido(conn_mock, pedido)
        assert "erro" in result
        assert "já estão reservadas" in result["erro"]

def test_criar_pedido_sucesso(conn_mock, pedido):
    with patch('app.controllers.pedidos.pedidos_service.obter_total_reservado_repository', return_value=0), \
         patch('app.controllers.pedidos.pedidos_service.obter_setor_evento_repository', return_value=[10]), \
         patch('app.controllers.pedidos.pedidos_service.atualizar_quantidade_lugares_repository'), \
         patch('app.controllers.pedidos.pedidos_service.inserir_pedido_repository', return_value=42):
        # Simula que a cadeira está livre
        cursor_mock = MagicMock()
        cursor_mock.fetchone.side_effect = [None]
        conn_mock.cursor.return_value = cursor_mock
        result = criar_pedido(conn_mock, pedido)
        assert result["id_pedido"] == 42

def test_listar_pedidos(conn_mock):
    with patch('app.controllers.pedidos.pedidos_service.listar_pedidos_repository', return_value=[(1,2,3,4,"reservado","VIP","A1",1,"2025-01-01 12:00:00",100.0,"2024-01-01 10:00:00")]):
        pedidos = listar_pedidos(conn_mock)
        assert isinstance(pedidos, list)
        assert pedidos[0]["id_pedido"] == 1

def test_atualizar_pedido_nao_encontrado(conn_mock):
    with patch('app.controllers.pedidos.pedidos_service.atualizar_pedido_repository', return_value=0):
        result = atualizar_pedido(conn_mock, 1, MagicMock())
        assert result is None

def test_deletar_pedido_sucesso(conn_mock):
    with patch('app.controllers.pedidos.pedidos_service.deletar_pedido_repository', return_value=1):
        assert deletar_pedido(conn_mock, 1) is True

def test_deletar_pedido_nao_encontrado(conn_mock):
    with patch('app.controllers.pedidos.pedidos_service.deletar_pedido_repository', return_value=0):
        assert deletar_pedido(conn_mock, 1) is False

def test_reservar_cadeiras_sucesso(conn_mock):
    with patch('app.controllers.pedidos.pedidos_service.reservar_cadeiras_repository', return_value=True):
        conn_mock.execute = MagicMock()
        conn_mock.commit = MagicMock()
        assert reservar_cadeiras(conn_mock, 3, [1,2]) is True

def test_liberar_cadeiras_sucesso(conn_mock):
    with patch('app.controllers.pedidos.pedidos_service.liberar_cadeiras_repository', return_value=True):
        conn_mock.execute = MagicMock()
        conn_mock.commit = MagicMock()
        assert liberar_cadeiras(conn_mock, 3, [1,2]) is True