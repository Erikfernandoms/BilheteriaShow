import time
import requests
from datetime import datetime, timedelta
from app.interface.produto import oferecer_produtos
from logger import log_info, log_error

def exibir_cadeiras_disponiveis(cadeiras):
    print("\nCadeiras disponíveis:")
    for cadeira in cadeiras:
        print(f"{cadeira['id_cadeira']} - {cadeira['identificacao']}")

def escolher_cadeiras(cadeiras_disponiveis, quantidade):
    ids_disponiveis = [cadeira['id_cadeira'] for cadeira in cadeiras_disponiveis]
    cadeiras_escolhidas = []
    for i in range(quantidade):
        while True:
            escolha = input(f"Escolha o ID da cadeira para o ingresso {i+1}: ")
            if escolha.isdigit() and int(escolha) in ids_disponiveis and int(escolha) not in cadeiras_escolhidas:
                cadeiras_escolhidas.append(int(escolha))
                break
            else:
                print("Cadeira inválida ou já escolhida. Escolha novamente.")
    return cadeiras_escolhidas

def obter_identificacoes(cadeiras_disponiveis, cadeiras_escolhidas):
    return [cadeira['identificacao'] for cadeira in cadeiras_disponiveis if cadeira['id_cadeira'] in cadeiras_escolhidas]

def reserva_ingresso(usuario_logado, evento, setor, quantidade_ingressos, cadeira=None):
    data_solicitacao = datetime.now()
    data_reserva = data_solicitacao + timedelta(minutes=15)
    cadeira_str = cadeira

    if setor['nome'].lower() in ["cadeira inferior", "cadeira superior"]:
        response = requests.get(f"http://localhost:8000/eventos/setores/{setor['id_setor_evento']}/cadeiras/disponiveis", verify=False)
        if response.status_code != 200:
            log_error("Não foi possível buscar as cadeiras disponíveis.")
            print("Não foi possível buscar as cadeiras disponíveis.")
            return
        cadeiras_disponiveis = response.json()
        if len(cadeiras_disponiveis) < int(quantidade_ingressos):
            log_error("Não há cadeiras suficientes disponíveis neste setor.")
            print("Não há cadeiras suficientes disponíveis neste setor.")
            return
        exibir_cadeiras_disponiveis(cadeiras_disponiveis)
        cadeiras_escolhidas = escolher_cadeiras(cadeiras_disponiveis, int(quantidade_ingressos))
        identificacoes = obter_identificacoes(cadeiras_disponiveis, cadeiras_escolhidas)
        cadeira_str = ",".join(identificacoes)
        log_info(f"Cadeiras escolhidas: {cadeira_str}")

    response = requests.post(
        "http://localhost:8000/pedidos",
        json={
            "id_usuario": usuario_logado['id_usuario'],
            "id_evento": evento['id_evento'],
            "id_setor_evento": setor['id_setor_evento'],
            "status": "reservado",
            "setor": setor['nome'],
            "cadeira": cadeira_str,
            "quantidade_ingressos": int(quantidade_ingressos),
            "valor_total": float(setor['preco_base']) * int(quantidade_ingressos),
            "reservado_ate": data_reserva.strftime("%Y-%m-%d %H:%M:%S")
        }, 
        verify=False
    )
    if response.status_code not in (200, 201):
        try:
            erro = response.json()
            log_error(f"Erro ao reservar ingresso: {erro.get('erro') or erro.get('detail') or 'Tente novamente.'}")
            print(f"\nErro ao reservar ingresso: {erro.get('erro') or erro.get('detail') or 'Tente novamente.'}")
        except Exception:
            log_error("Erro ao reservar ingresso. Tente novamente.")
            print("\nErro ao reservar ingresso. Tente novamente.")
        return
    pedido = response.json()
    id_pedido = pedido['id_pedido']

    log_info(f"Pedido reservado com sucesso! ID: {id_pedido}")

    print("\n=== RESERVA DE INGRESSO ===")
    print(f"Pedido reservado com sucesso! ID: {id_pedido}")
    print("Você tem 15 minutos para concluir sua compra.")

    print("Agora você pode adicionar produtos ao pedido.")
    oferecer_produtos(id_pedido, evento['id_evento'])
    pedidos_reservados = [pedido]
    while True:
        print("\nDeseja finalizar a compra agora?")
        print("1 - Sim")
        print("2 - Não, finalizar depois")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            finalizar_pagamento(id_pedido)
            break
        elif escolha == "2":
            print("Você pode finalizar o pagamento depois em 'Meus pedidos'.")
            break
        else:
            print("Opção inválida.")

