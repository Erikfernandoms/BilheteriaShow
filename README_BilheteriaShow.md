
# 🎟️ BilheteriaShow – Sistema de Bilhetagem via Terminal

Este projeto é a entrega do **case técnico para vaga de Engenheiro de Software Sênior no Itaú Unibanco**, onde foi solicitado o desenvolvimento de um sistema de bilhetagem funcional, utilizando arquitetura em AWS como referência e implementado em uma stack de escolha livre.

---

## 🧱 Arquitetura e Estrutura

A aplicação foi modelada com uma arquitetura modular, simulando uma API de microserviços e uma interface via terminal, atuando como frontend simulador.

```
BilheteriaShow/
│
├── app/                  # Lógica do sistema
│   ├── controllers/      # Regras de negócio (pedidos, eventos, produtos, etc)
│   ├── interface/        # Interface de usuário via terminal
│   ├── models/           # Criação do banco e tabelas
│   └── rotina/           # Ações automáticas, como expiração de pedidos
│
├── database/             # Conexão SQLite
├── logger.py             # Log das operações
├── main.py               # Interface principal de navegação (CLI)
├── run.py                # Alternativa de execução ao main
├── metrics.py            # Coleta de métricas de uso
├── notas_fiscais/        # Simulação da geração de NF
├── requirements.txt      # Dependências Python
└── bilhetagem.db         # Banco SQLite local (gerado automaticamente)
```

---

## 🚀 Como Executar

### 1. Clone o projeto
```bash
git clone https://github.com/seu-usuario/BilheteriaShow.git
cd BilheteriaShow
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o sistema
```bash
python main.py
```

---

## 🧠 Funcionalidades

- Autenticação de usuários (simples via ID e nome)
- Listagem de eventos e setores
- Reserva temporária de ingressos (15 minutos)
- Adição de produtos adicionais à compra (ex: pipoca, refrigerante)
- Geração de pedidos com persistência
- Expiração automática de reservas não finalizadas
- Visualização de pedidos
- Emissão de notas fiscais (simulada)
- Coleta de métricas de uso (acessos a setores, pedidos por status)

---

## 🛠️ Diferenciais Técnicos

- Interface `CLI` simulando frontend real
- Uso de **SQLite puro via `sqlite3`**, sem ORMs
- **Concorrência controlada** na reserva de ingressos com transações
- **Thread background** para limpeza de pedidos expirados
- Modularização clara entre controle, interface e banco
- Arquitetura facilmente portável para um backend FastAPI real

---

## 📌 Considerações

- A ausência de autenticação JWT e interface gráfica foram escolhas intencionais para foco na lógica de negócio.
- A arquitetura AWS foi proposta paralelamente ao código, conforme instruções do case (não é parte da execução local).
- Todo o código simula um comportamento real de microserviços e API Gateway por meio de organização de módulos.

---

## ✅ Exemplo de uso (terminal)

```bash
🎟️ Bem-vindo ao BilheteriaShow!

[1] Entrar com minha conta
[2] Sair

🧍 Nome: Bruno
📋 Eventos disponíveis:
1. Show do Legado
2. Festival Verão

🎟️ Setores disponíveis:
1. Pista Comum
2. Camarote - Superior

🔒 Reservando 2 ingressos...
💬 Deseja adicionar produtos extras?

[1] Sim        [2] Não
...
```

---

## ✍️ Autor

**Bruno Jovenasso**  
Desenvolvedor e Engenheiro de Software  
📧 contato@exemplo.com.br | 🔗 linkedin.com/in/brunojovenasso

