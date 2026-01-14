import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Financeiro Pro", layout="wide", initial_sidebar_state="auto")

# 2. CSS CUSTOMIZADO + SCRIPT DE LIMPEZA
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

    /* --- CARDS PRINCIPAIS (Receita/Despesa/Saldo) --- */
    .card {
        padding: 20px;       /* Ajuste de ALTURA interna */
        font-size: 16px;     /* Ajuste de TAMANHO DA FONTE */
        border-radius: 12px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .receita { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
    .despesa { background: linear-gradient(135deg, #dc3545 0%, #ff4b5c 100%); }
    .saldo   { background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); }

    /* --- CARDS DE DESPESA (Cartões) --- */
    .card-cartao-small {
        padding: 10px 15px;  /* (Altura, Comprimento Interno) */
        font-size: 14px;
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        margin-bottom: 8px;
    }

    /* --- BARRAS --- */
    .barra-preta-grossa { border-bottom: 6px solid #000000; margin-bottom: 10px; }
    
    .barra-preta-fina { 
        border-bottom: 2px solid #000000; 
        margin-top: -15px !important; /* COLA O TEXTO 'DESPESA' NA LINHA */
        margin-bottom: 25px; 
    }

    .espacamento-secao {
        margin-top: 20px; /* AJUSTE AQUI O ESPAÇO ENTRE A LINHA GROSSA E A FINA */
    }

    h3 { margin-bottom: 0px !important; } /* Tira espaço abaixo do título Despesa */
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SIMPLIFICADO PARA TESTE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = True # Pulei login para focar no layout

# ---------------------------------------------------------
# 4. DASHBOARD
# ---------------------------------------------------------

# Topo
t1, t2 = st.columns([5, 1])
with t1: st.markdown("## 🏠 Painel Inicial")
with t2: st.button("Sair")

st.markdown('<div class="barra-preta-grossa"></div>', unsafe_allow_html=True)

# --- LINHA DO AVATAR E FILTROS ---
# Para encurtar esta linha, aumente os números das colunas vazias (os 0.5)
_, col_avatar, col_vazia, col_mes, col_ano, _ = st.columns([0.1, 1.2, 0.5, 1, 1, 0.1])

with col_avatar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="40" style="border-radius: 50%;">
            <span style="font-size: 12px; font-weight: bold;">Gasto: 49%</span>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)

with col_mes:
    st.markdown('<span class="label-custom">Mês</span>', unsafe_allow_html=True)
    st.selectbox("", ["JANEIRO", "FEVEREIRO", "MARÇO"], key="mes_dashboard")

with col_ano:
    st.markdown('<span class="label-custom">Ano</span>', unsafe_allow_html=True)
    st.selectbox("", ["2026", "2027"], key="ano_dashboard")

# --- AJUSTE DE COMPRIMENTO DOS CARDS ---
# Usei colunas vazias [1, 4, 1] para o card não ficar esticado na tela toda
_, col_cards_central, _ = st.columns([0.1, 5, 0.1]) # Mude o 0.1 para valores maiores para ENCURTAR os cards
with col_cards_central:
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card receita">Receita<br>R$ 5.000,00</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card despesa">Despesa<br>R$ 2.450,00</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card saldo">Saldo<br>R$ 2.550,00</div>', unsafe_allow_html=True)

# --- SEÇÃO DE DESPESAS (Com espaçamento aumentado) ---
st.markdown('<div class="espacamento-secao"></div>', unsafe_allow_html=True)
st.markdown("<h3>DESPESA</h3>", unsafe_allow_html=True)
st.markdown('<div class="barra-preta-fina"></div>', unsafe_allow_html=True)

# Ajuste de comprimento da área de baixo
col_gastos, col_vazia, col_graf = st.columns([1.5, 0.2, 1.5]) # Aumente a 'col_vazia' para encurtar os lados

with col_gastos:
    st.markdown('<div class="card-cartao-small"><b>Total a pagar:</b> R$ 1.800,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Nubank:</b> R$ 450,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Visa:</b> R$ 200,00</div>', unsafe_allow_html=True)

with col_graf:
    chart_data = pd.DataFrame({'Cat': ['Aluguel', 'Lazer', 'Comida'], 'Val': [1200, 300, 950]})
    st.bar_chart(chart_data.set_index('Cat'), height=200) # Ajuste o HEIGHT para mudar altura do gráfico
    


































