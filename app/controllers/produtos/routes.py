from fastapi import APIRouter, Depends, HTTPException
from typing import List
import sqlite3
from app.models.produto import PedidoProdutoBase, PedidoProdutoOut, ProdutoBase, ProdutoEventoBase, ProdutoOut
from app.controllers.produtos.produtos_service import (
    associar_produto_ao_evento, listar_produtos, obter_produto, criar_produto, atualizar_produto, deletar_produto, adicionar_produto_pedido, listar_produtos_do_evento
)
from fastapi_cache.decorator import cache

router = APIRouter()

def get_db():
    conn = sqlite3.connect("bilhetagem.db", timeout=30)
    try:
        yield conn
    finally:
        conn.close()

@router.get("/", response_model=List[ProdutoOut])
@cache(expire=300)
def listar(db=Depends(get_db)):
    return listar_produtos(db)

@router.get("/eventos/{id_evento}/produtos", response_model=List[ProdutoOut])
@cache(expire=300)
def produtos_do_evento(id_evento: int, db=Depends(get_db)):
    return listar_produtos_do_evento(db, id_evento)

@router.post("/eventos/produto", response_model=ProdutoEventoBase)
def criar_produto_do_evento(dados: ProdutoEventoBase, db=Depends(get_db)):
    return associar_produto_ao_evento(db, dados.id_evento, dados.id_produto)

@router.get("/{produto_id}", response_model=ProdutoOut)
def obter(produto_id: int, db=Depends(get_db)):
    produto = obter_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=ProdutoOut)
def criar(produto: ProdutoBase, db=Depends(get_db)):
    return criar_produto(db, produto)

@router.post("/{pedido_id}/produtos", response_model=PedidoProdutoOut)
def adicionar_produto_ao_pedido(pedido_id: int, dados: PedidoProdutoBase, db=Depends(get_db)):
    resultado = adicionar_produto_pedido(db, pedido_id, dados.id_produto, dados.quantidade)
    if not resultado:
        raise HTTPException(status_code=400, detail="Estoque insuficiente ou erro ao adicionar produto ao pedido")
    return resultado
@router.put("/{produto_id}", response_model=ProdutoOut)
def atualizar(produto_id: int, dados: ProdutoBase, db=Depends(get_db)):
    produto = atualizar_produto(db, produto_id, dados)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.delete("/{produto_id}", response_model=None)
def deletar(produto_id: int, db=Depends(get_db)):
    deletar_produto(db, produto_id)