from app.tests.conftest import delete_memory
import pytest
from app.repositories.usuarios_repository import (
    listar_usuarios_repository,
    criar_usuario_repository,
    obter_usuario_repository,
    atualizar_usuario_repository,
    deletar_usuario_repository
)
import pytest
from app.repositories.usuarios_repository import (
    listar_usuarios_repository,
    criar_usuario_repository,
    obter_usuario_repository,
    atualizar_usuario_repository,
    deletar_usuario_repository
)



def test_criar_e_listar_usuarios_repository(conn, usuario_valido):
    delete_memory(conn)
    criar_usuario_repository(conn, usuario_valido)
    usuarios = listar_usuarios_repository(conn)
    assert any(usuario["email"] == usuario_valido.email for usuario in usuarios)

def test_obter_usuario_repository(conn, usuario_valido):
    criar_usuario_repository(conn, usuario_valido)
    usuario = obter_usuario_repository(conn, usuario_valido.email)
    assert usuario[1] == usuario_valido.nome
    assert usuario[2] == usuario_valido.email

def test_atualizar_usuario_repository(conn, usuario_valido):
    criado = criar_usuario_repository(conn, usuario_valido)
    usuario_valido.nome = "João Atualizado"
    usuario_valido.cep = "99999-999"
    sucesso = atualizar_usuario_repository(conn, criado["id_usuario"], usuario_valido)
    assert sucesso is True
    usuario = obter_usuario_repository(conn, usuario_valido.email)
    assert usuario[1] == "João Atualizado"

def test_deletar_usuario_repository(conn, usuario_valido):
    criado = criar_usuario_repository(conn, usuario_valido)
    deletado = deletar_usuario_repository(conn, criado["id_usuario"])
    assert deletado is True
    usuario = obter_usuario_repository(conn, usuario_valido.email)
    assert usuario is None

def test_deletar_usuario_inexistente_retorna_false(conn):
    resultado = deletar_usuario_repository(conn, usuario_id=9999)
    assert resultado is False

def test_atualizar_usuario_inexistente_retorna_none(conn, usuario_valido):
    resultado = atualizar_usuario_repository(conn, usuario_id=9999, dados=usuario_valido)
    assert resultado is None
