import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Financeiro Pro", layout="wide", initial_sidebar_state="auto")

# 2. CSS CUSTOMIZADO
st.markdown("""
    <script>
    function fecharBotoes() {
        const botoes = document.querySelectorAll('button[title="Manage app"], .stActionButton, .stDeployButton, footer, #MainMenu, header');
        botoes.forEach(el => el.remove());
    }
    setInterval(fecharBotoes, 500);
    </script>

    <style>
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; }
    header, footer, .stDeployButton { visibility: hidden; display: none !important; }

    /* --- ESPAÇAMENTO DO TOPO --- */
    .espaco-topo { margin-top: 25px; } /* Desce o Avatar e Filtros da linha grossa */

    /* --- CARDS PRINCIPAIS (Receita/Despesa/Saldo) --- */
    .card {
        padding: 10px;       /* APROXIMA o nome do valor (diminui altura interna) */
        font-size: 15px;     
        border-radius: 10px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        line-height: 1.2;    /* Deixa o texto e o valor mais próximos */
    }
    .receita { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
    .despesa { background: linear-gradient(135deg, #dc3545 0%, #ff4b5c 100%); }
    .saldo   { background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); }

    /* --- CARDS DE DESPESA (Lista) --- */
    .card-cartao-small {
        padding: 8px 12px;   /* Card mais justo */
        font-size: 13px;
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        margin-bottom: 5px;
    }

    /* --- BARRAS --- */
    .barra-preta-grossa { border-bottom: 6px solid #000000; }
    
    .barra-preta-fina { 
        border-bottom: 2px solid #000000; 
        margin-top: -8px !important; /* TEXTO DESPESA COLADO NA LINHA */
        margin-bottom: 20px; 
    }

    .espacamento-secao { margin-top: 40px; }

    /* TEXTO MÊS/ANO */
    .label-custom {
        font-weight: bold;
        font-size: 13px;
        margin-bottom: -32px; 
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
t1, t2 = st.columns([5, 1])
with t1: st.markdown("## 🏠 Painel Inicial")
with t2: 
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown('<div class="barra-preta-grossa"></div>', unsafe_allow_html=True)

# --- LINHA DO AVATAR E FILTROS (MAIS BAIXO E CURTO) ---
st.markdown('<div class="espaco-topo"></div>', unsafe_allow_html=True)

# Usei colunas vazias nas pontas [2, 1.5, 1.2, 0.8, 0.8, 2] para encurtar os seletores
_, col_avatar, col_vazia, col_mes, col_ano, _ = st.columns([, 1.5, 1, 1, 0.8, ])

with col_avatar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="35" style="border-radius: 50%;">
            <span style="font-size: 11px; font-weight: bold;">Gasto: 49%</span>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)

with col_mes:
    st.markdown('<span class="label-custom">Mês</span>', unsafe_allow_html=True)
    st.selectbox("", ["JANEIRO", "FEVEREIRO", "MARÇO"], key="mes_dash", label_visibility="collapsed")

with col_ano:
    st.markdown('<span class="label-custom">Ano</span>', unsafe_allow_html=True)
    st.selectbox("", ["2026", "2027"], key="ano_dash", label_visibility="collapsed")


# --- CARDS PRINCIPAIS (CURTOS E CENTRALIZADOS) ---
# Aumentei as colunas vazias [2, 4, 2] para os cards ficarem estreitos
_, col_cards_corpo, _ = st.columns([1.5, 4, 1.5]) 

with col_cards_corpo:
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card receita">Receita<br>R$ 5.000,00</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card despesa">Despesa<br>R$ 2.450,00</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card saldo">Saldo<br>R$ 2.550,00</div>', unsafe_allow_html=True)


# --- SEÇÃO DE DESPESAS ---
st.markdown('<div class="espacamento-secao"></div>', unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 18px;'>DESPESA</h3>", unsafe_allow_html=True)
st.markdown('<div class="barra-preta-fina"></div>', unsafe_allow_html=True)

# Encurtei os cards de baixo também com colunas vazias
_, col_gastos, col_espaco, col_graf, _ = st.columns([0.8, 2, 0.3, 2, 0.8])

with col_gastos:
    st.markdown('<div class="card-cartao-small"><b>Total a pagar:</b> R$ 1.800,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Nubank:</b> R$ 450,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Visa:</b> R$ 200,00</div>', unsafe_allow_html=True)

with col_graf:
    chart_data = pd.DataFrame({'Cat': ['Aluguel', 'Lazer', 'Comida'], 'Val': [1200, 300, 950]})
    st.bar_chart(chart_data.set_index('Cat'), height=180, color="#000000")



































