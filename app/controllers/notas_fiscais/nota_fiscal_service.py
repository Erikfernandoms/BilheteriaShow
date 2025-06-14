import os
import json
from datetime import datetime

PASTA_NFS = "notas_fiscais"
os.makedirs(PASTA_NFS, exist_ok=True)

def gerar_nota_fiscal(conn, pedido_id):
    cursor = conn.cursor()

    # Buscar dados do pedido
    cursor.execute("SELECT * FROM pedido WHERE id_pedido = ?", (pedido_id,))
    pedido_row = cursor.fetchone()
    if not pedido_row:
        raise Exception("Pedido não encontrado")
    pedido_cols = [desc[0] for desc in cursor.description]
    pedido = dict(zip(pedido_cols, pedido_row))

    # Buscar dados do usuário
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (pedido["id_usuario"],))
    usuario_row = cursor.fetchone()
    usuario_cols = [desc[0] for desc in cursor.description]
    usuario = dict(zip(usuario_cols, usuario_row)) if usuario_row else {}

    # Buscar nome do evento
    cursor.execute("SELECT nome FROM evento WHERE id_evento = ?", (pedido["id_evento"],))
    evento_row = cursor.fetchone()
    nome_evento = evento_row[0] if evento_row else f"Evento {pedido['id_evento']}"

    # Buscar produtos do pedido
    cursor.execute("""
        SELECT p.nome, pp.quantidade, pp.preco
        FROM produto_do_pedido pp
        JOIN produto p ON p.id_produto = pp.id_produto
        WHERE pp.id_pedido = ?
    """, (pedido_id,))
    produtos = [
        {"nome": row[0], "quantidade": row[1], "preco_unitario": row[2]}
        for row in cursor.fetchall()
    ]

    # Soma o valor total dos produtos
    valor_total_produtos = sum(p["quantidade"] * p["preco_unitario"] for p in produtos)

    # Valor dos ingressos = valor_total do pedido - valor_total_produtos
    valor_total_pedido = pedido.get("valor_total") or 0
    valor_ingressos = max(valor_total_pedido - valor_total_produtos, 0)

    # Buscar informações do ingresso (evento, setor, quantidade, cadeira)
    ingresso_info = {
        "evento": nome_evento,
        "setor": pedido.get("setor"),
        "quantidade_ingressos": pedido.get("quantidade_ingressos"),
        "cadeira": pedido.get("cadeira"),
        "valor_total": valor_ingressos
    }

    # Buscar id_pagamento aprovado
    cursor.execute("""
        SELECT id_pagamento FROM pagamento
        WHERE id_pedido = ? AND status = 'aprovado'
        ORDER BY data_confirmacao DESC LIMIT 1
    """, (pedido_id,))
    pagamento_row = cursor.fetchone()
    id_pagamento = pagamento_row[0] if pagamento_row else None

    numero_nota = f"NFS-{pedido_id:06d}"
    data_emissao = datetime.now().isoformat()

    nota = {
        "numero_nota": numero_nota,
        "data_emissao": data_emissao,
        "cliente": {
            "id": usuario.get("id_usuario"),
            "nome": usuario.get("nome"),
            "email": usuario.get("email")
        },
        "produtos": produtos,
        "ingresso": ingresso_info,
        "total": valor_total_pedido,
        "mensagem": "Nota fiscal gerada automaticamente após pagamento."
    }

    caminho_arquivo = os.path.join(PASTA_NFS, f"nota_{pedido_id}.json")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(nota, f, indent=4, ensure_ascii=False)

    registrar_nota_fiscal(conn, pedido_id, id_pagamento, caminho_arquivo, valor_total_pedido, numero_nota, data_emissao)
    print(f"Nota gerada: {caminho_arquivo}")
    return caminho_arquivo

def registrar_nota_fiscal(conn, id_pedido, id_pagamento, link_s3, valor_total, numero, emitida_em):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nota_fiscal (id_pedido, id_pagamento, link_s3, valor_total, numero, emitida_em)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_pedido, id_pagamento, link_s3, valor_total, numero, emitida_em))
    conn.commit()
    return {
        "id_nota": cursor.lastrowid,
        "id_pedido": id_pedido,
        "id_pagamento": id_pagamento,
        "link_s3": link_s3,
        "valor_total": valor_total,
        "numero": numero,
        "emitida_em": emitida_em
    }