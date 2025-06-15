import os
import json
from datetime import datetime
from logger import log_info, log_error
from metrics import incrementar_metrica
from app.repositories.nota_fiscal_repository import (
    buscar_pedido_repository,
    buscar_usuario_repository,
    buscar_nome_evento_repository,
    buscar_produtos_do_pedido_repository,
    buscar_pagamento_aprovado_repository,
    inserir_nota_fiscal_repository
)

PASTA_NFS = "notas_fiscais"
os.makedirs(PASTA_NFS, exist_ok=True)

def gerar_nota_fiscal(conn, pedido_id):
    pedido = buscar_pedido_repository(conn, pedido_id)
    if not pedido:
        raise Exception("Pedido não encontrado")

    usuario = buscar_usuario_repository(conn, pedido["id_usuario"]) or {}

    nome_evento = buscar_nome_evento_repository(conn, pedido["id_evento"]) or f"Evento {pedido['id_evento']}"

    produtos = buscar_produtos_do_pedido_repository(conn, pedido_id)

    valor_total_produtos = sum(p["quantidade"] * p["preco_unitario"] for p in produtos)

    valor_total_pedido = pedido.get("valor_total") or 0
    valor_ingressos = max(valor_total_pedido - valor_total_produtos, 0)

    ingresso_info = {
        "evento": nome_evento,
        "setor": pedido.get("setor"),
        "quantidade_ingressos": pedido.get("quantidade_ingressos"),
        "cadeira": pedido.get("cadeira"),
        "valor_total": valor_ingressos
    }

    id_pagamento = buscar_pagamento_aprovado_repository(conn, pedido_id)

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

    inserir_nota_fiscal_repository(
        conn, pedido_id, id_pagamento, caminho_arquivo, valor_total_pedido, numero_nota, data_emissao
    )
    print(f"Nota gerada: {caminho_arquivo}")
    log_info(f"Nota fiscal gerada para o pedido {pedido_id}: {caminho_arquivo}")