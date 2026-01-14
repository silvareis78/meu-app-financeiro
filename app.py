import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILIZAÇÃO CSS (Ajustada para não cortar o texto)
st.markdown("""
    <style>
    /* Remover margens e barras desnecessárias */
    .block-container { padding: 1rem 2rem; }
    footer {visibility: hidden;}
    
    /* Fundo */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Estilo do Título (Verde Água) */
    .logo-text {
        font-family: 'Inter', sans-serif;
        color: #008080;
        font-size: clamp(24px, 5vw, 35px); /* Fonte diminui no celular */
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 5px;
    }
    .fature-text {
        color: #1E293B;
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* Botão Acessar */
    .stButton>button {
        width: 100%;
        background-color: #20B2AA !important;
        color: white !important;
        border: none;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        height: 45px;
    }

    /* AJUSTE DA IMAGEM: Controla o tamanho para não cortar */
    .img-container img {
        max-width: 100%;
        height: auto;
        max-height: 450px; /* Limita a altura no PC */
        border-radius: 20px;
        object-fit: cover;
    }

    /* Ajuste para telas pequenas (Celular) */
    @media (max-width: 768px) {
        .img-container img {
            max-height: 250px; /* Imagem menor no celular para sobrar espaço */
            margin-top: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Colunas: Esquerda mais larga para o texto não apertar
    col1, col2 = st.columns([1.2, 1], gap="medium")

    with col1:
        st.markdown('<p class="logo-text">MeuApp<br>Financeiro</p>', unsafe_allow_html=True)
        st.markdown('<p class="fature-text">FATURE SISTEMAS</p>', unsafe_allow_html=True)
        
        email = st.text_input("E-mail", placeholder="seuemail@gmail.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Dados incorretos.")

    with col2:
        # Imagem dentro de um container para controlar o tamanho
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image("https://img.freepik.com/fotos-gratis/conceito-de-crescimento-de-negocios-com-moedas-e-planta_23-2148803930.jpg")
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------------------------------------------------------
# CONTEÚDO PÓS-LOGIN
# ---------------------------------------------------------
st.success("Login realizado com sucesso!")
if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
    
