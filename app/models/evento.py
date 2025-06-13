from pydantic import BaseModel

class EventoBase(BaseModel):
    nome: str
    descricao: str
    data: str
    local: str

class EventoOut(EventoBase):
    id_evento: int
    nome: str
    descricao: str
    local: str
    data: str
    criado_em: str


class SetorEventoBase(BaseModel):
    nome: str
    quantidade_lugares: int
    preco_base: float


class SetorEventoOut(SetorEventoBase):
    id_setor_evento: int
    nome: str
    quantidade_lugares: int
    preco_base: float
    id_evento: int