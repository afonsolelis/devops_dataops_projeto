import duckdb

def criar_tabelas():
    conn = duckdb.connect('ingressos.duckdb')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY,
            nome VARCHAR,
            descricao VARCHAR,
            data DATE,
            local VARCHAR
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingressos (
            id INTEGER PRIMARY KEY,
            evento_id INTEGER,
            tipo VARCHAR,
            preco FLOAT,
            quantidade_disponivel INTEGER,
            FOREIGN KEY (evento_id) REFERENCES eventos(id)
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingresso_id INTEGER,
            quantidade INTEGER,
            total_pago FLOAT,
            data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ingresso_id) REFERENCES ingressos(id)
        );
    """)

    # Inserir alguns dados de exemplo
    conn.execute("INSERT OR IGNORE INTO eventos VALUES (1, 'Show de Rock', 'Banda famosa ao vivo', '2025-07-15', 'Arena XYZ');")
    conn.execute("INSERT OR IGNORE INTO eventos VALUES (2, 'Peça de Teatro', 'Drama emocionante', '2025-08-01', 'Teatro ABC');")

    conn.execute("INSERT OR IGNORE INTO ingressos VALUES (1, 1, 'Pista', 150.0, 100);")
    conn.execute("INSERT OR IGNORE INTO ingressos VALUES (2, 1, 'Camarote', 300.0, 50);")
    conn.execute("INSERT OR IGNORE INTO ingressos VALUES (3, 2, 'Plateia', 80.0, 120);")

    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas e dados inseridos com sucesso.")
