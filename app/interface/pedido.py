import requests
from datetime import datetime, timedelta
from app.interface.produto import oferecer_produtos


def reserva_ingresso(usuario_logado, evento, setor, quantidade, cadeira=None):
    data_solicitacao = datetime.now()
    data_reserva = data_solicitacao + timedelta(minutes=1)
    response = requests.post(
        "http://localhost:8000/pedidos",
        json={
            "id_usuario": usuario_logado['id_usuario'],
            "id_evento": evento['id_evento'],
            "id_setor_evento": setor['id_setor_evento'],
            "status": "reservado",
            "setor": setor['nome'],
            "cadeira": cadeira,
            "quantidade_ingressos": int(quantidade),
            "valor_total": float(setor['preco_base']) * int(quantidade),
            "reservado_ate": data_reserva.strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    if response.status_code not in (200,201):
        try:
            erro = response.json()
            print(f"\nErro ao reservar ingresso: {erro.get('erro') or erro.get('detail') or 'Tente novamente.'}")
        except Exception:
            print("\nErro ao reservar ingresso. Tente novamente.")
        return
    pedido = response.json()
    id_pedido = pedido['id_pedido']

    print("\n=== RESERVA DE INGRESSO ===")
    print(f"Pedido reservado com sucesso! ID: {id_pedido}")
    print("Você tem 15 minutos para concluir sua compra.")

    print("Agora você pode adicionar produtos ao pedido.")
    oferecer_produtos(id_pedido, evento['id_evento'])

def listar_pedidos(usuario_logado):
    response = requests.get(f"http://localhost:8000/pedidos/{usuario_logado['id_usuario']}")
    if response.status_code == 404:
        print("\nVocê ainda não possui pedidos.")
        return
    if response.status_code != 200:
        print("\nNão foi possível recuperar os pedidos.")
        return

    pedidos = response.json()
    if not pedidos:
        print("\nVocê ainda não possui pedidos.")
        return

    print("\nSeus pedidos:")
    for pedido in pedidos:
        response = requests.get(f"http://localhost:8000/eventos/{pedido['id_evento']}")
        if response.status_code != 200:
            print("\nErro ao buscar detalhes do evento.")
            return
        evento = response.json()
        print(f"\nPedido ID: {pedido['id_pedido']}")
        print(f"Evento: {evento['nome']} | Setor: {pedido['setor']}")
        print(f"Ingressos: {pedido['quantidade_ingressos']} | Total: R${pedido['valor_total']:.2f}")
        print(f"Status: {pedido['status']} | Válido até: {pedido['reservado_ate']}")