import streamlit as st

st.title("🤖 Chatbot do Sistema")

with st.sidebar:
    st.header("📋 Menu de Opções")
    st.write("""
    1. Como cadastrar um produto?
    2. Como cadastrar um pedido?
    3. O que é dashboard?
    4. O que são as linhas vermelhas na tabela de produtos?
    5. Alarme de estoque baixo
    6. Como funciona os gráficos do dashboard?
    7. Como adicionar produtos ao estoque por pedido cancelado/devolução?
    8. Ajuda
    9. Sair
    """)

# Inicializar histórico de chat no session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_active" not in st.session_state:
    st.session_state.chat_active = False
if "last_action" not in st.session_state:
    st.session_state.last_action = None

# Exibir histórico de mensagens
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.write(f"**Você:** {msg['content']}")
    else:
        st.write(f"**Bot:** {msg['content']}")

# Função para exibir o menu principal

# Função para processar a escolha do usuário
def processar_escolha(escolha):
    if escolha == "1":
        return "Para cadastrar um produto, vá para a página 'Cadastrar Produtos'. Preencha o formulário com o SKU, título, preço, categoria, quantidade em estoque, marca e, opcionalmente, variantes (como cor ou modelo). Clique em 'Cadastrar Produto' para salvar."
    elif escolha == "2":
        return "Na página 'Cadastrar Pedidos', selecione o SKU do produto, informe a quantidade, descrição, observação, cliente e data do pedido. Clique em 'Cadastrar Pedido'. O sistema verificará se há estoque suficiente antes de salvar."
    elif escolha == "3":
        return "O Dashboard exibe gráficos e métricas, como o produto mais vendido, total de estoque, valor total dos produtos e movimentações por mês. Use os filtros na barra lateral para ajustar as datas ou categorias."
    elif escolha == "4":
        return "As linhas vermelhas na tabela de produtos indicam que o estoque está em nível crítico (igual ou abaixo de 20 unidades), destacando a necessidade de reposição."
    elif escolha == "5":
        return "O alarme de estoque baixo aparece na página 'Home' e 'Cadastrar Pedidos' quando produtos têm menos de 5 unidades. Você também pode verificar a lista completa na página 'Base de Produtos'."
    elif escolha == "6":
        return "Os gráficos do dashboard mostram dados como entradas e saídas de estoque por mês, top 5 produtos mais vendidos, estoque crítico vs. média de vendas e distribuição de vendas por categoria. Use os filtros na barra lateral para personalizar as visualizações."
    elif escolha == "7":
        return "Para adicionar produtos ao estoque por pedido cancelado ou devolução, acesse a página 'Estoque'. Selecione o SKU, escolha o motivo 'Devolução' ou 'Pedido Cancelado', insira a quantidade e o responsável, e clique em 'Registrar movimentação'."
    elif escolha == "8":
        return "Estou aqui para ajudar! Escolha uma opção do menu digitando o número correspondente ou consulte o menu acima para mais informações."
    elif escolha == "9":
        st.session_state.chat_active = False
        return "Chat finalizado. Clique em 'Iniciar Chat' para começar novamente."
    else:
        return "Opção inválida. Por favor, digite um número de 1 a 9."

# Botões de controle
col1, col2 = st.columns(2)
with col1:
    if st.button("Limpar Chat", key="limpar"):
        st.session_state.chat_history = []
        st.session_state.chat_active = False
        st.session_state.last_action = "limpar"
        #st.rerun()
with col2:
    if st.button("Iniciar Chat", key="iniciar") and not st.session_state.chat_active:
        st.session_state.chat_active = True
        #st.session_state.chat_history.append({"role": "bot", "content": exibir_menu()})
        st.session_state.last_action = "iniciar"
        #st.rerun()

# Campo de entrada e envio apenas se o chat estiver ativo
if st.session_state.chat_active:
    user_input = st.text_input("Digite o número da opção desejada:", key="chat_input")
    
    if st.button("Enviar", key="enviar") or (st.session_state.last_action == "enviar" and user_input):
        if user_input and st.session_state.last_action != "enviar":
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            resposta = processar_escolha(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": resposta})
            st.session_state.last_action = "enviar"
            
            if user_input == "9":
                st.session_state.chat_active = False
            
            st.rerun()
        else:
            st.session_state.last_action = None