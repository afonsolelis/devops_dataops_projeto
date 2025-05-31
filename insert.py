import duckdb

def inserir_dados_mockados():
    conn = duckdb.connect('ingressos.duckdb')

    # Inserir eventos mockados
    eventos = [
        (3, 'Festival de Jazz', 'Jazz ao vivo com artistas renomados', '2025-09-10', 'Parque Central'),
        (4, 'Stand-up Comedy', 'Noite de risadas com comediantes famosos', '2025-07-20', 'Teatro Municipal'),
        (5, 'Show de Música Eletrônica', 'Festa com DJs internacionais', '2025-10-05', 'Clube Noturno XYZ')
    ]
    conn.executemany("""
        INSERT OR IGNORE INTO eventos (id, nome, descricao, data, local)
        VALUES (?, ?, ?, ?, ?)
    """, eventos)

    # Inserir ingressos mockados
    ingressos = [
        (4, 3, 'Ingresso Normal', 120.0, 200),
        (5, 3, 'Ingresso VIP', 300.0, 50),
        (6, 4, 'Entrada Única', 80.0, 150),
        (7, 5, 'Pista', 100.0, 300),
        (8, 5, 'Área VIP', 250.0, 100)
    ]
    conn.executemany("""
        INSERT OR IGNORE INTO ingressos (id, evento_id, tipo, preco, quantidade_disponivel)
        VALUES (?, ?, ?, ?, ?)
    """, ingressos)

    conn.close()
    print("Dados mockados inseridos com sucesso.")

if __name__ == "__main__":
    inserir_dados_mockados()
