import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS "FORÇA BRUTA" PARA SUMIR COM TUDO
st.markdown("""
    <style>
    /* 1. Remove Header, Footer e Menu */
    header, footer, #MainMenu {visibility: hidden !important; display: none !important;}
    
    /* 2. Ataca os botões flutuantes do canto inferior (Manage App, Deploy, etc) */
    .stDeployButton, .stActionButton, .stStatusWidget {display: none !important;}
    
    /* 3. Seletores específicos para as versões mobile do Streamlit Cloud */
    [data-testid="stStatusWidget"], 
    [data-testid="manage-app-button"], 
    [data-testid="stActionButton"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 4. Remove qualquer elemento flutuante no canto inferior direito */
    div[class^="st-emotion-cache-"] button { display: none !important; }
    iframe[title="Manage app"] { display: none !important; }
    
    /* Centralização do Login */
    .block-container {
        padding-top: 0rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }

    .logo-text {
        font-family: 'Inter', sans-serif;
        color: #008080;
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
    }

    .stButton>button {
        width: 100%;
        background-color: #20B2AA !important;
        color: white !important;
        border: none;
        height: 50px;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
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
                st.error("Dados incorretos.")
    st.stop()

# CONTEÚDO PÓS-LOGIN
st.title("Olá, Robson!")
if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
    



