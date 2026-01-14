import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS PARA CENTRALIZAR E LIMPAR A INTERFACE
st.markdown("""
    <style>
    /* Esconder Barra Superior e Botão 'Manage App' */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    
    /* Remover espaços em branco no topo */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }

    /* Container de Login Centralizado */
    .login-box {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        width: 100%;
        max-width: 400px;
    }

    /* Título */
    .logo-text {
        font-family: 'Inter', sans-serif;
        color: #008080;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 30px;
    }

    /* Botão Acessar */
    .stButton>button {
        width: 100%;
        background-color: #20B2AA !important;
        color: white !important;
        border: none;
        height: 50px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN (Interface Centralizada)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Usando colunas apenas para garantir a centralização perfeita no Streamlit
    _, col_central, _ = st.columns([0.1, 0.8, 0.1])
    
    with col_central:
        st.markdown('<p class="logo-text">Meu App Financeiro</p>', unsafe_allow_html=True)
        
        email = st.text_input("E-mail", placeholder="seuemail@gmail.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Dados incorretos. Tente novamente.")
    st.stop()

# ---------------------------------------------------------
# CONTEÚDO PÓS-LOGIN (Dashboard)
# ---------------------------------------------------------
# Aqui reativamos a barra para você poder navegar após o login
st.markdown("<style>header {visibility: visible;}</style>", unsafe_allow_html=True)

st.title("Olá, Robson!")
st.write("Seu painel financeiro será montado aqui.")

if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
    

