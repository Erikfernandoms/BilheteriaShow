from datetime import datetime

def inserir_pagamento_repository(conn, pagamento):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pagamento (id_pedido, status, metodo_pagamento, valor_total, data_criacao, data_confirmacao)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        pagamento.id_pedido,
        pagamento.status,
        pagamento.metodo_pagamento,
        pagamento.valor_total,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") if pagamento.status == "aprovado" else None
    ))
    return cursor.lastrowid

def atualizar_status_pedido_repository(conn, id_pedido, status):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pedido SET status = ?, atualizado_em = CURRENT_TIMESTAMP WHERE id_pedido = ?",
        (status, id_pedido)
    )