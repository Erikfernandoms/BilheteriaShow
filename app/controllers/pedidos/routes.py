from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from typing import List
from app.controllers.pedidos.pedidos_service import cancelar_pedidos_pagamento_recusado, criar_pedido, listar_produtos_do_pedido, atualizar_pedido, deletar_pedido, listar_pedidos, listar_pedidos_usuario
from app.models.pedido import PedidoBase, PedidoOut, ProdutoPedidoOut
import random

router = APIRouter()
def get_db():
    conn = sqlite3.connect("bilhetagem.db", timeout=30)
    try:
        yield conn
    finally:
        conn.close()


@router.put("/{pedido_id}/cancelar-por-pagamento-recusado", response_model=PedidoBase)
def atualizar_pagamento_recusado(pedido_id: int, db = Depends(get_db)):
    pedido = cancelar_pedidos_pagamento_recusado(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.post("/{pedido_id}/recusar")
def recusar_pagamento_pedido(pedido_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE pedido SET status = 'pagamento recusado', atualizado_em = CURRENT_TIMESTAMP WHERE id_pedido = ?", (pedido_id,))
    db.commit()
    return {"msg": "Pagamento recusado"}

@router.get("/", response_model=List[PedidoOut])
def listar(db = Depends(get_db)):
    pedido = listar_pedidos(db)
    if not pedido:
        raise HTTPException(status_code=404, detail="Nenhum pedido encontrado")
    return pedido


@router.post("/", response_model=PedidoOut)
def criar(pedido: PedidoBase, db=Depends(get_db)):
    pedido_criado = criar_pedido(db, pedido)
    if not pedido_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar pedido")
    if "erro" in pedido_criado:
        raise HTTPException(status_code=400, detail=pedido_criado["erro"])
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


@router.get("/{pedido_id}/produtos", response_model=List[ProdutoPedidoOut])
def produtos_do_pedido(pedido_id: int, db=Depends(get_db)):
    produtos = listar_produtos_do_pedido(db, pedido_id)
    if produtos is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return produtos


@router.get("/{usuario_id}/usuarios", response_model=List[PedidoOut])
def listar_pedido_usuario(usuario_id:int, db = Depends(get_db)):
    pedido = listar_pedidos_usuario(db, usuario_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Nenhum pedido encontrado")
    return pedido


@router.get("/{pedido_id}", response_model=PedidoOut)
def obter_pedido(pedido_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pedido WHERE id_pedido = ?", (pedido_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, row))