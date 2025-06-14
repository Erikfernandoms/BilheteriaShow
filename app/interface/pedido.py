import time
import requests
from datetime import datetime, timedelta
from app.interface.produto import oferecer_produtos


def reserva_ingresso(usuario_logado, evento, setor, quantidade, cadeira=None):
    data_solicitacao = datetime.now()
    data_reserva = data_solicitacao + timedelta(minutes=15)
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
    pedidos_pendentes = [pedido]  # O pedido recém-criado
    while True:
        print("\nDeseja finalizar a compra agora?")
        print("1 - Sim")
        print("2 - Não, finalizar depois")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            menu_pagamento(pedidos_pendentes)
            break
        elif escolha == "2":
            print("Você pode finalizar o pagamento depois em 'Meus pedidos'.")
            break
        else:
            print("Opção inválida.")

def listar_pedidos(usuario_logado):
    response = requests.get(f"http://localhost:8000/pedidos/{usuario_logado['id_usuario']}/usuarios")
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
    
    pedidos_pendentes = [p for p in pedidos if p['status'] == 'reservado']
    if pedidos_pendentes:
        menu_pagamento(pedidos_pendentes)

def menu_pagamento(pedidos_pendentes):
    while True:
        usuario_id = pedidos_pendentes[0]['id_usuario'] if pedidos_pendentes else None
        if usuario_id:
            response = requests.get(f"http://localhost:8000/pedidos/{usuario_id}/usuarios")
            if response.status_code == 200:
                pedidos = response.json()
                pedidos_pendentes = [p for p in pedidos if p['status'] == 'reservado']
            else:
                print("\nNão foi possível atualizar a lista de pedidos.")
                break

        if not pedidos_pendentes:
            print("\nNenhum pedido pendente de pagamento.")
            break

        print("\nPedidos pendentes de pagamento:")
        for pedido in pedidos_pendentes:
            evento_resp = requests.get(f"http://localhost:8000/eventos/{pedido['id_evento']}")
            nome_evento = evento_resp.json()['nome'] if evento_resp.status_code == 200 else f"Evento {pedido['id_evento']}"

            print(f"\nPedido ID: {pedido['id_pedido']} | Evento: {nome_evento}")
            print(f"Setor: {pedido['setor']}")
            print(f"Ingressos: {pedido['quantidade_ingressos']}")
            print(f"Total: R${pedido['valor_total']:.2f}")

            produtos_resp = requests.get(f"http://localhost:8000/pedidos/{pedido['id_pedido']}/produtos")
            if produtos_resp.status_code == 200:
                produtos = produtos_resp.json()
                if produtos:
                    print("Produtos:")
                    for produto in produtos:
                        print(f"  - {produto['nome']} x{produto['quantidade']}")
                else:
                    print("Produtos: Nenhum")
            else:
                print("Produtos: Erro ao buscar")

        escolha = input("\nDigite o ID do pedido que deseja pagar (ou ENTER para voltar): ")
        if not escolha:
            break
        try:
            id_pedido = int(escolha)
            if any(pedido['id_pedido'] == id_pedido for pedido in pedidos_pendentes):
                finalizar_pagamento(id_pedido)
                
                response = requests.get(f"http://localhost:8000/pedidos/{usuario_id}/usuarios")
                if response.status_code == 200:
                    pedidos = response.json()
                    pedidos_pendentes = [pedido for pedido in pedidos if pedido['status'] == 'reservado']
                    if not pedidos_pendentes:
                        print("\nNenhum pedido pendente de pagamento.")
                        break
                else:
                    print("\nNão foi possível atualizar a lista de pedidos.")
                    break
            else:
                print("ID inválido.")
        except Exception as e:
            print(e)
            print("Entrada inválida.")

def finalizar_pagamento(id_pedido):
    print("\nEscolha a forma de pagamento:")
    print("1 - Cartão de Crédito")
    print("2 - Pix")
    print("3 - Boleto")
    formas = {"1": "cartao", "2": "pix", "3": "boleto"}
    while True:
        escolha = input("Digite o número da forma de pagamento: ")
        if escolha in formas:
            metodo_pagamento = formas[escolha]
            break
        else:
            print("Opção inválida.")

    print("\nProcessando pagamento...")
    response = requests.post("http://localhost:8000/pagamentos/mock")
    status_pagamento = "aprovado" if response.status_code == 200 and response.json()["status"] == "aprovado" else "recusado"

    pedido_resp = requests.get(f"http://localhost:8000/pedidos/{id_pedido}")
    if pedido_resp.status_code == 200:
        pedido = pedido_resp.json()
        valor_total = pedido["valor_total"]
    else:
        valor_total = 0

    response = requests.post(
        f"http://localhost:8000/pagamentos/",
        json={
            "id_pedido": id_pedido,
            "status": status_pagamento,
            "metodo_pagamento": metodo_pagamento,
            "valor_total": valor_total
        }
    )
    if status_pagamento == "aprovado" and response.status_code == 201:
        print("Pagamento aprovado! Sua compra está confirmada.")
    elif status_pagamento == "recusado":
        print("Pagamento recusado pelo banco. Tente novamente.")
    else:
        print("Erro ao registrar pagamento no sistema.")