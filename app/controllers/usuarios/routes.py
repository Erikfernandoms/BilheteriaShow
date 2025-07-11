from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from app.controllers.usuarios.usuarios_service import atualizar_usuario, deletar_usuario, obter_usuario, criar_usuario
from app.models.usuario import UsuarioBase, UsuarioOut

router = APIRouter()
def get_db():
    conn = sqlite3.connect("bilhetagem.db", timeout=30)
    try:
        yield conn
    finally:
        conn.close()

@router.post("/", response_model=UsuarioOut)
def criar(usuario: UsuarioBase, db = Depends(get_db)):
    return criar_usuario(db, usuario)


@router.get("/{usuario_email}", response_model=UsuarioOut)
def obter(usuario_email: str, db = Depends(get_db)):
    usuario = obter_usuario(db, usuario_email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioOut)
def atualizar(usuario_id: int, dados: UsuarioBase, db = Depends(get_db)):
    usuario = atualizar_usuario(db, usuario_id, dados)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.delete("/{usuario_id}", response_model=None)
def deletar(usuario_id: int, db = Depends(get_db)):
    sucesso = deletar_usuario(db, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}

