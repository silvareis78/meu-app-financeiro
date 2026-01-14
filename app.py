import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu App Financeiro", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS PARA INTERFACE PROFISSIONAL
st.markdown("""
    <style>
    /* Fundo da tela */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Centralizar conteúdo do login */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }

    /* Estilo do Título */
    .main-title {
        color: #1E293B;
        font-size: 28px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: 'Inter', sans-serif;
    }

    /* Subtítulo */
    .sub-title {
        color: #64748B;
        font-size: 16px;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Botão Entrar */
    .stButton>button {
        width: 100%;
        background-color: #0F172A;
        color: white;
        height: 50px;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        margin-top: 10px;
    }
    
    /* Campos de Input */
    .stTextInput>div>div>input {
        border-radius: 12px;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE ACESSO
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Criando colunas para centralizar o login no PC, mas no Celular elas se empilham
    _, col_central, _ = st.columns([0.1, 0.8, 0.1])
    
    with col_central:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        # IMAGEM DO TEMA (Cofre com moedas)
        st.image("https://cdn-icons-png.flaticon.com/512/5551/5551382.png", width=120)
        
        st.markdown("<div class='main-title'>Meu App Financeiro</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Gestão de Gastos - Robson</div>", unsafe_allow_html=True)
        
        # CAMPO DE SENHA
        senha = st.text_input("Senha de Acesso", type="password", placeholder="Digite sua senha secreta")
        
        if st.button("Acessar Carteira"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Senha incorreta. Tente novamente.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# CÓDIGO APÓS LOGIN (Aparece quando você acerta a senha)
# ---------------------------------------------------------
st.success("Você está logado! Em breve montaremos o Dashboard aqui.")
if st.button("Sair"):
    st.session_state.logged_in = False
    st.rerun()
