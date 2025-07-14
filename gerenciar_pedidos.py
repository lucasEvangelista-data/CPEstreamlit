import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

st.title("Gerenciar Pedidos")

# Conexão com MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
colecao_pedidos = db["pedidos"]

# Carrega pedidos
pedidos = list(colecao_pedidos.find())
df = pd.DataFrame(pedidos)

# Conversão e limpeza
if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    df["Data_str"] = df["Data"].dt.strftime("%d/%m/%Y")
    df["id_str"] = df["_id"].astype(str)
else:
    st.info("Nenhum pedido cadastrado ainda.")
    st.stop()

# Filtros
with st.sidebar:
    st.subheader("Filtros")
    sku_filtro = st.selectbox("Filtrar por SKU", options=["Todos"] + sorted(df["SKU"].unique().tolist()))
    status_filtro = st.selectbox("Filtrar por Status", options=["Todos", "Pendente", "Em andamento", "Concluído"])
    data_filtro = st.date_input("Filtrar por Data", value=None)

# Aplicar filtros
df_filtrado = df.copy()

if sku_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["SKU"] == sku_filtro]

if status_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Status"] == status_filtro]

if data_filtro:
    data_filtro = pd.to_datetime(data_filtro)
    df_filtrado = df_filtrado[df_filtrado["Data"].dt.date == data_filtro.date()]

# Exibir pedidos
st.subheader("Pedidos encontrados:")
if df_filtrado.empty:
    st.warning("Nenhum pedido encontrado com os filtros selecionados.")
else:
    for i, row in df_filtrado.iterrows():
        with st.expander(f"📦 Pedido SKU: {row['SKU']} — Cliente: {row['Cliente']} — Data: {row['Data_str']}"):
            st.write(f"**Descrição:** {row['Descrição']}")
            st.write(f"**Observação:** {row['Observação']}")
            st.write(f"**Quantidade:** {row['Quantidade']}")
            st.write(f"**Status atual:** {row['Status']}")
            
            novo_status = st.selectbox(
                f"Atualizar status do pedido {row['id_str']}",
                ["Pendente", "Em andamento", "Concluído"],
                index=["Pendente", "Em andamento", "Concluído"].index(row["Status"]),
                key=f"status_{row['id_str']}"
            )
            
            if st.button(f"Atualizar Status do Pedido {row['id_str']}", key=f"btn_{row['id_str']}"):
                colecao_pedidos.update_one(
                    {"_id": row["_id"]},
                    {"$set": {"Status": novo_status}}
                )
                st.success("Status atualizado com sucesso!")
