import random

def mock_pagamento_externo():
    if random.random() < 0.9:
        return {"status": "aprovado"}
    return {"status": "recusado"}