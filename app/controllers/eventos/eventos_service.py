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

def listar_cadeiras(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cadeira")
    colunas = [desc[0] for desc in cursor.description]
    cadeiras = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    return cadeiras

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

def atualizar_setor_evento(conn, setor_id: int, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE setor_evento
        SET nome = ?, quantidade_lugares = ?, preco_base = ?
        WHERE id_setor_evento = ?
    """, (dados.nome, dados.quantidade_lugares, dados.preco_base, setor_id))
    conn.commit()

    if cursor.rowcount == 0:
        return None

    return {
        "id_setor_evento": setor_id,
        "nome": dados.nome,
        "quantidade_lugares": dados.quantidade_lugares,
        "preco_base": dados.preco_base,
        "id_evento": dados.id_evento
    }


def listar_cadeiras_disponiveis(conn, id_setor_evento: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_cadeira, c.identificacao
        FROM cadeira c
        JOIN cadeira_do_setor cs ON c.id_cadeira = cs.id_cadeira
        WHERE cs.id_setor_evento = ? AND cs.reservada = 0
    """, (id_setor_evento,))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]