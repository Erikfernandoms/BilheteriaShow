import time
import sqlite3
from app.controllers.pedidos.pedidos_service import cancelar_reservas_expiradas

    
def rotina_limpeza_pedidos():
    while True:
        try:
            conn = sqlite3.connect("bilhetagem.db", timeout=30, check_same_thread=False)
            cancelar_reservas_expiradas(conn)
            conn.close()
        except sqlite3.OperationalError as e:
            print(f"Erro de banco de dados na rotina de limpeza: {e}")
        time.sleep(60)