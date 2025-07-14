import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth


senhas_criptografadas = stauth.Hasher(["123456", "654321"]).generate()

credenciais = {"usernames":{
    "gestao@gmail.com": {"name": "Gestor", "password": senhas_criptografadas[0]},
    "func_1@gmail.com": {"name": "Funcionario", "password": senhas_criptografadas[1]}
    #"func_2@gmail.com": {"name": "Funcionario", "password": senhas_criptografadas[2]}
    #"func_3@gmail.com": {"name": "Funcionario", "password": senhas_criptografadas[3]}
}}

authenticador = stauth.Authenticate(credenciais, "credenciais_ebo", "eb%$67247BO#htbN%5", cookie_expiry_days=30)

def autenticar_usuario (authenticator):
    nome, status_autenticacao, username = authenticador.login()
    if status_autenticacao:
        return{"nome": nome, "username": username}
    elif status_autenticacao == False:
        st.error("Usuário ou email inválidos")
    else:
        st.error("Preencha corretamente o formulário para fazer login")

def logout():
    authenticador.logout()

#Autenticar usuário
dados_usuario = autenticar_usuario(authenticador)

if dados_usuario:
    username = dados_usuario["username"]
    user_role = credenciais["usernames"][username]["name"]

    from data_loader import carregar_dados_mongo

    @st.cache_data
    def carregar_dados():
        return carregar_dados_mongo()

    base = carregar_dados()


    if user_role == "Gestor":

        pg = st.navigation(
            {
                "Home": [st.Page("homepage.py", title="EBO Fied")],
                "Dashboards": [st.Page("dashboard.py", title="Dashboard")],
                "Produtos": [st.Page("produtos.py", title="Base de Produtos"),
                st.Page("cadastro_produto.py", title="Cadastrar Produtos"),
                st.Page("estoque.py", title="Estoque"),
                st.Page("movimenta_estoque.py", title="Histórico estoque")],
                "Pedidos":[st.Page("cadastro_pedidos.py", title="Cadastrar Pedidos"),
                st.Page("gerenciar_pedidos.py", title="Gerenciar Pedidos")],
                "Chatbot": [st.Page("chatbot.py", title="Chatbot do Sistema")],
                "Conta": [st.Page(logout, title="Sair")]
            } )
    else:
         pg = st.navigation(
            {
                "Produtos": [st.Page("produtos.py", title="Base de Produtos"),
                st.Page("cadastro_produto.py", title="Cadastrar Produtos"),
                st.Page("estoque.py", title="Estoque"),
                st.Page("movimenta_estoque.py", title="Histórico estoque")],
                "Pedidos":[st.Page("cadastro_pedidos.py", title="Cadastrar Pedidos"),
                st.Page("gerenciar_pedidos.py", title="Gerenciar Pedidos")],
                "Conta": [st.Page(logout, title="Sair")]
            } )   

    pg.run()
