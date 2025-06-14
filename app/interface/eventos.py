import requests
from app.interface.pedido import reserva_ingresso
from app.interface.pedido import listar_pedidos


def menu_eventos(usuario_logado):
    response = requests.get("http://localhost:8000/eventos/")
    if response.status_code == 200:
        eventos = response.json()
        if not eventos:
            print("\nNenhum evento encontrado.")
            return
        print("\n=== EVENTOS ===")
        for evento in eventos:
            print("\n--------------------")
            print(f"ID: {evento['id_evento']}")
            print(f"Nome: {evento['nome']}")
            print(f"Descrição: {evento['descricao']}")
            print(f"Data: {evento['data']}")
            print(f"Local: {evento['local']}")

        print("\n--------------------")
        print("1. Ver meus pedidos")
        print("2. Deseja comprar um ingresso para algum evento?")

        escolha = input("Escolha uma opção: ")
        if escolha.lower() == '1':
            if usuario_logado:
                listar_pedidos(usuario_logado)
            else:
                print("\nVocê precisa estar logado para ver seus pedidos.")
        elif escolha.lower() == '2':
            if usuario_logado:
                evento_id = input(f"\nOlá, {usuario_logado['nome']}! Digite o ID do evento que deseja comprar ingresso: ")
                response = requests.get(f"http://localhost:8000/eventos/{evento_id}")
                if response.status_code == 200: 
                    evento = response.json()
                menu_setores(evento_id, evento, usuario_logado)
            else:
                print("\nVocê precisa estar logado para comprar ingressos.")
        else:
            print("\nOpção inválida. Tente novamente.")
        return
    else:
        print("\nErro ao buscar eventos. Tente novamente.")
  



def menu_setores(evento_id, evento, usuario_logado):
    response = requests.get(f"http://localhost:8000/eventos/setores/{evento_id}")
    if response.status_code != 200:
        print("\nErro ao buscar setores do evento. Tente novamente.")
        return

    setores_eventos = response.json()
    if not setores_eventos:
        print("\nNenhum setor de evento encontrado.")
        return

    setor = escolher_setor(setores_eventos, evento)
    if not setor:
        return

    quantidade = escolher_quantidade(setor)
    if quantidade is None:
        return

    reserva_ingresso(usuario_logado, evento, setor, quantidade)


def escolher_setor(setores, evento):
    print(f"\n=== SETORES DO EVENTO: {evento['nome']} ===")
    setores_disponiveis = [s for s in setores if s['quantidade_lugares'] > 0]

    if not setores_disponiveis:
        print("\nTodos os setores estão esgotados.")
        return None

    for setor in setores_disponiveis:
        print("\n--------------------")
        print(f"ID: {setor['id_setor_evento']}")
        print(f"Nome: {setor['nome']}")
        print(f"Quantidade de lugares: {setor['quantidade_lugares']}")
        print(f"Preço base: R$ {setor['preco_base']:.2f}")

    ids_validos = [str(s['id_setor_evento']) for s in setores_disponiveis]

    while True:
        setor_id = input("\nDigite o ID do setor que deseja comprar ingresso (ou 'voltar' para cancelar): ")
        if setor_id.lower() == "voltar":
            return None
        if setor_id not in ids_validos:
            print("Setor inválido. Tente novamente.")
            continue
        # Busca o setor na lista local, não na API
        setor = next(s for s in setores_disponiveis if str(s['id_setor_evento']) == setor_id)
        print(f"\nSetor selecionado: {setor['nome']}")
        return setor


def escolher_quantidade(setor):
    while True:
        quantidade = input("Digite a quantidade de ingressos (máx. 3): ")
        if not quantidade.isdigit():
            print("Digite um número válido.")
            continue

        quantidade = int(quantidade)
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
        elif quantidade > 3:
            print("Limite de 3 ingressos por compra.")
        elif quantidade > setor['quantidade_lugares']:
            print("Não há ingressos suficientes disponíveis.")
        else:
            return quantidade
    