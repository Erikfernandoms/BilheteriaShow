from fastapi import APIRouter, Depends, status
import sqlite3
from app.models.pagamento import PagamentoBase, PagamentoOut
from app.controllers.pagamentos.pagamento_service import registrar_pagamento, mock_pagamento_externo

router = APIRouter()

def get_db():
    conn = sqlite3.connect("bilhetagem.db", timeout=30)
    try:
        yield conn
    finally:
        conn.close()

@router.post("/", response_model=PagamentoOut, status_code=201)
def criar_pagamento(pagamento: PagamentoBase, db=Depends(get_db)):
    return registrar_pagamento(db, pagamento)

@router.post("/mock")
def mock_pagamento():
    resultado = mock_pagamento_externo()
    if resultado["status"] == "aprovado":
        return resultado
    return resultado, status.HTTP_402_PAYMENT_REQUIRED