import streamlit as st

from data_loader import carregar_dados_mongo

df = carregar_dados_mongo()

# variantes como texto legível
df["Variante"] = df["Variante"].apply(lambda x: ", ".join([f"{v['Nome']}: {v['Opção']}" for v in x]) if isinstance(x, list) else "")


st. title ("Produtos")
def destacar_estoque(row):
    if row["Qtd_estoque"] <= 20:
        return ["background-color: #DF0406"] * len(row)  
    return [""] * len(row)

st.dataframe(df.style.apply(destacar_estoque, axis=1))
