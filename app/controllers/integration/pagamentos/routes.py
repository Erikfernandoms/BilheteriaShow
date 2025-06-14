from fastapi import APIRouter, status
from app.controllers.integration.pagamentos.pagamento_service import mock_pagamento_externo

router = APIRouter()

@router.post("/mock")
def mock_pagamento():
    resultado = mock_pagamento_externo()
    if resultado["status"] == "aprovado":
        return resultado
    return resultado, status.HTTP_402_PAYMENT_REQUIRED