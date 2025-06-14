from datetime import datetime

def criar_pedido(conn, pedido):
    cursor = conn.cursor()
    try:
        # Soma os ingressos já reservados/aprovados para o evento por esse usuário
        cursor.execute("""
            SELECT COALESCE(SUM(quantidade_ingressos), 0)
            FROM pedido
            WHERE id_usuario = ? AND id_evento = ? AND status IN ('reservado', 'pagamento aprovado')
        """, (pedido.id_usuario, pedido.id_evento))
        total_reservado = cursor.fetchone()[0]

        if total_reservado + pedido.quantidade_ingressos > 3:
            return {"erro": "Você só pode reservar até 3 ingressos por evento, considerando todos os seus pedidos ativos."}

        conn.execute('BEGIN IMMEDIATE')

        cursor.execute("""
            SELECT quantidade_lugares 
            FROM setor_evento 
            WHERE id_setor_evento = ?
        """, (pedido.id_setor_evento,))
        row = cursor.fetchone()
        if not row or row[0] < pedido.quantidade_ingressos:
            conn.rollback()
            return {"erro": "Ingressos insuficientes para o setor selecionado."}

        cursor.execute("""
            UPDATE setor_evento 
            SET quantidade_lugares = quantidade_lugares - ?
            WHERE id_setor_evento = ?
        """, (pedido.quantidade_ingressos, pedido.id_setor_evento))

        cursor.execute("""
            INSERT INTO pedido (id_usuario, id_evento, id_setor_evento, status, setor, cadeira, quantidade_ingressos, reservado_ate, valor_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pedido.id_usuario,
            pedido.id_evento,
            pedido.id_setor_evento,
            pedido.status,
            pedido.setor,
            pedido.cadeira,
            pedido.quantidade_ingressos,
            pedido.reservado_ate,
            pedido.valor_total
        ))

        conn.commit()
        return {
            "id_pedido": cursor.lastrowid,
            "id_usuario": pedido.id_usuario,
            "id_evento": pedido.id_evento,
            "id_setor_evento": pedido.id_setor_evento,
            "setor": pedido.setor,
            "cadeira": pedido.cadeira,
            "quantidade_ingressos": pedido.quantidade_ingressos,
            "valor_total": pedido.valor_total,
            "reservado_ate": pedido.reservado_ate,
            "status": pedido.status
        }
    except Exception as e:
        conn.rollback()
        return {"erro": f"Erro ao criar pedido: {str(e)}"}

def listar_pedidos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()
    return [
        {
            "id_pedido": pedido[0],
            "id_usuario": pedido[1],
            "id_evento": pedido[2],
            "id_setor_evento": pedido[3],
            "status": pedido[4],
            "setor": pedido[5],
            "cadeira": pedido[6],
            "quantidade_ingressos": pedido[7],
            "reservado_ate": pedido[8],
            "valor_total": pedido[9],
            "criado_em": pedido[10],
            "atualizado_em": pedido[11]
        } for pedido in pedidos
    ]

def atualizar_pedido(conn, pedido_id, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedido
        SET id_usuario = ?, id_evento = ?, id_setor_evento = ?, status = ?, setor = ?, cadeira = ?, reservado_ate = ?, valor_total = ?, atualizado_em = CURRENT_TIMESTAMP
        WHERE id_pedido = ?
    """, (dados.id_usuario,
        dados.id_evento,
        dados.id_setor_evento,
        dados.status,
        dados.setor,
        dados.cadeira,
        dados.reservado_ate,
        dados.valor_total,
        pedido_id
    ))
    conn.commit()

    if cursor.rowcount == 0:
        return None

    return {
        "id_pedido": pedido_id,
        "id_usuario": dados.id_usuario,
        "id_evento": dados.id_evento,
        "id_setor_evento": dados.id_setor_evento,
        "status": dados.status,
        "setor": dados.setor,
        "cadeira": dados.cadeira,
        "reservado_ate": dados.reservado_ate,
        "valor_total": dados.valor_total,
        "quantidade_ingressos": dados.quantidade_ingressos
    }

def deletar_pedido(conn, pedido_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido WHERE id_pedido = ?", (pedido_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return False

    return True

def listar_pedidos_usuario(conn, usuario_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido WHERE id_usuario = ? and status != 'cancelado'", (usuario_id,))
    pedidos = cursor.fetchall()
    
    if not pedidos:
        return []

    return [
        {
            "id_pedido": pedido[0],
            "id_usuario": pedido[1],
            "id_evento": pedido[2],
            "id_setor_evento": pedido[3],
            "status": pedido[4],
            "setor": pedido[5],
            "cadeira": pedido[6],
            "quantidade_ingressos": pedido[7],
            "reservado_ate": pedido[8],
            "valor_total": pedido[9],

        } for pedido in pedidos
    ]

def cancelar_reservas_expiradas(conn):
    cursor = conn.cursor()
    agora = datetime.now()

    cursor.execute("""
        SELECT id_pedido, reservado_ate, id_setor_evento, quantidade_ingressos FROM pedido
        WHERE status = 'reservado'
    """)
    pedidos = cursor.fetchall()

    expirados = [
        (pedido[0], pedido[2], pedido[3])  # id_pedido, id_setor_evento, quantidade_ingressos
        for pedido in pedidos
        if datetime.strptime(pedido[1], "%Y-%m-%d %H:%M:%S") < agora
    ]
    
    for id_pedido, id_setor_evento, quantidade_ingressos in expirados:
        cursor.execute("""
            UPDATE pedido
            SET status = 'expirado'
            , atualizado_em = CURRENT_TIMESTAMP
            WHERE id_pedido = ?
        """, (id_pedido,))

        cursor.execute("""
            UPDATE setor_evento
            SET quantidade_lugares = quantidade_lugares + ?
            WHERE id_setor_evento = ?
        """, (quantidade_ingressos, id_setor_evento))

        cursor.execute("""
            SELECT id_produto, quantidade FROM produto_do_pedido
            WHERE id_pedido = ?
        """, (id_pedido,))
        produtos = cursor.fetchall()
        for id_produto, quantidade in produtos:
            cursor.execute("""
                UPDATE produto
                SET estoque_disponivel = estoque_disponivel + ?
                WHERE id_produto = ?
            """, (quantidade, id_produto))

    conn.commit()