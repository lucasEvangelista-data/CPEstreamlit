import streamlit as st
from data_loader import carregar_movimentacoes_estoque

st.title("Histórico de Movimentações de Estoque")

df = carregar_movimentacoes_estoque()

st.dataframe(df)
