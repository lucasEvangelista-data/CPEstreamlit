import streamlit as st
from pymongo import MongoClient
from datetime import datetime

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


st.title("Cadastrar Pedido")

# Conectar ao MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
colecao_produtos = db["produtos"]
colecao_pedidos = db["pedidos"]

# Obter SKUs disponíveis
skus = [doc["SKU"] for doc in colecao_produtos.find({}, {"SKU": 1, "_id": 0})]

# Formulário
with st.form("form_pedido"):
    sku = st.selectbox("Produto (SKU)", skus)
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    descricao = st.text_input("Descrição")
    observacao = st.text_area("Observação")
    cliente = st.text_input("Cliente")
    status = "Pendente"
    data = st.date_input("Data do Pedido", value=datetime.today())
    
    enviar = st.form_submit_button("Cadastrar Pedido")

# Lógica ao enviar
if enviar:
    # Verifica estoque disponível
    produto = colecao_produtos.find_one({"SKU": sku})
    estoque_atual = produto.get("Qtd_estoque", 0)

    if quantidade > estoque_atual:
        st.error(f"Estoque insuficiente. Estoque disponível: {estoque_atual}")
    else:
        # Criar pedido
        novo_pedido = {
            "SKU": sku,
            "Quantidade": quantidade,
            "Descrição": descricao,
            "Observação": observacao,
            "Data": data.strftime("%Y-%m-%d"),
            "Cliente": cliente,
            "Status": status
        }
        colecao_pedidos.insert_one(novo_pedido)

        # Atualizar estoque
        if status == "Pendente":
            colecao_produtos.update_one(
            {"SKU": sku},
            {"$inc": {"Qtd_estoque": -quantidade} } )

    

        st.success("Pedido cadastrado e estoque atualizado com sucesso!")
