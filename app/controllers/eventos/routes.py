from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from typing import List
from app.controllers.eventos.eventos_service import listar_eventos, listar_cadeiras, atualizar_setor_evento,listar_cadeiras_disponiveis,criar_evento, obter_evento, atualizar_evento, deletar_evento, listar_setores_eventos, obter_setores_eventos
from app.models.evento import EventoOut, EventoBase, SetorEventoOut
from app.models.evento import CadeiraOut
from fastapi_cache.decorator import cache

router = APIRouter()
def get_db():
    conn = sqlite3.connect("bilhetagem.db", timeout=30)
    try:
        yield conn
    finally:
        conn.close()

@router.get("/setores/cadeiras", response_model=List[SetorEventoOut])
@cache(expire=300)
def listar_setores_cadeiras(db = Depends(get_db)):
    setores_eventos = listar_cadeiras(db)
    if not setores_eventos:
        raise HTTPException(status_code=404, detail="Nenhuma cadeira encontrada")
    return setores_eventos

@router.get("/setores/{evento_id}", response_model=List[SetorEventoOut])
@cache(expire=300)
def listar_setores(evento_id: int, db = Depends(get_db)):
    setores_eventos = listar_setores_eventos(db, evento_id)
    if not setores_eventos:
        raise HTTPException(status_code=404, detail="Nenhum setor de evento encontrado")
    return setores_eventos

@router.get("/setores/{id_setor_evento}/cadeiras/disponiveis", response_model=List[CadeiraOut])
def listar_cadeiras_setor_disponiveis(id_setor_evento: int, db = Depends(get_db)):
    cadeiras_disponiveis = listar_cadeiras_disponiveis(db, id_setor_evento)
    if not cadeiras_disponiveis:
        raise HTTPException(status_code=404, detail="Nenhuma cadeira disponível encontrada para o setor de evento")
    return cadeiras_disponiveis

@router.get("/setor/{setor_id}", response_model=SetorEventoOut)
def lista_setor(setor_id: int, db = Depends(get_db)):
    setores_eventos = obter_setores_eventos(db, setor_id)
    if not setores_eventos:
        raise HTTPException(status_code=404, detail="Setor de evento não encontrado")
    return setores_eventos[0]

@router.put("/setor/{setor_id}", response_model=SetorEventoOut)
def atualizar_setor(setor_id: int, dados: SetorEventoOut, db = Depends(get_db)):
    setor_evento = atualizar_setor_evento(db, setor_id, dados)
    if not setor_evento:
        raise HTTPException(status_code=404, detail="Setor de evento não encontrado")
    return setor_evento

@router.get("/{evento_id}", response_model=EventoOut)
@cache(expire=300)
def lista_evento(evento_id: int, db = Depends(get_db)):     
    evento = obter_evento(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return EventoOut(**evento)

@router.get("/", response_model=List[EventoOut])
@cache(expire=300)
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