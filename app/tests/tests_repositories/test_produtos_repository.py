import pytest
from app.repositories.produtos_repository import (
    listar_produtos_repository,
    listar_produtos_do_evento_repository,
    associar_produto_ao_evento_repository,
    obter_produto_repository,
    criar_produto_repository,
    atualizar_produto_repository,
    deletar_produto_repository,
    adicionar_produto_pedido_repository
)

def test_criar_e_obter_produto(conn, produto_base):
    id_produto = criar_produto_repository(conn, produto_base)
    produto = obter_produto_repository(conn, id_produto)
    assert produto["nome"] == produto_base.nome
    assert produto["estoque_disponivel"] == produto_base.estoque_disponivel

def test_listar_produtos_repository(conn, produto_base):
    criar_produto_repository(conn, produto_base)
    produtos = listar_produtos_repository(conn)
    assert any(p["nome"] == produto_base.nome for p in produtos)

def test_associar_e_listar_produtos_do_evento_repository(conn, produto_base):
    id_produto = criar_produto_repository(conn, produto_base)
    associar_produto_ao_evento_repository(conn, 1, id_produto)
    produtos = listar_produtos_do_evento_repository(conn, 1)
    assert any(p["id_produto"] == id_produto for p in produtos)

def test_atualizar_produto_repository(conn, produto_base):
    id_produto = criar_produto_repository(conn, produto_base)
    produto_base.preco = 120.0
    atualizar_produto_repository(conn, id_produto, produto_base)
    produto = obter_produto_repository(conn, id_produto)
    assert produto["preco"] == 120.0

def test_deletar_produto_repository(conn, produto_base):
    id_produto = criar_produto_repository(conn, produto_base)
    deletar_produto_repository(conn, id_produto)
    produto = obter_produto_repository(conn, id_produto)
    assert produto is None

def test_adicionar_produto_pedido_repository(conn, produto_base):
    from conftest import criar_usuario_e_pedido
    id_usuario, id_pedido = criar_usuario_e_pedido(conn)
    id_produto = criar_produto_repository(conn, produto_base)
    id_pedido_produto = adicionar_produto_pedido_repository(conn, id_pedido, id_produto, 2)
    assert id_pedido_produto is not None
