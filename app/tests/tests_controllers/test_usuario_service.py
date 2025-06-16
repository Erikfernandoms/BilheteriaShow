from app.tests.conftest import delete_memory
import pytest
from fastapi import HTTPException
from app.controllers.usuarios.usuarios_service import (
    listar_usuarios,
    criar_usuario,
    obter_usuario,
    atualizar_usuario,
    deletar_usuario
)


def test_criar_e_listar_usuarios(conn, usuario_valido):
    from conftest import delete_memory
    delete_memory(conn)
    criar_usuario(conn, usuario_valido)
    usuarios = listar_usuarios(conn)
    assert any(usuario["email"] == usuario_valido.email for usuario in usuarios)

def test_criar_usuario_com_email_duplicado_gera_erro(conn, usuario_valido):
    # Primeiro usuário com CPF e e-mail válidos
    criar_usuario(conn, usuario_valido)

    # Segundo usuário com mesmo e-mail, mas CPF diferente
    usuario_com_email_repetido = type(usuario_valido)(
        nome="Outro Nome",
        email=usuario_valido.email,       # <-- mesmo e-mail
        cpf="99999999999",                # <-- CPF diferente
        senha="outrasenha",
        telefone="11888888888",
        cep="98765-432"
    )

    with pytest.raises(HTTPException) as exc:
        criar_usuario(conn, usuario_com_email_repetido)

    assert "e-mail" in str(exc.value.detail)

def test_obter_usuario(conn, usuario_valido):
    criar_usuario(conn, usuario_valido)
    usuario = obter_usuario(conn, usuario_valido.email)
    assert usuario["nome"] == usuario_valido.nome
    assert usuario["cpf"] == usuario_valido.cpf

def test_atualizar_usuario(conn, usuario_valido):
    criar_usuario(conn, usuario_valido)
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario FROM usuario WHERE email=?", (usuario_valido.email,))
    usuario_id = cursor.fetchone()[0]

    usuario_valido.nome = "Maria da Silva"
    usuario_valido.cep = "99999-999"

    atualizado = atualizar_usuario(conn, usuario_id, usuario_valido)
    assert atualizado["nome"] == "Maria da Silva"
    assert atualizado["cep"] == "99999-999"

def test_deletar_usuario(conn, usuario_valido):
    criar_usuario(conn, usuario_valido)
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario FROM usuario WHERE email=?", (usuario_valido.email,))
    usuario_id = cursor.fetchone()[0]

    resultado = deletar_usuario(conn, usuario_id)
    assert resultado is True

    usuarios = listar_usuarios(conn)
    assert not any(usuario["id_usuario"] == usuario_id for usuario in usuarios)
