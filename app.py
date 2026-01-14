import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS "MODO INVISÍVEL" + JAVASCRIPT PARA REMOVER BOTÕES TEIMOSOS
st.markdown("""
    <script>
    // Função para remover os botões chatos do Streamlit no celular
    function fecharBotoes() {
        const botoes = document.querySelectorAll('button[title="Manage app"], .stActionButton, .stDeployButton, footer, #MainMenu, header');
        botoes.forEach(el => el.remove());
        
        // Remove indicadores de status no canto inferior
        const status = document.querySelectorAll('[data-testid="stStatusWidget"]');
        status.forEach(el => el.remove());
    }
    // Executa a cada meio segundo para garantir que eles não voltem
    setInterval(fecharBotoes, 500);
    </script>

    <style>
    /* Esconder tudo que for do Streamlit */
    header, footer, #MainMenu, .stDeployButton, .stActionButton {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Tenta esconder o container dos botões no celular */
    div[data-testid="stStatusWidget"], 
    [data-testid="manage-app-button"] {
        display: none !important;
    }

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
    
    /* Remove bordas de foco que aparecem no mobile */
    input:focus {
        outline: none !important;
        border: 2px solid #20B2AA !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    _, col_central, _ = st.columns([0.05, 0.9, 0.05])
    
    with col_central:
        st.markdown('<p class="logo-text">Meu App Financeiro</p>', unsafe_allow_html=True)
        email = st.text_input("E-mail", placeholder="seuemail@gmail.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Senha ou e-mail incorretos.")
    st.stop()

# ---------------------------------------------------------
# CONTEÚDO PÓS-LOGIN
# ---------------------------------------------------------
st.title("Olá, Robson!")
st.write("Estamos dentro!")

if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
    




