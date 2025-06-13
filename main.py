#app.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])
import requests
from app.repository.init_db import init_db
import sys

init_db()
usuario_logado = None

def menu_principal():
    while True:
        print("\n=== SISTEMA DE BILHETAGEM ===")
        print("1 - Conta")
        print("2 - Ver eventos")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            if usuario_logado:
                menu_conta()
            else:
                print("\n=== LOGIN ===")
                print("1 - Entrar")
                print("2 - Criar conta")
                input_escolha = input("Escolha uma opção: ")
                if input_escolha == "1":
                    if usuario_logado:
                        print("Você já está logado.")
                    else:
                        login()
                elif input_escolha == "2":
                    cadastrar_usuario()
                else:
                    print("Opção inválida. Tente novamente.")
        elif escolha == "2":
            if usuario_logado:
                ver_eventos()
            else:
                print("⚠️ Você precisa estar logado para ver os eventos.")
        elif escolha == "3":
            print("Saindo...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")


def menu_conta():
    print("\n=== MENU DE CONTA ===")
    print(f"Nome: {usuario_logado['nome']}")
    print(f"Email: {usuario_logado['email']}")
    print(f"CPF: {usuario_logado['cpf']}")
    print(f"Telefone: {usuario_logado['telefone']}")
    print(f"CEP: {usuario_logado['cep']}")
    print("1 - Atualizar conta")
    print("2 - Deletar conta")
    print("3 - Voltar ao menu principal")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        atualizar_conta()
    elif escolha == "2":
        deletar_conta()
    elif escolha == "3":
        return
    else:
        print("Opção inválida. Tente novamente.")


def atualizar_conta():
    global usuario_logado
    print("\n=== ATUALIZAR CONTA ===")
    print("Deixe o campo vazio se não quiser alterar.")
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
        print("✅ Conta atualizada com sucesso!")
        usuario_logado = response.json()
        return
    else:
        print("❌ Erro ao atualizar conta. Tente novamente.")
        return

def deletar_conta():
    global usuario_logado
    id = usuario_logado["id_usuario"]
    response = requests.delete(f"http://localhost:8000/usuarios/{id}")
    if response.status_code == 200:
        print("✅ Conta deletada com sucesso!")
        usuario_logado = None
        return
    else:
        print("❌ Erro ao deletar conta. Tente novamente.")
        return

def login():
    global usuario_logado
    email = input("Digite o seu email: ")
    
    response = requests.get("http://localhost:8000/usuarios/"+email)
    if response.status_code == 200:
        usuarios = response.json()
        senha = input("Digite a sua senha: ")
        if senha != usuarios["senha"]:
            print("❌ Senha incorreta.")
            return
        else:
            nome = usuarios["nome"]
            print(f"✅ Bem-vindo, {nome}!")
            usuario_logado = usuarios
            return
    else:
        print("❌ Usuário não encontrado.")
        return
    
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
        print("✅ Conta criada com sucesso!")
        return
    else:
        print("❌ Erro ao criar conta. Verifique os dados e tente novamente.")
        return

def ver_eventos():
    pass
  

if __name__ == "__main__":
    menu_principal()
