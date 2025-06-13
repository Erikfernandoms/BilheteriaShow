from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    email: str
    senha: str
    cpf: str
    telefone: str
    cep: str

class UsuarioCreate(UsuarioBase):
    pass


class UsuarioOut(UsuarioBase):
    id_usuario: int
    nome: str
    email: str
    cpf: str
    telefone: str
    cep: str