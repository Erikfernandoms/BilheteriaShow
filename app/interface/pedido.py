import requests
from datetime import datetime, timedelta



def reserva_ingresso(usuario_logado, evento, setor, quantidade, cadeira=None):
    data_solicitacao = datetime.now()
    data_reserva = data_solicitacao + timedelta(minutes=15)
    response = requests.post(
        "http://localhost:8000/pedidos",
        json={
            "id_usuario": usuario_logado['id_usuario'],
            "id_evento": evento['id_evento'],
            "id_setor_evento": setor['id_setor_evento'],
            "status": "solicitado",
            "setor": setor['nome'],
            "cadeira": cadeira,
            "quantidade_ingressos": int(quantidade),
            "valor_total": float(setor['preco_base']) * int(quantidade),
            "reservado_ate": data_reserva.strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    if response.status_code not in (200,201):
        print("\n❌ Erro ao reservar ingresso. Tente novamente.")
        return
    pedido = response.json()
    id_pedido = pedido['id_pedido']


    print(f"✅ Pedido reservado com sucesso! ID: {id_pedido}")
    print("🕐 Você tem 15 minutos para concluir sua compra.")
    print("👉 Agora você pode adicionar produtos ao pedido.")
