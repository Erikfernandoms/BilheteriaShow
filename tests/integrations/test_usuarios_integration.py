from unittest.mock import patch
from fastapi.testclient import TestClient
from run import app
from app.interface.usuarios import cadastrar_usuario, login, atualizar_conta

client = TestClient(app)


@patch("builtins.input", side_effect=[
    "Usuário Teste",                  # nome
    "usuario_teste@teste.com",       # email
    "senha123",                      # senha
    "12345678900",                   # cpf
    "11999999999",                   # telefone
    "12345678"                       # cep
])
def test_cadastrar_usuario(mock_input):
    cadastrar_usuario()
    response = client.get("/usuarios/usuario_teste@teste.com")
    assert response.status_code == 200
    assert response.json()["nome"] == "Usuário Teste"


@patch("builtins.input", side_effect=[
    "usuario_teste@teste.com",  # email
    "senha123"                   # senha
])
def test_login_usuario(mock_input):
    usuario = login()
    assert usuario["email"] == "usuario_teste@teste.com"


@patch("builtins.input", side_effect=[
    "Usuário Atualizado", "usuario@teste.com", "123456", "cpf_teste", "11999999999", "01001000"
])
def test_atualizar_usuario(mock_input):
    # Cadastro prévio do usuário
    cadastrar_usuario()
    with patch("builtins.input", side_effect=[
        "usuario@teste.com", "123456"
    ]):
        usuario = login()
    # Atualização
    with patch("builtins.input", side_effect=[
        "Usuário Atualizado", "", "", "", "", ""
    ]):
        atualizado = atualizar_conta(usuario)

        assert atualizado is not None
        assert atualizado["nome"] == "Usuário Atualizado"


def test_deletar_usuario():
    response = client.get("/usuarios/usuario_teste@teste.com")
    assert response.status_code == 200
    usuario = response.json()
    delete_response = client.delete(f"/usuarios/{usuario['id_usuario']}")
    assert delete_response.status_code == 200

    confirm = client.get(f"/usuarios/{usuario['email']}")
    assert confirm.status_code == 404