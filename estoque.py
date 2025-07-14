import streamlit as st
from pymongo import MongoClient
from datetime import datetime

st.title("Movimentação de Estoque")

# Conectar ao MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
colecao_produtos = db["produtos"]
colecao_estoque = db["estoque"]

# Obter SKUs disponíveis
skus = [doc["SKU"] for doc in colecao_produtos.find({}, {"SKU": 1, "_id": 0})]

# Formulário
with st.form("form_estoque"):
    sku = st.selectbox("Selecione o produto (SKU)", skus)
    motivo = st.selectbox("Motivo da movimentação", ["Compra", "Devolução", "Pedido Cancelado"])
    quantidade = st.number_input("Quantidade", step=1, min_value=1)
    data = st.date_input("Data da movimentação", value=datetime.today())
    responsavel = st.text_input("Responsável pela movimentação")

    enviar = st.form_submit_button("Registrar movimentação")

# Ao enviar o formulário
if enviar:
    ajuste = quantidade


    # Registrar movimentação na coleção estoque (histórico)
    nova_movimentacao = {
        "SKU": sku,
        "Motivo": motivo,
        "Quantidade": ajuste,
        "Data": data.strftime("%Y-%m-%d"),
        "Responsável": responsavel
    }

    colecao_estoque.insert_one(nova_movimentacao)

        # Atualizar estoque (entrada ou saída com base no ajuste)
    colecao_produtos.update_one(
        {"SKU": sku},
        {"$inc": {"Qtd_estoque": ajuste}}
    )

    st.success(f"Movimentação registrada com sucesso. Foi adicionado ao Estoque {ajuste} unidade(s) .")

