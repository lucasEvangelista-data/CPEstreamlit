import streamlit as st
from pymongo import MongoClient

# Conectar ao MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
colecao_produtos = db["produtos"]

# Buscar produtos com estoque baixo
estoque_baixo = list(colecao_produtos.find({"Qtd_estoque": {"$lt": 5}}))

# Exibir alerta se houver produtos com estoque crítico
if estoque_baixo:
    st.warning(f"⚠️ Atenção: {len(estoque_baixo)} produto(s) com estoque abaixo de 5 unidades.")
    with st.expander("Ver produtos com estoque baixo"):
        for produto in estoque_baixo:
            st.write(f"• {produto['Título']} — {produto['Qtd_estoque']} unidades")

st.title ("Controle de Estoque e Pedidos")

coluna_esquerda, coluna_direita = st.columns([1, 1.5])

coluna_esquerda.write ("#### Bem vindo, Erick")

botao_dashboard = coluna_esquerda.button("Dashboard")
botao_produtos = coluna_esquerda.button("Tabela Produtos")
botao_estoque = coluna_esquerda.button("Movimentação estoque")
botao_chatbot = coluna_esquerda.button("Tirar duvidas com chatbot")

if botao_dashboard:
    st.switch_page("dashboard.py")
if botao_produtos:
    st.switch_page("produtos.py")
if botao_estoque:
    st.switch_page("movimenta_estoque.py")
if botao_chatbot:
    st.switch_page("chatbot.py")

container = coluna_direita.container(border=True)
container.image("E.png")    