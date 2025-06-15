import sqlite3



def listar_usuarios_repository(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    return usuarios


def criar_usuario_repository(conn, usuario):
    try:
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO usuario (nome, email, cpf, senha, telefone, cep)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (usuario.nome, usuario.email, usuario.cpf, usuario.senha, usuario.telefone, usuario.cep))
        conn.commit()
        return {
            "id_usuario": cursor.lastrowid,
            "nome": usuario.nome,
            "email": usuario.email,
            "cpf": usuario.cpf,
            "senha": usuario.senha,
            "telefone": usuario.telefone,
            "cep": usuario.cep
        }
    
    except sqlite3.IntegrityError as e:
       raise e


def obter_usuario_repository(conn, usuario_email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE email = ?", (usuario_email,))
    usuario = cursor.fetchone()
    return usuario

def atualizar_usuario_repository(conn, usuario_id, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuario
        SET nome = ?, email = ?, cpf = ?, senha = ?, telefone = ?, cep = ?
        WHERE id_usuario = ?
    """, (dados.nome, dados.email, dados.cpf, dados.senha, dados.telefone, dados.cep, usuario_id))
    conn.commit()

    if cursor.rowcount == 0:
        return None
    return True
    
def deletar_usuario_repository(conn, usuario_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (usuario_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False
    return True