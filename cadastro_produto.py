import streamlit as st
from pymongo import MongoClient

st.title("Cadastrar Produtos")

# Conectar ao MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
colecao = db["produtos"]

# Formulário
with st.form("form_cadastro"):
    sku = st.text_input("Código SKU")
    titulo = st.text_input("Título do produto")
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.01)
    categoria = st.selectbox("Categoria", ["Utensílio Doméstico", "Brinquedos", "Esportes", "Material Escolar"])
    estoque = st.number_input("Quantidade em estoque", min_value=0, step=1)
    marca = st.text_input("Marca")

    st.markdown("### Variante 1")
    variante1_nome = st.text_input("Nome da variante 1", value="Cor")
    variante1_opcao = st.text_input("Opção da variante 1", value="")

    st.markdown("### Variante 2 (opcional)")
    variante2_nome = st.text_input("Nome da variante 2", value="Modelo")
    variante2_opcao = st.text_input("Opção da variante 2", value="")

    enviar = st.form_submit_button("Cadastrar Produto")

# Lógica ao submeter
if enviar:
    if not sku or not titulo:
        st.warning("Preencha todos os campos obrigatórios.")
    else:
        novo_produto = {
            "SKU": sku,
            "Título": titulo,
            "Preço": round(preco, 2),
            "Categoria_produto": categoria,
            "Qtd_estoque": estoque,
            "Marca": marca,
            "Variante": []
        }

        # Adiciona variantes se preenchidas
        if variante1_opcao:
            novo_produto["Variante"].append({"Nome": variante1_nome, "Opção": variante1_opcao})
        if variante2_opcao:
            novo_produto["Variante"].append({"Nome": variante2_nome, "Opção": variante2_opcao})

        colecao.insert_one(novo_produto)
        st.success(f"Produto '{titulo}' cadastrado com sucesso!")
