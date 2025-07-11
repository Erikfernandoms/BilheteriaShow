import requests

def oferecer_produtos(pedido_id, id_evento):
    response = requests.get(f"http://localhost:8000/produtos/eventos/{id_evento}/produtos", verify=False)
    if response.status_code != 200:
        print("\nNão foi possível recuperar os produtos.")
        return

    produtos = response.json()
    if not produtos:
        print("\nNenhum produto adicional disponível.")
        return

    print("\nProdutos adicionais disponíveis:")
    for idx, produto in enumerate(produtos, 1):
        status = "Ativo" if produto["ativo"] else "Indisponível"
        print(f"{idx} - {produto['nome']} | R${produto['preco']:.2f} | Estoque: {produto['estoque_disponivel']} | {status}")

    while True:
        escolha = input("\nDigite o número do produto para adicionar ao pedido (ou ENTER para pular): ")
        if not escolha:
            break
        if not escolha.isdigit() or not (1 <= int(escolha) <= len(produtos)):
            print("Opção inválida.")
            continue
        idx = int(escolha) - 1
        produto = produtos[idx]
        if not produto["ativo"] or produto["estoque_disponivel"] <= 0:
            print("Produto indisponível no momento.")
            continue
        try:
            qtd = int(input(f"Quantidade de '{produto['nome']}' para adicionar: "))
        except Exception:
            print("Entrada inválida.")
            continue
        if qtd <= 0:
            print("Quantidade inválida.")
            continue
        if qtd > produto["estoque_disponivel"]:
            print(f"Quantidade solicitada ({qtd}) excede o estoque disponível ({produto['estoque_disponivel']}).")
            continue
        reponse = requests.post(
            f"http://localhost:8000/produtos/{pedido_id}/produtos",
            json={"id_produto": produto["id_produto"], "quantidade": qtd},
            verify=False
        )
        if reponse.status_code in (200, 201):
            print(f"Produto '{produto['nome']}' adicionado ao pedido!")
        else:
            print("Erro ao adicionar produto ao pedido.")