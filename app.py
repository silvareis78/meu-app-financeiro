import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILIZAÇÃO CSS AVANÇADA
st.markdown("""
    <style>
    /* Remover margens padrão */
    .block-container { padding: 0px; }
    footer {visibility: hidden;}
    
    /* Fundo em degradê suave */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Container Principal */
    .main-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        padding: 20px;
    }

    /* Estilo do Título (Verde Água) */
    .logo-text {
        font-family: 'Inter', sans-serif;
        color: #008080;
        font-size: 35px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 5px;
    }
    .fature-text {
        color: #1E293B;
        font-size: 14px;
        letter-spacing: 2px;
        font-weight: 500;
        margin-bottom: 30px;
    }

    /* Estilo dos Inputs */
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 8px;
    }

    /* Botão Acessar (Igual da imagem) */
    .stButton>button {
        width: 100%;
        background-color: #20B2AA !important;
        color: white !important;
        border: none;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #008080 !important;
        transform: translateY(-2px);
    }

    /* Imagem Arredondada */
    .img-rounded {
        border-radius: 30px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Criando as duas colunas (Esquerda: Login | Direita: Imagem)
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("<div style='padding: 50px;'>", unsafe_allow_html=True)
        
        # Logo e Título
        st.markdown('<p class="logo-text">MeuApp<br>Financeiro</p>', unsafe_allow_html=True)
        st.markdown('<p class="fature-text">FATURE SISTEMAS</p>', unsafe_allow_html=True)
        
        # Inputs
        email = st.text_input("E-mail", placeholder="seuemail@exemplo.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Dados incorretos.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Imagem que remete à prosperidade e crescimento (como na sua referência)
        st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
        st.image("https://img.freepik.com/fotos-gratis/conceito-de-crescimento-de-negocios-com-moedas-e-planta_23-2148803930.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------------------------------------------------------
# CONTEÚDO PÓS-LOGIN (O que aparece depois de entrar)
# ---------------------------------------------------------
st.title("Bem-vindo ao seu Dashboard!")
if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
