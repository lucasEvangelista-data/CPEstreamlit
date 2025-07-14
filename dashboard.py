import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go



st.title("📊 Dashboard de Estoque")

# Conexão com MongoDB
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
produtos = db["produtos"]
pedidos = db["pedidos"]
estoque = db["estoque"]

# Carregar dados
df_produtos = pd.DataFrame(list(produtos.find({}, {"_id": 0})))
df_pedidos = pd.DataFrame(list(pedidos.find({}, {"_id": 0})))
df_estoque = pd.DataFrame(list(estoque.find({}, {"_id": 0})))

# Preprocessamento
df_estoque["Data"] = pd.to_datetime(df_estoque["Data"], errors="coerce")
df_pedidos["Data"] = pd.to_datetime(df_pedidos["Data"], errors="coerce")

# === CARDS ===
if not df_pedidos.empty:
    sku_mais_vendido = df_pedidos.groupby("SKU")["Quantidade"].sum().idxmax()
    titulo_mais_vendido = df_produtos[df_produtos["SKU"] == sku_mais_vendido]["Título"].values[0]
else:
    titulo_mais_vendido = "Sem pedidos"

total_estoque = df_produtos["Qtd_estoque"].sum() if not df_produtos.empty else 0

total_money_estoque = df_produtos["Preço"].sum()
valor_formatado = f"R$ {total_money_estoque:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

mes_atual = datetime.today().strftime("%Y-%m")
mov_mes = df_estoque[df_estoque["Data"].dt.strftime("%Y-%m") == mes_atual]
total_mov_mes = mov_mes.shape[0]

