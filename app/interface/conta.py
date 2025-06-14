import requests

def menu_conta(usuario_logado):
    print("\n=== MENU DE CONTA ===")
    print(f"\nNome: {usuario_logado['nome']}")
    print(f"Email: {usuario_logado['email']}")
    print(f"CPF: {usuario_logado['cpf']}")
    print(f"Telefone: {usuario_logado['telefone']}")
    print(f"CEP: {usuario_logado['cep']}")
    print("\n1 - Atualizar conta")
    print("2 - Deletar conta")
    print("3 - Voltar ao menu principal")
    escolha = input("\nEscolha uma opção: ")


    if escolha == "1":
        usuario_logado = atualizar_conta(usuario_logado)
    elif escolha == "2":
        usuario_logado = deletar_conta(usuario_logado)
    elif escolha == "3":
        return usuario_logado
    else:
        print("\nOpção inválida. Tente novamente.")
    
    return usuario_logado


def login():
    email = input("\nDigite o seu email: ")
    
    response = requests.get("http://localhost:8000/usuarios/"+email)
    if response.status_code == 200:
        usuarios = response.json()
        senha = input("\nDigite a sua senha: ")
        if senha != usuarios["senha"]:
            print("❌ Senha incorreta.")
            return
        else:
            nome = usuarios["nome"]
            print(f"\nBem-vindo, {nome}!")
            usuario_logado = usuarios
            return usuario_logado
    else:
        print("\nUsuário não encontrado.")
        return 


def atualizar_conta(usuario_logado):
    print("\n=== ATUALIZAR CONTA ===")
    print("\nDeixe o campo vazio se não quiser alterar.")
    nome = input(f"Nome ({usuario_logado['nome']}): ") or usuario_logado['nome']
    email = input(f"Email ({usuario_logado['email']}): ") or usuario_logado['email']
    senha = input(f"Senha ({usuario_logado['senha']}): ") or usuario_logado['senha']
    cpf = input(f"CPF ({usuario_logado['cpf']}): ") or usuario_logado['cpf']
    telefone = input(f"Telefone ({usuario_logado['telefone']}): ") or usuario_logado['telefone']
    cep = input(f"CEP ({usuario_logado['cep']}): ") or usuario_logado['cep']
    usuario_logado_alterado = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cpf": cpf,
        "telefone": telefone,
        "cep": cep
    }
    id = usuario_logado["id_usuario"]
    response = requests.put(f"http://localhost:8000/usuarios/{id}", json=usuario_logado_alterado)
    if response.status_code == 200:
        print("\nConta atualizada com sucesso!")
        usuario_logado = response.json()
        return usuario_logado
    else:
        print("\nErro ao atualizar conta. Tente novamente.")
        return usuario_logado


def deletar_conta(usuario_logado):
    id = usuario_logado["id_usuario"]
    response = requests.delete(f"http://localhost:8000/usuarios/{id}")
    if response.status_code == 200:
        print("\nConta deletada com sucesso!")
        usuario_logado = None
        return usuario_logado
    else:
        print("\nErro ao deletar conta. Tente novamente.")
        return usuario_logado


def cadastrar_usuario():
    nome = input("Digite o seu nome: ")
    email = input("Digite o seu email: ")
    senha = input("Digite a sua senha: ")
    cpf = input("Digite o seu CPF: ")
    telefone = input("Digite o seu telefone: ")
    cep = input("Digite o seu CEP: ")


    usuario_data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "cpf": cpf,
        "telefone": telefone,
        "cep": cep
    }


    response = requests.post("http://localhost:8000/usuarios/", json=usuario_data)
    

    if response.status_code in (201, 200):
        print("\nConta criada com sucesso!")
        return
    else:
        print("\nErro ao criar conta. Verifique os dados e tente novamente.")
        return
