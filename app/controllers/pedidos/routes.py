from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from typing import List
from app.controllers.pedidos.pedidos_service import criar_pedido, atualizar_pedido, deletar_pedido, listar_pedidos, listar_pedidos_usuario
from app.models.pedido import PedidoBase, PedidoOut
router = APIRouter()
def get_db():
    conn = sqlite3.connect("bilhetagem.db")
    try:
        yield conn
    finally:
        conn.close()


@router.get("/", response_model=List[PedidoOut])
def listar(db = Depends(get_db)):
    pedido = listar_pedidos(db)
    if not pedido:
        raise HTTPException(status_code=404, detail="Nenhum pedido encontrado")
    return pedido

@router.get("/{usuario_id}", response_model=List[PedidoOut])
def listar_pedido_usuario(usuario_id:int, db = Depends(get_db)):
    pedido = listar_pedidos_usuario(db, usuario_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Nenhum pedido encontrado")
    return pedido

@router.post("/", response_model=PedidoOut)
def criar(pedido: PedidoBase,db=Depends(get_db)):
    pedido_criado = criar_pedido(db, pedido)
    if not pedido_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar pedido")
    return pedido_criado

@router.put("/{pedido_id}", response_model=PedidoBase)
def atualizar(pedido_id: int, dados: PedidoBase, db = Depends(get_db)):
    pedido = atualizar_pedido(db, pedido_id, dados)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.delete("/{pedido_id}", response_model=None)
def deletar(pedido_id: int, db = Depends(get_db)):
    sucesso = deletar_pedido(db, pedido_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": "Pedido deletado com sucesso"}