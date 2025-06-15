from logger import log_info, log_error
from metrics import incrementar_metrica
from app.repositories.produtos_repository import (
    adicionar_produto_pedido_repository,
    associar_produto_ao_evento_repository,
    atualizar_produto_repository,
    criar_produto_repository,
    deletar_produto_repository,
    listar_produtos_repository,
    listar_produtos_do_evento_repository,
    obter_produto_repository
)

def listar_produtos(conn):
    try:
        return listar_produtos_repository(conn)
    except Exception as e:
        raise e

def listar_produtos_do_evento(conn, id_evento):
    try:
        return listar_produtos_do_evento_repository(conn, id_evento)
    except Exception as e:
        raise e

def associar_produto_ao_evento(conn, id_evento: int, id_produto: int):
    try:
        if associar_produto_ao_evento_repository(conn, id_evento, id_produto):
            return {"id_evento": id_evento, "id_produto": id_produto}
        return None
    except Exception as e:
        raise e

def obter_produto(conn, produto_id: int):
    try:
        return obter_produto_repository(conn, produto_id)
    except Exception as e:
        raise e

def criar_produto(conn, produto):
    try:
        produto_id = criar_produto_repository(conn, produto)
        return obter_produto(conn, produto_id)
    except Exception as e:
        raise e

def atualizar_produto(conn, produto_id: int, dados):
    try:
        if atualizar_produto_repository(conn, produto_id, dados):
            return obter_produto(conn, produto_id)
    except Exception as e:
        raise e

def deletar_produto(conn, produto_id: int):
    try:
        return deletar_produto_repository(conn, produto_id)
    except Exception as e:
        raise e

def adicionar_produto_pedido(conn, pedido_id: int, id_produto: int, quantidade: int):
    try:
        produto_id = adicionar_produto_pedido_repository(conn, pedido_id, id_produto, quantidade)
        incrementar_metrica("produtos_adicionados_pedido")
        log_info(f"Produto {id_produto} adicionado ao pedido {pedido_id} com quantidade {quantidade}.")
        return {
            "id_pedido_produto": produto_id,
            "id_pedido": pedido_id,
            "id_produto": id_produto,
            "quantidade": quantidade
        }
    except Exception as e:
        raise e