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
    /* 1. CONFIGURAÇÃO GERAL */
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; }
    header, footer { visibility: hidden; display: none !important; }

    /* 2. CARDS IGUAIS À FOTO */
    .card {
        padding: 10px 25px !important; 
        font-size: 13px !important;
        border-radius: 5px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        line-height: 1.1 !important;
    }
    .receita { background-color: #008080; } 
    .despesa { background-color: #B22222; } 
    .saldo   { background-color: #DAA520; } 

    /* 3. SELETORES (Mês/Ano) */
    div[data-testid="stSelectbox"] { margin-top: -15px !important; }
    div[data-baseweb="select"] { height: 35px !important; min-height: 35px !important; }

    /* 4. AVATAR E FRASE LATERAL */
    .avatar-container {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        line-height: 1.2;
        margin-top: -5px;
    } 

    /* 5. ESTILO DA BARRA GROSSA */
    .barra-preta-grossa {
        border-bottom: 6px solid #000000 !important; /* !important garante que apareça */
        margin-bottom: 20px !important;
        margin-top: 10px !important;
        display: block !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
t1, t2 = st.columns([5, 1])
with t1: 
    st.markdown("## 🏠 Painel Inicial")
with t2: 
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown('<div class="barra-preta-grossa"></div>', unsafe_allow_html=True)

# --- LINHA ÚNICA (REPLICANDO A FOTO) ---
# [Filtros, Receita, Despesa, Saldo, Avatar]
# AJUSTE DE LARGURA: Altere os números abaixo para encurtar ou esticar cada item
col_filtro, col_rec, col_desp, col_sal, col_ava = st.columns([0.8, 1.2, 1.2, 1.2, 2.5])

with col_filtro:
    # Mês e Ano bem compactos
    st.selectbox("", ["AGOSTO"], key="mes_f", label_visibility="collapsed")
    st.selectbox("", ["2024"], key="ano_f", label_visibility="collapsed")

with col_rec:
    # Card de Receita (Verde Água)
    st.markdown('<div class="card receita">RECEITA<br>R$ 5.000,00</div>', unsafe_allow_html=True)

with col_desp:
    # Card de Despesa (Vermelho)
    st.markdown('<div class="card despesa">DESPESA<br>R$ 2.450,00</div>', unsafe_allow_html=True)

with col_sal:
    # Card de Saldo (Amarelo/Ouro)
    st.markdown('<div class="card saldo">SALDO<br>R$ 2.550,00</div>', unsafe_allow_html=True)

with col_ava:
    # Avatar e frase lateral colados nos cards
    st.markdown("""
        <div class="avatar-container">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="35" style="border-radius: 50%;">
            <div>Opa! Você gastou <b>49%</b> do que recebeu!</div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)


# --- SEÇÃO DE DESPESAS (PARTE DE BAIXO) ---
st.markdown('<div class="espacamento-secao"></div>', unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 18px;'>DESPESA</h3>", unsafe_allow_html=True)
st.markdown('<div class="barra-preta-fina"></div>', unsafe_allow_html=True)

# Layout de duas colunas para as contas e o gráfico
# [Cards de Contas, Espaço, Gráfico]
col_gastos, col_espaco, col_graf = st.columns([2, 0.5, 2])

with col_gastos:
    st.markdown('<div class="card-cartao-small"><b>Total a pagar:</b> R$ 1.800,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Nubank:</b> R$ 450,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-cartao-small">💳 <b>Visa:</b> R$ 200,00</div>', unsafe_allow_html=True)

with col_graf:
    chart_data = pd.DataFrame({'Cat': ['Aluguel', 'Lazer', 'Comida'], 'Val': [1200, 300, 950]})
    st.bar_chart(chart_data.set_index('Cat'), height=200, color="#000000")
















































