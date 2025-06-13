from pydantic import BaseModel
from typing import Optional
class PedidoBase(BaseModel):
    id_usuario: int
    id_evento: int
    id_setor_evento: int
    status: str
    setor: str
    cadeira: Optional[str] = None
    quantidade_ingressos: int
    valor_total: float
    reservado_ate: str
   

class PedidoOut(PedidoBase):
    id_pedido: int
    id_usuario: int
    id_evento: int
    id_setor_evento: int
    status: str
    setor: str
    cadeira: Optional[str] = None
    quantidade_ingressos: int
    reservado_ate: str
    valor_total: float