from pydantic import BaseModel
from typing import Optional

class PagamentoBase(BaseModel):
    id_pedido: int
    status: str
    metodo_pagamento: str
    valor_total: float

class PagamentoOut(PagamentoBase):
    id_pagamento: int
    data_criacao: Optional[str]