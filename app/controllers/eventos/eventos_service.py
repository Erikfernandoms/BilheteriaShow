



def listar_eventos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento")
    colunas = [desc[0] for desc in cursor.description]
    eventos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    return eventos

def listar_setores_eventos(conn, id_evento: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM setor_evento where id_evento = ?", (id_evento,))
    colunas = [desc[0] for desc in cursor.description]
    eventos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    return eventos

def obter_evento(conn, evento_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento WHERE id_evento = ?", (evento_id,))
    evento = cursor.fetchone()
    
    if evento:
        colunas = [desc[0] for desc in cursor.description]
        return dict(zip(colunas, evento))
    else:
        return None

def obter_setores_eventos(conn, setor_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM setor_evento WHERE id_setor_evento = ?", (setor_id,))
    colunas = [desc[0] for desc in cursor.description]
    setores_eventos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    return setores_eventos

def criar_evento(conn, evento):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO evento (nome, descricao, local, data)
        VALUES (?, ?, ?, ?)
    """, (evento.nome, evento.descricao, evento.local, evento.data))
    conn.commit()
    return {
        "id_evento": cursor.lastrowid,
        "nome": evento.nome,
        "descricao": evento.descricao,
        "local": evento.local,
        "data": evento.data
    }


def atualizar_evento(conn, evento_id: int, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE evento
        SET nome = ?, descricao = ?, local = ?, data = ?
        WHERE id_evento = ?
    """, (dados.nome, dados.descricao, dados.local, dados.data, evento_id))
    conn.commit()

    if cursor.rowcount == 0:
        return None

    return {
        "id_evento": evento_id,
        "nome": dados.nome,
        "descricao": dados.descricao,
        "local": dados.local,
        "data": dados.data
    }

def deletar_evento(conn, evento_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evento WHERE id_evento = ?", (evento_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False
    return True

