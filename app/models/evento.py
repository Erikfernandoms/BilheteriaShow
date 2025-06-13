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