def card_com_borda(titulo, valor, delta=""):
    st.markdown(
        f"""
        <div style='border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #111; text-align: center'>
            <p style='margin:0; color:#ccc; font-size:14px'>{titulo}</p>
            <p style='margin:0; font-size:24px; font-weight:bold; color:white'>{valor}</p>
            <p style='margin:0; color:orange; font-size:12px'>{delta}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3 = st.columns(3)
with col1:
    card_com_borda("📦 Produto mais vendido", titulo_mais_vendido)
with col2:
    card_com_borda("📊 Total de produtos em estoque", total_estoque)
with col3:
    card_com_borda("💰 Valor total de produtos em estoque", valor_formatado)

st.divider()

# === GRÁFICOS ===

# 📌 Filtros globais
with st.sidebar:
    st.subheader("📅 Filtros")
    data_inicial = st.date_input("Data inicial", value=datetime(2025, 1, 1))
    data_final = st.date_input("Data final", value=datetime.today())

    # Filtro por Categoria
    categorias = df_produtos["Categoria_produto"].dropna().unique().tolist()
    categorias.sort()
    categoria_filtro = st.selectbox("Filtrar por Categoria", ["Todos"] + categorias)


    # Filtro por Motivo
    lista_motivos = ["Todos"] + sorted(df_estoque["Motivo"].dropna().unique().tolist())
    motivo_filtro = st.selectbox("Filtrar por Motivo", lista_motivos)

    # Aplicar filtros no df_estoque
    # Aplicar filtros no df_pedidos
    df_pedidos_filtrado = df_pedidos.copy()
    df_pedidos_filtrado = df_pedidos_filtrado[
    (df_pedidos_filtrado["Data"] >= pd.to_datetime(data_inicial)) &
    (df_pedidos_filtrado["Data"] <= pd.to_datetime(data_final))]

    df_filtrado = df_estoque.copy()
    df_filtrado = df_filtrado[(df_filtrado["Data"] >= pd.to_datetime(data_inicial)) &
                            (df_filtrado["Data"] <= pd.to_datetime(data_final))]

    
    if motivo_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Motivo"] == motivo_filtro]



# 1. Entradas x Saídas por mês
if not df_estoque.empty and not df_pedidos.empty:
    # → Estoque (Entradas)
    df_estoque["MesAno"] = df_estoque["Data"].dt.to_period("M").astype(str)
    df_estoque_entradas = df_estoque[["MesAno", "Quantidade"]].copy()
    df_estoque_entradas["Tipo"] = "Entrada"

    # → Pedidos (Saídas)
    df_pedidos["MesAno"] = df_pedidos["Data"].dt.to_period("M").astype(str)
    df_pedidos_saidas = df_pedidos[["MesAno", "Quantidade"]].copy()
    df_pedidos_saidas["Quantidade"] = df_pedidos_saidas["Quantidade"]  # saída é negativa
    df_pedidos_saidas["Tipo"] = "Saída"

    # → Unir os dois
    df_movimentacoes = pd.concat([df_estoque_entradas, df_pedidos_saidas], ignore_index=True)

    # → Agrupar e somar
    resumo_entrada_saida = df_movimentacoes.groupby(["MesAno", "Tipo"])["Quantidade"].sum().reset_index()

    # → Gráfico
    fig1 = px.bar(resumo_entrada_saida, x="MesAno", y="Quantidade", color="Tipo", barmode="group",
                  title="📊 Entradas x Saídas de Estoque por Mês")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Não há movimentações e pedidos suficientes para o gráfico.")


# 2. Gráfico de Motivos
if not df_filtrado.empty and "Motivo" in df_filtrado.columns:
    # Juntar com os produtos para obter os títulos
    df_motivo = df_filtrado.merge(df_produtos[["SKU", "Título"]], on="SKU", how="left")

    # Criar coluna para exibir no gráfico: "Motivo - Produto"
    df_motivo["Motivo_Produto"] = df_motivo["Título"]

    # Agrupar por Motivo e Produto
    motivo_count = df_motivo.groupby(["Motivo_Produto", "Motivo"])["Quantidade"].sum().reset_index()
    motivo_count = motivo_count.sort_values(by="Quantidade", ascending=True) 

    # Gráfico de barras horizontais com cores por motivo
    grafico_motivo = px.bar(
        motivo_count,
        x="Quantidade",
        y="Motivo_Produto",
        color="Motivo",
        orientation="h",
        title="🔍 Entrada no Estoque por Motivo e Produto",
        labels={"Motivo_Produto": "Produto", "Quantidade": "Quantidade"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    grafico_motivo.update_layout(xaxis=dict(showgrid=True, gridcolor='gray', gridwidth=0.5))

    st.plotly_chart(grafico_motivo, use_container_width=True)


# 3. Ranking de produtos mais vendidos

    top_vendidos = df_pedidos_filtrado.groupby("SKU")["Quantidade"].sum().reset_index()
    top_vendidos.columns = ["SKU", "Total_vendido"]
    top_vendidos = top_vendidos.merge(df_produtos[["SKU", "Título"]], on="SKU", how="left")
    top_vendidos = top_vendidos.sort_values(by="Total_vendido", ascending=False).head(5)

    fig_top = px.bar(
        top_vendidos,
        x="Título",
        y="Total_vendido",
        title="🏅 Top 5 Produtos Mais Vendidos",
        labels={"Título": "Produto", "Total_vendido": "Unidades Vendidas"},
        color_discrete_sequence=["lightskyblue"]
    )
    st.plotly_chart(fig_top, use_container_width=True)


#Grafico 4 st.subheader("📉 Estoque Crítico vs. Média de Vendas Mensal")

# 1. Selecionar produtos com estoque crítico
produtos_criticos = df_produtos[df_produtos["Qtd_estoque"] <= 20]

if not produtos_criticos.empty:
    # 2. Calcular a média de vendas por mês para cada produto
    df_pedidos["AnoMes"] = df_pedidos["Data"].dt.to_period("M")
    pedidos_group = df_pedidos.groupby(["SKU", "AnoMes"])["Quantidade"].sum().reset_index()

    # 3. Calcular a média mensal por SKU
    media_mensal = pedidos_group.groupby("SKU")["Quantidade"].mean().reset_index()
    media_mensal.columns = ["SKU", "Media_Vendas_Mensal"]

    # 4. Juntar com os produtos críticos
    criticos_com_media = produtos_criticos.merge(media_mensal, on="SKU", how="left")
    criticos_com_media["Media_Vendas_Mensal"].fillna(0, inplace=True)  # caso algum produto nunca tenha sido vendido

    # 5. Preparar dados para o gráfico (reshape para barras lado a lado)
    criticos_com_media = criticos_com_media.rename(columns={"Título": "Produto"})
    criticos_com_media_melted = criticos_com_media.melt(
        id_vars=["Produto"],
        value_vars=["Qtd_estoque", "Media_Vendas_Mensal"],
        var_name="Tipo",
        value_name="Quantidade"
    )

    # 6. Criar gráfico de barras lado a lado
    fig_critico = px.bar(
        criticos_com_media_melted,
        x="Produto",
        y="Quantidade",
        color="Tipo",
        title="🚨 Produtos com Estoque Baixo vs Média de Vendas Mensal",
        labels={"Quantidade": "Quantidade", "Produto": "Produto"},
        color_discrete_map={"Qtd_estoque": "rosybrown", "Media_Vendas_Mensal": "red"}
    )
    fig_critico.update_layout(
        xaxis_title="Produto",
        yaxis_title="Quantidade",
        legend_title="Tipo",
        barmode="group"
    )
    st.plotly_chart(fig_critico, use_container_width=True)

else:
    st.info("Nenhum produto com estoque crítico encontrado.")


# Agrupando as vendas por categoria
vendas_categoria = df_pedidos_filtrado.merge(df_produtos[["SKU", "Categoria_produto"]], on="SKU", how="left")
vendas_categoria = vendas_categoria.groupby("Categoria_produto")["Quantidade"].sum().reset_index()

# Gráfico de pizza com rótulo externo e linha
fig_pizza = go.Figure(data=[go.Pie(
    labels=vendas_categoria["Categoria_produto"],
    values=vendas_categoria["Quantidade"],
    textinfo='label+percent',
    textposition='outside',
    pull=[0.01]*len(vendas_categoria),  # ligeira separação das fatias
    marker=dict(line=dict(color='black', width=1))  # borda preta para melhorar a leitura
)])

fig_pizza.update_layout(
    title="📊 Distribuição de Vendas por Categoria",
    showlegend=False
)

st.plotly_chart(fig_pizza, use_container_width=True)


