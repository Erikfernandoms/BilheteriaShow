import time

class CircuitBreaker:
    def __init__(self, falhas_max=3, timeout=60):
        self.falhas_max = falhas_max
        self.timeout = timeout
        self.falhas = 0
        self.aberto = False
        self.ultima_falha = None

    def permitir_execucao(self):
        if not self.aberto:
            return True
        if time.time() - self.ultima_falha > self.timeout:
            self.aberto = False
            self.falhas = 0
            return True
        return False

    def registrar_falha(self):
        self.falhas += 1
        if self.falhas >= self.falhas_max:
            self.aberto = True
            self.ultima_falha = time.time()

    def resetar(self):
        self.falhas = 0
        self.aberto = False
        self.ultima_falha = None

circuito_pagamento = CircuitBreaker()