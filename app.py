import streamlit as st
import duckdb
from datetime import datetime

# Função para conectar ao banco DuckDB
@st.cache_resource
def get_conexao():
    return duckdb.connect('ingressos.duckdb')

def listar_eventos(conn):
    return conn.execute("SELECT id, nome, data, local FROM eventos ORDER BY data").fetchall()

def listar_ingressos_por_evento(conn, evento_id):
    return conn.execute("""
        SELECT id, tipo, preco, quantidade_disponivel
        FROM ingressos
        WHERE evento_id = ?
        AND quantidade_disponivel > 0
    """, [evento_id]).fetchall()

def registrar_pedido(conn, ingresso_id, quantidade, total):
    # Atualiza a quantidade disponível
    conn.execute("""
        UPDATE ingressos
        SET quantidade_disponivel = quantidade_disponivel - ?
        WHERE id = ? AND quantidade_disponivel >= ?
    """, [quantidade, ingresso_id, quantidade])
    # Insere o pedido
    conn.execute("""
        INSERT INTO pedidos (ingresso_id, quantidade, total_pago)
        VALUES (?, ?, ?)
    """, [ingresso_id, quantidade, total])

def main():
    st.title("Compra de Ingressos - Exemplo Didático")

    conn = get_conexao()

    eventos = listar_eventos(conn)
    if not eventos:
        st.warning("Nenhum evento disponível no momento.")
        return

    evento_selecionado = st.selectbox("Selecione o evento", options=eventos, format_func=lambda e: f"{e[1]} - {e[2]} - {e[3]}")

    ingressos = listar_ingressos_por_evento(conn, evento_selecionado[0])
    if not ingressos:
        st.warning("Nenhum ingresso disponível para este evento.")
        return

    ingresso_selecionado = st.selectbox(
        "Selecione o tipo de ingresso",
        options=ingressos,
        format_func=lambda i: f"{i[1]} - R$ {i[2]:.2f} - Disponível: {i[3]}"
    )

    quantidade = st.number_input("Quantidade", min_value=1, max_value=ingresso_selecionado[3], step=1)

    total = ingresso_selecionado[2] * quantidade
    st.write(f"Total a pagar: R$ {total:.2f}")

    if st.button("Comprar"):
        if quantidade <= ingresso_selecionado[3]:
            registrar_pedido(conn, ingresso_selecionado[0], quantidade, total)
            st.success(f"Compra realizada com sucesso! Você comprou {quantidade} ingresso(s) do tipo {ingresso_selecionado[1]}.")
        else:
            st.error("Quantidade solicitada maior que a disponível.")

if __name__ == "__main__":
    main()
