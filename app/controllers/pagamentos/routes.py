from fastapi import APIRouter, Depends, Response, status
import sqlite3
from app.models.pagamento import PagamentoBase, PagamentoOut
from app.controllers.pagamentos.pagamento_service import registrar_pagamento, mock_pagamento_externo

router = APIRouter()
from app.controllers.pagamentos.circuit_breaker import circuito_pagamento


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
def mock_pagamento(response: Response):
    if not circuito_pagamento.permitir_execucao():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "falha_circuito"}

    resultado = mock_pagamento_externo()
    if resultado["status"] == "aprovado":
        circuito_pagamento.resetar()
        return resultado
    else:
        circuito_pagamento.registrar_falha()
        response.status_code = status.HTTP_402_PAYMENT_REQUIRED
        return resultado