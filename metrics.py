
import json
import os

METRICS_FILE = "logs/metrics.json"

def _carregar():
    if not os.path.exists(METRICS_FILE):
        return {}
    with open(METRICS_FILE) as f:
        return json.load(f)

def _salvar(dados):
    with open(METRICS_FILE, "w") as f:
        json.dump(dados, f, indent=2)

def incrementar_metrica(nome):
    dados = _carregar()
    dados[nome] = dados.get(nome, 0) + 1
    _salvar(dados)

def registrar_valor(nome, valor):
    dados = _carregar()
    dados[nome] = valor
    _salvar(dados)

def obter_metricas():
    return _carregar()
