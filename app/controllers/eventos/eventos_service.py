from app.repositories.eventos_repository import (
    listar_eventos_repository,
    listar_setores_eventos_repository,
    listar_cadeiras_repository,
    obter_evento_repository,
    obter_setores_eventos_repository,
    criar_evento_repository,
    atualizar_evento_repository,
    deletar_evento_repository,
    atualizar_setor_evento_repository,
    listar_cadeiras_disponiveis_repository
)

def listar_eventos(conn):
    return listar_eventos_repository(conn)

def listar_setores_eventos(conn, id_evento: int):
    return listar_setores_eventos_repository(conn, id_evento)

def listar_cadeiras(conn):
    return listar_cadeiras_repository(conn)

def obter_evento(conn, evento_id: int):
    return obter_evento_repository(conn, evento_id)

def obter_setores_eventos(conn, setor_id: int):
    return obter_setores_eventos_repository(conn, setor_id)

def criar_evento(conn, evento):
    try:
        evento_id = criar_evento_repository(conn, evento)
        conn.commit()
        return {
            "id_evento": evento_id,
            "nome": evento.nome,
            "descricao": evento.descricao,
            "local": evento.local,
            "data": evento.data
        }
    except Exception as e:
        conn.rollback()
        raise e

def atualizar_evento(conn, evento_id: int, dados):
    try:
        atualizado = atualizar_evento_repository(conn, evento_id, dados)
        if not atualizado:
            conn.rollback()
            return None
        conn.commit()
        return {
            "id_evento": evento_id,
            "nome": dados.nome,
            "descricao": dados.descricao,
            "local": dados.local,
            "data": dados.data
        }
    except Exception as e:
        conn.rollback()
        raise e

def deletar_evento(conn, evento_id: int):
    try:
        resultado = deletar_evento_repository(conn, evento_id)
        if resultado:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False
    except Exception as e:
        conn.rollback()
        raise e

def atualizar_setor_evento(conn, setor_id: int, dados):
    try:
        atualizado = atualizar_setor_evento_repository(conn, setor_id, dados)
        if not atualizado:
            conn.rollback()
            return None
        conn.commit()
        return {
            "id_setor_evento": setor_id,
            "nome": dados.nome,
            "quantidade_lugares": dados.quantidade_lugares,
            "preco_base": dados.preco_base,
            "id_evento": dados.id_evento
        }
    except Exception as e:
        conn.rollback()
        raise e

def listar_cadeiras_disponiveis(conn, id_setor_evento: int):
    return listar_cadeiras_disponiveis_repository(conn, id_setor_evento)  # CERTO: chama a função e retorna o resultado