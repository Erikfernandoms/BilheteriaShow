import sqlite3
from fastapi import HTTPException
from app.repositories.usuarios_repository import atualizar_usuario_repository, criar_usuario_repository, deletar_usuario_repository, listar_usuarios_repository, obter_usuario_repository



def listar_usuarios(conn):
    try:
        return listar_usuarios_repository(conn)
    except Exception as e:
        raise e

def criar_usuario(conn, usuario):
    try:
        return criar_usuario_repository(conn, usuario)
    except sqlite3.IntegrityError as e:
        if "cpf" in str(e).lower():
            raise HTTPException(status_code=400, detail="Já existe um usuário cadastrado com esse CPF.")
        if "email" in str(e).lower():
            raise HTTPException(status_code=400, detail="Já existe um usuário cadastrado com esse e-mail.")
        raise HTTPException(status_code=400, detail="Erro ao criar usuário: dados duplicados.")

def obter_usuario(conn, usuario_email: str):
    try:
        usuario = obter_usuario_repository(conn,  usuario_email)
        if usuario:
            return {
                "id_usuario": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "cpf": usuario[3],
                "senha": usuario[4], 
                "telefone": usuario[5],
                "cep": usuario[6],
                "criado_em": usuario[7]
            }
        else:
            return None
    except Exception as e:
        raise e

def atualizar_usuario(conn, usuario_id: int, dados):
    try:
        atualizado = atualizar_usuario_repository(conn, usuario_id, dados)
        if not atualizado:
            return None

        return {
            "id_usuario": usuario_id,
            "nome": dados.nome,
            "email": dados.email,
            "cpf": dados.cpf,
            "senha": dados.senha,
            "telefone": dados.telefone,
            "cep": dados.cep
        }
    except Exception as e:
        raise e
    
def deletar_usuario(conn, usuario_id: int):
    try:
        if deletar_usuario_repository(conn, usuario_id):
            return True
        else:
            return False

    except Exception as e:
        raise e

