
#from app.models.usuario import Usuario
#from app.schemas.usuario import UsuarioCreate


def listar_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    return usuarios

def criar_usuario(conn, usuario):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome, email, cpf, senha, telefone, cep)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (usuario.nome, usuario.email, usuario.cpf, usuario.senha, usuario.telefone, usuario.cep))
    conn.commit()
    return {
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "senha": usuario.senha,
        "telefone": usuario.telefone,
        "cep": usuario.cep
    }

def obter_usuario(conn, usuario_email: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE email = ?", (usuario_email,))
    usuario = cursor.fetchone()
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

def atualizar_usuario(conn, usuario_id: int, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuario
        SET nome = ?, email = ?, cpf = ?, senha = ?, telefone = ?, cep = ?
        WHERE id_usuario = ?
    """, (dados.nome, dados.email, dados.cpf, dados.senha, dados.telefone, dados.cep, usuario_id))
    conn.commit()
    
    if cursor.rowcount == 0:
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

def deletar_usuario(conn, usuario_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (usuario_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False
    return True

