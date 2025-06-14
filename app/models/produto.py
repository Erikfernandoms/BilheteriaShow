from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    estoque_disponivel: int
    ativo: bool

class ProdutoOut(ProdutoBase):
    id_produto: int


class PedidoProdutoBase(BaseModel):
    id_produto: int
    quantidade: int

class PedidoProdutoOut(PedidoProdutoBase):
    id_pedido_produto: int
    id_pedido: int

class ProdutoEventoBase(BaseModel):
    id_evento: int
    id_produto: int