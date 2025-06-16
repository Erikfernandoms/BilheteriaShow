from app.tests.conftest import DadosSetor, DummyEvento
import pytest
from unittest.mock import MagicMock, patch
from app.controllers.eventos.eventos_service import (
    atualizar_setor_evento,
    listar_cadeiras,
    listar_eventos,
    criar_evento,
    atualizar_evento,
    deletar_evento,
    listar_cadeiras_disponiveis,
    listar_setores_eventos,
    obter_evento,
    obter_setores_eventos
)


def test_listar_eventos(conn_mock):
    with patch('app.controllers.eventos.eventos_service.listar_eventos_repository') as mock_repo:
        mock_repo.return_value = [{"id_evento": 1, "nome": "Show"}]
        eventos = listar_eventos(conn_mock)
        assert eventos == [{"id_evento": 1, "nome": "Show"}]
        mock_repo.assert_called_once_with(conn_mock)

def test_criar_evento_success(conn_mock):
    evento = DummyEvento("Show", "Descrição", "Estádio", "2025-07-01")
    with patch('app.controllers.eventos.eventos_service.criar_evento_repository') as mock_repo:
        mock_repo.return_value = 42
        result = criar_evento(conn_mock, evento)
        assert result["id_evento"] == 42
        conn_mock.commit.assert_called_once()

def test_criar_evento_exception(conn_mock):
    evento = DummyEvento("Show", "Descrição", "Estádio", "2025-07-01")
    with patch('app.controllers.eventos.eventos_service.criar_evento_repository', side_effect=Exception("fail")):
        with pytest.raises(Exception):
            criar_evento(conn_mock, evento)
        conn_mock.rollback.assert_called_once()

def test_listar_cadeiras_disponiveis(conn_mock):
    with patch('app.controllers.eventos.eventos_service.listar_cadeiras_disponiveis_repository') as mock_repo:
        mock_repo.return_value = [{"id_cadeira": 1, "identificacao": "A1"}]
        cadeiras = listar_cadeiras_disponiveis(conn_mock, 7)
        assert cadeiras == [{"id_cadeira": 1, "identificacao": "A1"}]
        mock_repo.assert_called_once_with(conn_mock, 7)

def test_atualizar_evento_sucesso(conn_mock):
    dados = DummyEvento("Novo Show", "Nova desc", "Novo local", "2025-08-01")
    with patch('app.controllers.eventos.eventos_service.atualizar_evento_repository') as repo:
        repo.return_value = True
        result = atualizar_evento(conn_mock, 1, dados)
        assert result["nome"] == "Novo Show"
        conn_mock.commit.assert_called_once()

def test_atualizar_evento_falha(conn_mock):
    dados = DummyEvento("Novo Show", "Nova desc", "Novo local", "2025-08-01")
    with patch('app.controllers.eventos.eventos_service.atualizar_evento_repository') as repo:
        repo.return_value = False
        result = atualizar_evento(conn_mock, 1, dados)
        assert result is None
        conn_mock.rollback.assert_called_once()

def test_deletar_evento_sucesso(conn_mock):
    with patch('app.controllers.eventos.eventos_service.deletar_evento_repository') as repo:
        repo.return_value = True
        result = deletar_evento(conn_mock, 1)
        assert result is True
        conn_mock.commit.assert_called_once()

def test_deletar_evento_falha(conn_mock):
    with patch('app.controllers.eventos.eventos_service.deletar_evento_repository') as repo:
        repo.return_value = False
        result = deletar_evento(conn_mock, 1)
        assert result is False
        conn_mock.rollback.assert_called_once()

def test_listar_setores_eventos(conn_mock):
    with patch('app.controllers.eventos.eventos_service.listar_setores_eventos_repository') as repo:
        repo.return_value = ['setor1', 'setor2']
        result = listar_setores_eventos(conn_mock, 1)
        assert result == ['setor1', 'setor2']
        repo.assert_called_once_with(conn_mock, 1)

def test_listar_cadeiras(conn_mock):
    with patch('app.controllers.eventos.eventos_service.listar_cadeiras_repository') as repo:
        repo.return_value = ['cadeira1', 'cadeira2']
        result = listar_cadeiras(conn_mock)
        assert result == ['cadeira1', 'cadeira2']
        repo.assert_called_once_with(conn_mock)


def test_obter_evento(conn_mock):
    with patch('app.controllers.eventos.eventos_service.obter_evento_repository') as repo:
        repo.return_value = {"id_evento": 1, "nome": "Evento Teste"}
        result = obter_evento(conn_mock, 1)
        assert result["id_evento"] == 1
        repo.assert_called_once_with(conn_mock, 1)


def test_obter_setores_eventos(conn_mock):
    with patch('app.controllers.eventos.eventos_service.obter_setores_eventos_repository') as repo:
        repo.return_value = {"id_setor": 1, "nome": "Setor A"}
        result = obter_setores_eventos(conn_mock, 1)
        assert result["nome"] == "Setor A"
        repo.assert_called_once_with(conn_mock, 1)

def test_atualizar_setor_evento_sucesso(conn_mock):
    dados = DadosSetor("VIP", 100, 200.0, 2)

    with patch('app.controllers.eventos.eventos_service.atualizar_setor_evento_repository') as repo:
        repo.return_value = True
        result = atualizar_setor_evento(conn_mock, 1, dados)
        assert result["nome"] == "VIP"
        conn_mock.commit.assert_called_once()


def test_atualizar_setor_evento_falha(conn_mock):
    dados = DadosSetor("VIP", 100, 200.0, 2)

    with patch('app.controllers.eventos.eventos_service.atualizar_setor_evento_repository') as repo:
        repo.return_value = False
        result = atualizar_setor_evento(conn_mock, 1, dados)
        assert result is None
        conn_mock.rollback.assert_called_once()

