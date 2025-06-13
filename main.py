#app.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])
import requests
from app.repository.init_db import init_db
import sys

init_db()
usuario_logado = None

def menu_principal():
    while True:
        print("\n=== SISTEMA DE BILHETAGEM ===")
        print("\n1 - Conta")
        print("2 - Eventos")
        print("3 - Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            if usuario_logado:
                menu_conta()
            else:
                print("\n=== LOGIN ===")
                print("1 - Entrar")
                print("2 - Criar conta")
                input_escolha = input("\nEscolha uma opção: ")
                if input_escolha == "1":
                    if usuario_logado:
                        print("\nVocê já está logado.")
                    else:
                        login()
                elif input_escolha == "2":
                    cadastrar_usuario()
                else:
                    print("\nOpção inválida. Tente novamente.")
        elif escolha == "2":
            eventos()
        elif escolha == "3":
            print("\nSaindo...")
            sys.exit()
        else:
            print("\nOpção inválida. Tente novamente.")


def menu_conta():
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
        atualizar_conta()
    elif escolha == "2":
        deletar_conta()
    elif escolha == "3":
        return
    else:
        print("\nOpção inválida. Tente novamente.")


def atualizar_conta():
    global usuario_logado
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
        print("\n✅ Conta atualizada com sucesso!")
        usuario_logado = response.json()
        return
    else:
        print("\n❌ Erro ao atualizar conta. Tente novamente.")
        return

def deletar_conta():
    global usuario_logado
    id = usuario_logado["id_usuario"]
    response = requests.delete(f"http://localhost:8000/usuarios/{id}")
    if response.status_code == 200:
        print("\n✅ Conta deletada com sucesso!")
        usuario_logado = None
        return
    else:
        print("\n❌ Erro ao deletar conta. Tente novamente.")
        return

def login():
    global usuario_logado
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
            print(f"\n✅ Bem-vindo, {nome}!")
            usuario_logado = usuarios
            return
    else:
        print("\n❌ Usuário não encontrado.")
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
        print("\n✅ Conta criada com sucesso!")
        return
    else:
        print("\n❌ Erro ao criar conta. Verifique os dados e tente novamente.")
        return

def eventos():
    global usuario_logado
    response = requests.get("http://localhost:8000/eventos/")
    if response.status_code == 200:
        eventos = response.json()
        if not eventos:
            print("\n⚠️ Nenhum evento encontrado.")
            return
        print("\n=== EVENTOS ===")
        for evento in eventos:
            print("\n--------------------")
            print(f"ID: {evento['id_evento']}")
            print(f"Nome: {evento['nome']}")
            print(f"Descrição: {evento['descricao']}")
            print(f"Data: {evento['data']}")
            print(f"Local: {evento['local']}")
        
        print("\nDeseja comprar um ingresso para algum evento?")
        escolha = input("Digite 's' para sim ou qualquer outra tecla para voltar: ")
        if escolha.lower() == 's':
            if usuario_logado:
                evento_id = input(f"\nOlá, {usuario_logado['nome']}! Digite o ID do evento que deseja comprar ingresso: ")
                response = requests.get(f"http://localhost:8000/eventos/{evento_id}")
                if response.status_code == 200: 
                    evento = response.json()
                menu_setores(evento_id, evento)
            else:
                print("\n⚠️ Você precisa estar logado para comprar ingressos.")
        return
    else:
        print("\n❌ Erro ao buscar eventos. Tente novamente.")
  

def menu_setores(evento_id, evento):
    response = requests.get(f"http://localhost:8000/eventos/setores/{evento_id}")
    if response.status_code == 200:
        setores_eventos = response.json()
        if not setores_eventos:
            print("\n⚠️ Nenhum setor de evento encontrado.")
            return
        print("\n=== SETORES DO EVENTO ===")
        for setor in setores_eventos:
            if setor['quantidade_lugares'] > 0:
                print("\n--------------------")
                print(f"Evento: {evento['nome']}")
                print("\n--------------------")
                print(f"ID: {setor['id_setor_evento']}")
                print(f"Nome: {setor['nome']}")
                print(f"Quantidade de lugares: {setor['quantidade_lugares']}")
                print(f"Preço base: R$ {setor['preco_base']:.2f}")
        while True:
            setor_id = input("\nDigite o ID do setor que deseja comprar ingresso: ")
            response = requests.get(f"http://localhost:8000/eventos/setor/{setor_id}")
            if response.status_code == 200:
                setor = response.json()
                print(f"\nVocê escolheu o setor: {setor['nome']}")
                print(f"Quantidade de lugares disponíveis: {setor['quantidade_lugares']}")
                break
            else:
                print("\n❌ Setor inválido. Tente novamente.")
        while True:
            quantidade = input("Digite a quantidade de ingressos que deseja comprar: ")
            if not quantidade.isdigit() or int(quantidade) <= 0:
                print("\n⚠️ Quantidade inválida. Deve ser maior que zero e numeral positivo.")
            else:
                if int(quantidade) > 2:
                    print("\n⚠️ Quantidade máxima de 2 ingressos por compra.")
                else:
                    quantidade = int(quantidade)
                    break

        reserva_ingresso(evento_id, setor_id, quantidade)
    else:
        print("\n❌ Erro ao buscar setores do evento. Tente novamente.")

def reserva_ingresso(evento_id, setor_id, quantidade):
    pass
    
if __name__ == "__main__":
    menu_principal()
