import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS "ULTRA-CLEAN" (Remove absolutamente todos os ícones e barras)
st.markdown("""
    <style>
    /* Esconder Header, Rodapé e Menu */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* Remover TODOS os botões flutuantes e indicadores do canto inferior direito */
    .stDeployButton {display:none !important;}
    div[data-testid="stStatusWidget"] {display:none !important;}
    button[title="Manage app"] {display: none !important;}
    .stActionButton {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    div[class^="st-emotion-cache-10zv66v"] {display: none !important;} /* Seletor para novos layouts */
    
    /* Centralização e Estética */
    .block-container {
        padding-top: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
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
        font-size: 16px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Coluna para centralizar no PC
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

# ---------------------------------------------------------
# CONTEÚDO PÓS-LOGIN (DASHBOARD)
# ---------------------------------------------------------
st.title("Olá, Robson!")
st.write("Agora sim! Tela 100% limpa.")

if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
    


