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


def login():
    global usuario_logado
    email = input("Digite o seu email: ")
    
    response = requests.get("http://localhost:8000/usuarios/"+email)
    if response.status_code == 200:
        usuarios = response.json()
        print("Digite a sua senha:")
        senha = input("Senha: ")
        if senha != usuarios["senha"]:
            print("❌ Senha incorreta.")
            return
        else:
            nome = usuarios["nome"]
            print(f"✅ Bem-vindo, {nome}!")
            usuario_logado = usuarios  # Aqui salva o usuário logado!
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
