import streamlit as st # Biblioteca principal

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="App Financeiro")

# --- TESTE DE MENU (NATIVO) ---
# Se este bloco não aparecer, o erro está antes dele
with st.sidebar:
    st.markdown("### 🗂️ Navegação")
    selecionado = st.selectbox(
        "Ir para:",
        ["Painel Inicial", "Despesa", "Receita", "Cartões", "Cadastros Iniciais", "Configurações"]
    )







































































































