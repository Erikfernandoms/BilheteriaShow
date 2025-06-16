import pytest

@pytest.fixture
def usuario_mock():
    return {
        "id_usuario": 999,
        "nome": "Usuário Teste",
        "email": "teste@teste.com",
        "cpf": "00000000000"
    }

@pytest.fixture
def evento_mock():
    return {
        "id_evento": 3,  # Evento "Pericles" que tem cadeiras
        "nome": "Pericles",
        "descricao": "Aaaah se eu largar o freio!",
        "data": "2025-09-10",
        "hora": "20:00"
    }

@pytest.fixture
def setor_mock_cadeira():
    return {
        "id_setor_evento": 6,  # setor "Cadeira Inferior" do evento "Pericles"
        "nome": "Cadeira Inferior",
        "preco_base": 80.0
    }

@pytest.fixture
def setor_mock_pista():
    return {
        "id_setor_evento": 1,  # "Pista" do "Show do Coldplay"
        "nome": "Pista",
        "preco_base": 125.0
    }


@pytest.fixture
def produtos_mock():
    return [
        {"id_produto": 1, "nome": "Camiseta Oficial", "preco": 50.0, "estoque_disponivel": 10, "ativo": True},
        {"id_produto": 2, "nome": "Boné", "preco": 25.0, "estoque_disponivel": 0, "ativo": True},
        {"id_produto": 3, "nome": "Caneca", "preco": 30.0, "estoque_disponivel": 5, "ativo": False}
    ]

@pytest.fixture
def usuario_mock():
    return {"id_usuario": 1, "nome": "Usuário Teste", "email": "teste@teste.com"}

@pytest.fixture
def evento_mock():
    return {"id_evento": 1, "nome": "Evento Teste"}

@pytest.fixture
def setor_mock_pista():
    return {"id_setor_evento": 1, "nome": "Pista", "preco_base": 100.0}

@pytest.fixture
def setor_mock_cadeiras():
    return {"id_setor_evento": 2, "nome": "Cadeiras", "preco_base": 150.0}

class DummyPedido:
    def __init__(self, id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos, valor_total, reservado_ate):
        self.id_usuario = id_usuario
        self.id_evento = id_evento
        self.id_setor_evento = id_setor_evento
        self.status = status
        self.setor = setor
        self.cadeira = cadeira
        self.quantidade_ingressos = quantidade_ingressos
        self.valor_total = valor_total
        self.reservado_ate = reservado_ate