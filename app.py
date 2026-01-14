import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Financeiro Pro", layout="wide", initial_sidebar_state="auto")

# 2. CSS "MODO INVISÍVEL" + ESTILO DOS CARDS
st.markdown("""
    <script>
    function fecharBotoes() {
        const botoes = document.querySelectorAll('button[title="Manage app"], .stActionButton, .stDeployButton, footer, #MainMenu, header');
        botoes.forEach(el => el.remove());
        const status = document.querySelectorAll('[data-testid="stStatusWidget"]');
        status.forEach(el => el.remove());
    }
    setInterval(fecharBotoes, 500);
    </script>

    <style>
    /* Esconder elementos nativos */
    header, footer, .stDeployButton {visibility: hidden; display: none !important;}

    /* Título do Login */
    .logo-text-login {
        color: #008080;
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Estilização dos Cards em Gradiente */
    .card {
        padding: 20px;
        border-radius: 15px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .receita { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
    .despesa { background: linear-gradient(135deg, #dc3545 0%, #ff4b5c 100%); }
    .saldo { background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); }
    
    /* Barra Vermelha Lateral */
    .barra-vermelha {
        border-left: 6px solid #dc3545;
        padding-left: 12px;
        font-weight: bold;
        font-size: 18px;
        color: #1E293B;
        margin: 25px 0 15px 0;
    }

    /* Container do Avatar */
    .avatar-box {
        text-align: center;
        padding: 10px;
        background: white;
        border-radius: 15px;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SISTEMA DE LOGIN (ÚNICO E CORRIGIDO)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    _, col_central, _ = st.columns([0.1, 0.8, 0.1])
    with col_central:
        st.markdown('<p class="logo-text-login">Meu App Financeiro</p>', unsafe_allow_html=True)
        email = st.text_input("E-mail", placeholder="seuemail@gmail.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Dados incorretos.")
    st.stop() # Interrompe aqui até logar

# ---------------------------------------------------------
# 4. DASHBOARD (SÓ EXECUTA APÓS O LOGIN)
# ---------------------------------------------------------

# Cabeçalho: Painel Inicial (Esquerda) e Sair (Direita)
topo_esq, topo_dir = st.columns([5, 1])
with topo_esq:
    st.markdown("### 🏠 Painel Inicial")
with topo_dir:
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

st.divider()

# Linha 1: Filtros, Cards e Avatar
col_filtros, col_cards, col_avatar = st.columns([1, 2.5, 1.2])

with col_filtros:
    mes = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
    ano = st.selectbox("Ano", ["2025", "2026", "2027"])

with col_cards:
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card receita">Receita<br>R$ 5.000,00</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card despesa">Despesa<br>R$ 2.450,00</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card saldo">Saldo<br>R$ 2.550,00</div>', unsafe_allow_html=True)

with col_avatar:
    st.markdown("""
        <div class="avatar-box">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="55" style="border-radius: 50%;">
            <p style="margin:5px 0; font-size:13px; color: gray;">Gasto: <b>49%</b> do recebido</p>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)

# Linha 2: Descrição Despesa e Detalhes
st.markdown('<div class="barra-vermelha">DESCRIÇÃO DESPESA</div>', unsafe_allow_html=True)

col_detalhes, col_grafico = st.columns([1, 1])

with col_detalhes:
    st.info("📌 **Total a pagar no mês:** R$ 1.800,00")
    st.warning("💳 **Nubank:** R$ 450,00")
    st.warning("💳 **Visa:** R$ 200,00")

with col_grafico:
    # Gráfico de exemplo
    dados = pd.DataFrame({'Cat': ['Aluguel', 'Lazer', 'Comida'], 'Val': [1200, 300, 950]})
    st.bar_chart(dados.set_index('Cat'))

# Menu Lateral
with st.sidebar:
    st.markdown("## ⚙️ Menu")
    st.button("📊 Dashboard", use_container_width=True)
    st.button("💸 Lançamentos", use_container_width=True)
    st.button("📋 Extrato", use_container_width=True)
    







