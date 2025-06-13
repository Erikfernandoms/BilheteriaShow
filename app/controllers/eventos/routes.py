from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from typing import List
from app.controllers.eventos.eventos_service import listar_eventos, criar_evento, obter_evento, atualizar_evento, deletar_evento, listar_setores_eventos, obter_setores_eventos
from app.models.evento import EventoOut, EventoBase, SetorEventoOut

router = APIRouter()
def get_db():
    conn = sqlite3.connect("bilhetagem.db")
    try:
        yield conn
    finally:
        conn.close()

@router.get("/setores/{evento_id}", response_model=List[SetorEventoOut])
def listar_setores(evento_id: int, db = Depends(get_db)):
    setores_eventos = listar_setores_eventos(db, evento_id)
    if not setores_eventos:
        raise HTTPException(status_code=404, detail="Nenhum setor de evento encontrado")
    return setores_eventos

@router.get("/setor/{setor_id}", response_model=SetorEventoOut)
def lista_setor(setor_id: int, db = Depends(get_db)):
    setores_eventos = obter_setores_eventos(db, setor_id)
    if not setores_eventos:
        raise HTTPException(status_code=404, detail="Setor de evento não encontrado")
    return setores_eventos[0]

@router.get("/{evento_id}", response_model=EventoOut)
def lista_evento(evento_id: int, db = Depends(get_db)):     
    evento = obter_evento(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return EventoOut(**evento)

@router.get("/", response_model=List[EventoOut])
def listar(db = Depends(get_db)):
    eventos = listar_eventos(db)
    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado")
    return eventos

@router.post("/", response_model=EventoBase)
def criar(evento: EventoBase, db = Depends(get_db)):
    criar_evento(db, evento)
    return evento

@router.put("/{evento_id}", response_model=EventoBase)
def atualizar(evento_id: int, dados: EventoBase, db = Depends(get_db)):
    evento = atualizar_evento(db, evento_id, dados)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return evento

@router.delete("/{evento_id}", response_model=None)
def deletar(evento_id: int, db = Depends(get_db)):
    sucesso = deletar_evento(db, evento_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return {"message": "Evento deletado com sucesso"}