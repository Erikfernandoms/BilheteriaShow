from datetime import datetime
import random 
from app.controllers.notas_fiscais.nota_fiscal_service import gerar_nota_fiscal
from logger import log_info, log_error
from metrics import incrementar_metrica
from app.repositories.pagamentos_repository import (
    inserir_pagamento_repository,
    atualizar_status_pedido_repository
)

def registrar_pagamento(conn, pagamento):
    try:
        id_pagamento = inserir_pagamento_repository(conn, pagamento)
        novo_status = "pagamento aprovado" if pagamento.status == "aprovado" else "pagamento recusado"
        atualizar_status_pedido_repository(conn, pagamento.id_pedido, novo_status)
        conn.commit()
        if pagamento.status == "aprovado":
            gerar_nota_fiscal(conn, pagamento.id_pedido)
            log_info(f"Pagamento aprovado para o pedido {pagamento.id_pedido}. Nota fiscal gerada.")
            incrementar_metrica("pagamentos_aprovados")
        else:
            log_error(f"Pagamento recusado para o pedido {pagamento.id_pedido}.")
            incrementar_metrica("pagamentos_recusados")
        return {
            "id_pagamento": id_pagamento,
            "id_pedido": pagamento.id_pedido,
            "status": pagamento.status,
            "metodo_pagamento": pagamento.metodo_pagamento,
            "valor_total": pagamento.valor_total,
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        conn.rollback()
        log_error(f"Erro ao registrar pagamento: {e}")
        raise e

def mock_pagamento_externo():
    if random.random() < 0.9:
        return {"status": "aprovado"}
    return {"status": "recusado"}