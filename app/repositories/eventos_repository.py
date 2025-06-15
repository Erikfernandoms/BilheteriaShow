def listar_eventos_repository(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento")
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def listar_setores_eventos_repository(conn, id_evento: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM setor_evento where id_evento = ?", (id_evento,))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def listar_cadeiras_repository(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cadeira")
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def obter_evento_repository(conn, evento_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evento WHERE id_evento = ?", (evento_id,))
    evento = cursor.fetchone()
    if evento:
        colunas = [desc[0] for desc in cursor.description]
        return dict(zip(colunas, evento))
    else:
        return None

def obter_setores_eventos_repository(conn, setor_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM setor_evento WHERE id_setor_evento = ?", (setor_id,))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

def criar_evento_repository(conn, evento):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO evento (nome, descricao, local, data)
        VALUES (?, ?, ?, ?)
    """, (evento.nome, evento.descricao, evento.local, evento.data))
    return cursor.lastrowid

def atualizar_evento_repository(conn, evento_id: int, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE evento
        SET nome = ?, descricao = ?, local = ?, data = ?
        WHERE id_evento = ?
    """, (dados.nome, dados.descricao, dados.local, dados.data, evento_id))
    if cursor.rowcount == 0:
        return None
    return True

def deletar_evento_repository(conn, evento_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evento WHERE id_evento = ?", (evento_id,))
    if cursor.rowcount == 0:
        return False
    return True

def atualizar_setor_evento_repository(conn, setor_id: int, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE setor_evento
        SET nome = ?, quantidade_lugares = ?, preco_base = ?
        WHERE id_setor_evento = ?
    """, (dados.nome, dados.quantidade_lugares, dados.preco_base, setor_id))
    if cursor.rowcount == 0:
        return None
    return True

def listar_cadeiras_disponiveis_repository(conn, id_setor_evento: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_cadeira, c.identificacao
        FROM cadeira c
        JOIN cadeira_do_setor cs ON c.id_cadeira = cs.id_cadeira
        WHERE cs.id_setor_evento = ?
        AND c.id_cadeira NOT IN (
            SELECT DISTINCT c2.id_cadeira
            FROM pedido p
            JOIN setor_evento se ON p.id_setor_evento = se.id_setor_evento
            JOIN cadeira_do_setor cs2 ON cs2.id_setor_evento = se.id_setor_evento
            JOIN cadeira c2 ON c2.id_cadeira = cs2.id_cadeira
            WHERE p.status IN ('reservado', 'pagamento aprovado')
            AND se.id_setor_evento = ?
            AND instr(',' || p.cadeira || ',', ',' || c2.identificacao || ',') > 0
        )
    """, (id_setor_evento, id_setor_evento))
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]