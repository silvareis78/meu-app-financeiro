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

    /* Barra cinza mais grossa no topo */
    .divisor-grossa { 
        border-bottom: 4px solid #E2E8F0; 
        margin-bottom: 20px; 
        margin-top: -10px;
    }
    
    /* Ajuste para filtros ficarem na mesma linha (Label + Input) */
    .filter-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }

    /* Cards de Cartão mais elegantes */
    .card-cartao {
        background-color: #F1F5F9;
        border-left: 5px solid #475569;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #1E293B;
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

# Cabeçalho mais alto e barra grossa
topo_esq, topo_dir = st.columns([5, 1])
with topo_esq:
    st.markdown("<h2 style='margin-bottom: 0px;'>🏠 Painel Inicial</h2>", unsafe_allow_html=True)
with topo_dir:
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown('<div class="divisor-grossa"></div>', unsafe_allow_html=True)

# No Celular: Avatar e Porcentagem aparecem PRIMEIRO
col_avatar, col_filtros = st.columns([1, 1])

with col_avatar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 15px; background: white; padding: 10px; border-radius: 15px; border: 1px solid #eee;">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="50" style="border-radius: 50%;">
            <div>
                <p style="margin:0; font-size:12px; color: gray;">Gasto Total</p>
                <p style="margin:0; font-weight: bold; color: #1E293B;">49% do Recebido</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)

with col_filtros:
    # Filtros com Label e Caixa lado a lado usando colunas internas
    f1, f2 = st.columns(2)
    with f1:
        st.selectbox("Mês", ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"], label_visibility="collapsed")
    with f2:
        st.selectbox("Ano", ["2025", "2026", "2027"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Cards de Receita, Despesa e Saldo
c1, c2, c3 = st.columns(3)
c1.markdown('<div class="card receita">Receita<br>R$ 5.000,00</div>', unsafe_allow_html=True)
c2.markdown('<div class="card despesa">Despesa<br>R$ 2.450,00</div>', unsafe_allow_html=True)
c3.markdown('<div class="card saldo">Saldo<br>R$ 2.550,00</div>', unsafe_allow_html=True)

# Seção de Despesas
st.markdown('<div class="barra-vermelha">DESPESA</div>', unsafe_allow_html=True)

col_detalhes, col_grafico = st.columns([1, 1])

with col_detalhes:
    st.markdown('<div class="card-cartao"><b>Total a pagar:</b> R$ 1.800,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao"><b>💳 Nubank:</b> R$ 450,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao"><b>💳 Visa:</b> R$ 200,00</div>', unsafe_allow_html=True)

with col_grafico:
    dados = pd.DataFrame({'Cat': ['Aluguel', 'Lazer', 'Comida'], 'Val': [1200, 300, 950]})
    st.bar_chart(dados.set_index('Cat'), color="#dc3545")

# Menu Lateral
with st.sidebar:
    st.markdown("## ⚙️ Menu")
    st.button("📊 Dashboard", use_container_width=True)
    st.button("💸 Lançamentos", use_container_width=True)
    








