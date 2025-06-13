import sqlite3




def init_db():
    conn = sqlite3.connect("bilhetagem.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        CPF VARCHAR(11) UNIQUE NOT NULL,
        senha VARCHAR(100) NOT NULL,
        telefone VARCHAR(15) NOT NULL,
        cep VARCHAR(10) NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evento (
        id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
        nome  VARCHAR(100) NOT NULL,
        descricao TEXT NOT NULL,
        local VARCHAR(100) NOT NULL,
        data TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Dados iniciais
    cursor.execute("INSERT OR IGNORE INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Show do Coldplay", "O maior show das americas", "Morumbi", "2025-12-10"))
    cursor.execute("INSERT OR IGNORE INTO evento (nome, descricao, local, data) VALUES (?, ?, ?, ?)", ("Rock in Rio", "Venha sentir essa experiência!", "Rio de Janeiro", "2025-09-20"))

    conn.commit()
    conn.close()
    print("Banco de dados criado e populado com sucesso.")
