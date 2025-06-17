from app.interface.usuarios import menu_conta
from app.interface.eventos import menu_eventos
from app.interface.usuarios import cadastrar_usuario

from app.interface.usuarios import login
from database.init_db import init_db
import sys
import os
from threading import Thread
from app.jobs.limpeza import rotina_limpeza_pedidos  # se salvar num módulo separado

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

sys.stdout.reconfigure(encoding="utf-8")


def menu_principal(usuario_logado):
    init_db()
    """
    Rotina que limpa registros de pedidos expirados, está desativado por limitação do banco de dados SQLite!
    """
    limpador = Thread(target=rotina_limpeza_pedidos, daemon=True)
    limpador.start()

    while True:
        print("\n=== SISTEMA DE BILHETAGEM ===")
        print("\n1 - Conta")
        print("2 - Eventos")
        print("3 - Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            if usuario_logado:
                usuario_logado = menu_conta(usuario_logado)
            else:
                print("\n=== LOGIN ===")
                print("1 - Entrar")
                print("2 - Criar conta")
                input_escolha = input("\nEscolha uma opção: ")
                if input_escolha == "1":
                    if usuario_logado:
                        print("\nVocê já está logado.")
                    else:
                        usuario_logado = login()
                elif input_escolha == "2":
                    usuario_logado = cadastrar_usuario()
                else:
                    print("\nOpção inválida. Tente novamente.")
        elif escolha == "2":
            menu_eventos(usuario_logado)
        elif escolha == "3":
            print("\nSaindo...")
            sys.exit()
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    usuario_logado = None
    menu_principal(usuario_logado)
