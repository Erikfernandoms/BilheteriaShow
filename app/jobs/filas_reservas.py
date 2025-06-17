from queue import Queue
from app.interface.pedido import reserva_ingresso

fila_reservas = Queue()

def consumir_reservas():
    while True:
        try:
            usuario_logado, evento, setor, quantidade = fila_reservas.get()
            reserva_ingresso(usuario_logado, evento, setor, quantidade)
        except Exception as e:
            print(f"Erro ao processar reserva: {e}")