def listar_pedidos(usuario_logado):
    response = requests.get(f"http://localhost:8000/pedidos/{usuario_logado['id_usuario']}/usuarios", verify=False)
    if response.status_code == 404:
        print("\nVocê ainda não possui pedidos.")
        return
    if response.status_code != 200:
        log_error("Não foi possível recuperar os pedidos.")
        print("\nNão foi possível recuperar os pedidos.")
        return

    pedidos = response.json()
    if not pedidos:
        print("\nVocê ainda não possui pedidos.")
        return

    print("\nSeus pedidos:")
    for pedido in pedidos:
        response = requests.get(f"http://localhost:8000/eventos/{pedido['id_evento']}", verify=False)
        if response.status_code != 200:
            log_error("Erro ao buscar detalhes do evento.")
            print("\nErro ao buscar detalhes do evento.")
            return
        evento = response.json()
        print(f"\nPedido ID: {pedido['id_pedido']}")
        print(f"Evento: {evento['nome']} | Setor: {pedido['setor']}")
        print(f"Ingressos: {pedido['quantidade_ingressos']} | Total: R${pedido['valor_total']:.2f}")
        print(f"Status: {pedido['status']} | Válido até: {pedido['reservado_ate']}")
        if pedido["setor"].lower() in ["cadeira inferior", "cadeira superior"]:
            print(f"Cadeiras: {pedido['cadeira']}")
    pedidos_reservados = [pedido for pedido in pedidos if pedido['status'] == 'reservado']
    if pedidos_reservados:
        menu_pagamento_pedidos_reservados(pedidos_reservados)


def menu_pagamento_pedidos_reservados(pedidos_reservados):
    while True:
        usuario_id = pedidos_reservados[0]['id_usuario'] if pedidos_reservados else None
        if usuario_id:
            response = requests.get(f"http://localhost:8000/pedidos/{usuario_id}/usuarios", verify=False)
            if response.status_code == 200:
                pedidos = response.json()
                pedidos_reservados = [pedido for pedido in pedidos if pedido['status'] == 'reservado']
            else:
                log_error("Não foi possível atualizar a lista de pedidos.")
                print("\nNão foi possível atualizar a lista de pedidos.")
                break

        if not pedidos_reservados:
            print("\nNenhum pedido reservado de pagamento.")
            break

        print("\nPedidos reservados aguardando pagamento:")
        for pedido in pedidos_reservados:
            evento_resp = requests.get(f"http://localhost:8000/eventos/{pedido['id_evento']}", verify=False)
            nome_evento = evento_resp.json()['nome'] if evento_resp.status_code == 200 else f"Evento {pedido['id_evento']}"

            print(f"\nPedido ID: {pedido['id_pedido']} | Evento: {nome_evento}")
            print(f"Setor: {pedido['setor']}")
            print(f"Ingressos: {pedido['quantidade_ingressos']}")
            print(f"Total: R${pedido['valor_total']:.2f}")
            if pedido["setor"].lower() in ["cadeira inferior", "cadeira superior"]:
                print(f"Cadeiras: {pedido['cadeira']}")

            produtos_resp = requests.get(f"http://localhost:8000/pedidos/{pedido['id_pedido']}/produtos", verify=False)
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
            if any(pedido['id_pedido'] == id_pedido for pedido in pedidos_reservados):
                finalizar_pagamento(id_pedido)
                
                response = requests.get(f"http://localhost:8000/pedidos/{usuario_id}/usuarios", verify=False)
                if response.status_code == 200:
                    pedidos = response.json()
                    pedidos_reservados = [pedido for pedido in pedidos if pedido['status'] == 'reservado']
                    if not pedidos_reservados:
                        print("\nNenhum pedido reservado de pagamento.")
                        break
                else:
                    log_error("Não foi possível atualizar a lista de pedidos.")
                    print("\nNão foi possível atualizar a lista de pedidos.")
                    break
            else:
                print("ID inválido.")
        except Exception as e:
            log_error(f"Entrada inválida: {e}")
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
    response = requests.post("http://localhost:8000/pagamentos/mock", verify=False)
    data = response.json()
    status_pagamento = "aprovado" if response.status_code == 200 and isinstance(data, dict) and data.get("status") == "aprovado" else "recusado"

    pedido_resp = requests.get(f"http://localhost:8000/pedidos/{id_pedido}", verify=False)
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
        }, 
        verify=False
    )
    if status_pagamento == "aprovado" and response.status_code == 201:
        log_info(f"Pagamento aprovado para pedido {id_pedido}")
        print("Pagamento aprovado! Sua compra está confirmada.")
    elif status_pagamento == "recusado":
        log_error(f"Pagamento recusado para pedido {id_pedido}")
        print("Pagamento recusado pelo banco. Tente novamente.")
    else:
        log_error(f"Erro ao registrar pagamento no sistema para pedido {id_pedido}")
        print("Erro ao registrar pagamento no sistema.")