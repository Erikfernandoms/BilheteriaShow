import time
import sqlite3
from app.controllers.pedidos.pedidos_service import cancelar_reservas_expiradas

    
def rotina_limpeza_pedidos():
    conn = sqlite3.connect("bilhetagem.db")
    while True:
        cancelar_reservas_expiradas(conn)
        time.sleep(60)