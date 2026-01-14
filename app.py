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
   header {visibility: hidden; display: none !important;}
    .block-container {padding-top: 0rem;} /* Sobe o Painel Inicial ao máximo */

    /* Barra Preta Grossa */
    .barra-preta-grossa {
        border-bottom: 6px solid #000000;
        margin-bottom: 20px;
    }

    /* Barra Preta Fina para Divisões */
    .barra-preta-fina {
        border-bottom: 2px solid #000000;
        margin: 10px 0 20px 0;
  
    }

    /* Cards em Gradiente */
    .card {
        padding: 20px;
        border-radius: 12px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    .receita { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
    .despesa { background: linear-gradient(135deg, #dc3545 0%, #ff4b5c 100%); }
    .saldo { background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); }
    
    /* Cards de Cartão Menores */
    .card-cartao-small {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        padding: 8px 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 14px;
    }

    /* Labels de Filtros */
    .label-filtro {
        font-weight: bold;
        margin-bottom: -15px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    _, col_central, _ = st.columns([0.1, 0.8, 0.1])
    with col_central:
        st.markdown("<h1 style='text-align:center; color:#008080;'>Meu App Financeiro</h1>", unsafe_allow_html=True)
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# ---------------------------------------------------------
# 4. DASHBOARD
# ---------------------------------------------------------

# Cabeçalho no topo máximo
topo_esq, topo_dir = st.columns([5, 1])
with topo_esq:
    st.markdown("<h2 style='margin-top: 0px;'>🏠 Painel Inicial</h2>", unsafe_allow_html=True)
with topo_dir:
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown('<div class="barra-preta-grossa"></div>', unsafe_allow_html=True)

# Linha 1: Avatar/Gasto e Filtros Verticais
col_avatar, col_vazio, col_mes, col_ano = st.columns([1.5, 1.5, 1, 1])

with col_avatar:
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; background: white; padding: 10px; border-radius: 12px; border: 1px solid #ddd;">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="45" style="border-radius: 50%;">
            <div>
                <p style="margin:0; font-size:11px; color: gray;">Gasto Total</p>
                <p style="margin:0; font-weight: bold; font-size:14px;">49% do Recebido</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)

with col_mes:
    st.markdown('<p class="label-filtro">Mês</p>', unsafe_allow_html=True)
    st.selectbox("", ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], key="sel_mes")

with col_ano:
    st.markdown('<p class="label-filtro">Ano</p>', unsafe_allow_html=True)
    st.selectbox("", ["2025", "2026", "2027"], index=1, key="sel_ano")

# Cards de Receita, Despesa e Saldo
c1, c2, c3 = st.columns(3)
c1.markdown('<div class="card receita">Receita<br>R$ 5.000,00</div>', unsafe_allow_html=True)
c2.markdown('<div class="card despesa">Despesa<br>R$ 2.450,00</div>', unsafe_allow_html=True)
c3.markdown('<div class="card saldo">Saldo<br>R$ 2.550,00</div>', unsafe_allow_html=True)

# Seção Despesa com Barras Pretas
st.markdown("<h3 style='margin-bottom:0px;'>DESPESA</h3>", unsafe_allow_html=True)
st.markdown('<div class="barra-preta-fina"></div>', unsafe_allow_html=True)

col_info_gastos, col_divisor, col_grafico = st.columns([2, 0.1, 2])

with col_info_gastos:
    st.markdown('<div class="card-cartao-small"><b>Total a pagar:</b> R$ 1.800,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Nubank:</b> R$ 450,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Visa:</b> R$ 200,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Mastercard:</b> R$ 300,00</div>', unsafe_allow_html=True)

with col_divisor:
    st.markdown('<div class="divisor-vertical"></div>', unsafe_allow_html=True)

with col_grafico:
    dados = pd.DataFrame({'Cat': ['Aluguel', 'Lazer', 'Comida'], 'Val': [1200, 300, 950]})
    st.bar_chart(dados.set_index('Cat'), color="#000000") # Gráfico em preto para combinar

# Menu Lateral
with st.sidebar:
    st.markdown("## 📊 Menu Principal")
    st.button("Dashboard", use_container_width=True)
    st.button("Lançamentos", use_container_width=True)
    











