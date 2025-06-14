from datetime import datetime
import random 

def registrar_pagamento(conn, pagamento):
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
    # Atualiza status do pedido
    novo_status = "pagamento aprovado" if pagamento.status == "aprovado" else "pagamento recusado"
    cursor.execute("UPDATE pedido SET status = ?, atualizado_em = CURRENT_TIMESTAMP WHERE id_pedido = ?", (novo_status, pagamento.id_pedido))
    conn.commit()
    return {
        "id_pagamento": cursor.lastrowid,
        "id_pedido": pagamento.id_pedido,
        "status": pagamento.status,
        "metodo_pagamento": pagamento.metodo_pagamento,
        "valor_total": pagamento.valor_total,
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def mock_pagamento_externo():
    if random.random() < 0.9:
        return {"status": "aprovado"}
    return {"status": "recusado"}