import requests
import bcrypt
from logger import log_info, log_error

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
    
    response = requests.get("http://localhost:8000/usuarios/"+email, verify=False)
    if response.status_code == 200:
        usuarios = response.json()
        senha = input("\nDigite a sua senha: ")
        senha_hash = usuarios["senha"]
        if not bcrypt.checkpw(senha.encode(), senha_hash.encode()):
            print("❌ Senha incorreta.")
            return
        else:
            nome = usuarios["nome"]
            print(f"\nBem-vindo, {nome}!")
            usuario_logado = usuarios
            log_info(f"Usuário {nome} ({email}) logado com sucesso.")
            return usuario_logado
    else:
        print("\nUsuário não encontrado.")
        return 


def atualizar_conta(usuario_logado):
    print("\n=== ATUALIZAR CONTA ===")
    print("\nDeixe o campo vazio se não quiser alterar.")
    nome = input(f"Nome ({usuario_logado['nome']}): ") or usuario_logado['nome']
    email = input(f"Email ({usuario_logado['email']}): ") or usuario_logado['email']
    senha = input(f"Senha (deixe em branco para manter): ")
    if senha:
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    else:
        senha_hash = usuario_logado['senha']
    cpf = input(f"CPF ({usuario_logado['cpf']}): ") or usuario_logado['cpf']
    telefone = input(f"Telefone ({usuario_logado['telefone']}): ") or usuario_logado['telefone']
    cep = input(f"CEP ({usuario_logado['cep']}): ") or usuario_logado['cep']
    usuario_logado_alterado = {
        "nome": nome,
        "email": email,
        "senha": senha_hash,
        "cpf": cpf,
        "telefone": telefone,
        "cep": cep
    }
    id = usuario_logado["id_usuario"]
    response = requests.put(f"http://localhost:8000/usuarios/{id}", json=usuario_logado_alterado, verify=False)
    if response.status_code == 200:
        print("\nConta atualizada com sucesso!")
        usuario_logado = response.json()
        log_info(f"Conta do usuário {nome} atualizada com sucesso.")
        return usuario_logado
    else:
        print("\nErro ao atualizar conta. Tente novamente.")
        return usuario_logado


def deletar_conta(usuario_logado):
    id = usuario_logado["id_usuario"]
    response = requests.delete(f"http://localhost:8000/usuarios/{id}", verify=False)
    if response.status_code == 200:
        print("\nConta deletada com sucesso!")
        log_info(f"Conta do usuário {usuario_logado['nome']} deletada com sucesso.")
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

    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    usuario_data = {
        "nome": nome,
        "email": email,
        "senha": senha_hash,
        "cpf": cpf,
        "telefone": telefone,
        "cep": cep
    }
    def cpf_valido(cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))
        return len(cpf) == 11
    
    if not cpf_valido(cpf):
        print("❌ CPF inválido. Digite 11 números com ou sem máscara.")
        return

    response = requests.post("http://localhost:8000/usuarios/", json=usuario_data, verify=False)
    if response.status_code in (201, 200):
        print("\nConta criada com sucesso!")
        log_info(f"Usuário {nome} ({email}) cadastrado com sucesso.")
        return
    else:
        try:
            erro = response.json()
            if "cpf" in erro.get("detail", "").lower():
                print("\nJá existe uma conta cadastrada com esse CPF.")
            else:
                print(f"\nErro ao criar conta: {erro.get('detail', 'Verifique os dados e tente novamente.')}")
        except Exception:
            print("\nErro ao criar conta. Verifique os dados e tente novamente.")
        return
