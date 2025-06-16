import pytest
from app.controllers.produtos.produtos_service import (
    listar_produtos,
    listar_produtos_do_evento,
    associar_produto_ao_evento,
    criar_produto,
    atualizar_produto,
    deletar_produto,
    adicionar_produto_pedido
)

def test_criar_obter_produto(conn, produto_base):
    produto = criar_produto(conn, produto_base)
    assert produto["nome"] == produto_base.nome
    assert produto["estoque_disponivel"] == produto_base.estoque_disponivel

def test_listar_produtos(conn, produto_base):
    criar_produto(conn, produto_base)
    produtos = listar_produtos(conn)
    assert isinstance(produtos, list)
    assert any(pedido["nome"] == "Camiseta" for pedido in produtos)

def test_listar_produtos_do_evento(conn, produto_base):
    produto = criar_produto(conn, produto_base)
    associar_produto_ao_evento(conn, 1, produto["id_produto"])
    produtos_evento = listar_produtos_do_evento(conn, 1)
    assert any(p["id_produto"] == produto["id_produto"] for p in produtos_evento)

def test_atualizar_produto(conn, produto_base):
    produto = criar_produto(conn, produto_base)
    produto_base.preco = 120.0
    atualizado = atualizar_produto(conn, produto["id_produto"], produto_base)
    assert atualizado["preco"] == 120.0

def test_deletar_produto(conn, produto_base):
    produto = criar_produto(conn, produto_base)
    deletado = deletar_produto(conn, produto["id_produto"])
    assert deletado is True

def test_adicionar_produto_pedido(conn, produto_base):
    from conftest import criar_usuario_e_pedido
    id_usuario, id_pedido = criar_usuario_e_pedido(conn)
    produto = criar_produto(conn, produto_base)
    resultado = adicionar_produto_pedido(conn, id_pedido, produto["id_produto"], 1)
    assert resultado["id_pedido"] == id_pedido
    assert resultado["id_produto"] == produto["id_produto"]
    assert resultado["quantidade"] == 1