import streamlit as st
import pandas as pd 
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Financeiro Pro", layout="wide")

# 2. CSS "MODO INVISÍVEL" + JAVASCRIPT PARA REMOVER BOTÕES TEIMOSOS
st.markdown("""
    <script>
    // Função para remover os botões chatos do Streamlit no celular
    function fecharBotoes() {
        const botoes = document.querySelectorAll('button[title="Manage app"], .stActionButton, .stDeployButton, footer, #MainMenu, header');
        botoes.forEach(el => el.remove());
        
        // Remove indicadores de status no canto inferior
        const status = document.querySelectorAll('[data-testid="stStatusWidget"]');
        status.forEach(el => el.remove());
    }
    // Executa a cada meio segundo para garantir que eles não voltem
    setInterval(fecharBotoes, 500);
    </script>

    <style>
    /* Cards em Gradiente */
    .card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    .receita { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); }
    .despesa { background: linear-gradient(135deg, #dc3545 0%, #ff4b5c 100%); }
    .saldo { background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); }

    /* Barra Vermelha de Divisão */
    .barra-vermelha {
        border-left: 5px solid #dc3545;
        padding-left: 10px;
        font-weight: bold;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    _, col_central, _ = st.columns([0.05, 0.9, 0.05])
    
    with col_central:
        st.markdown('<p class="logo-text">Meu App Financeiro</p>', unsafe_allow_html=True)
        email = st.text_input("E-mail", placeholder="seuemail@gmail.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        
        if st.button("Acessar"):
            if senha == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Senha ou e-mail incorretos.")

# LÓGICA DE LOGIN (Mantida para segurança)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # (O código de login simplificado que já aprovamos vai aqui)
    st.markdown("<h2 style='text-align: center;'>Meu App Financeiro</h2>", unsafe_allow_html=True)
    senha = st.text_input("Senha", type="password")
    if st.button("Acessar"):
        if senha == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ---------------------------------------------------------
# DASHBOARD PRINCIPAL
# ---------------------------------------------------------

# Barra de Topo: Título e Sair
t1, t2 = st.columns([5, 1])
with t1:
    st.subheader("🏠 Painel Inicial")
with t2:
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown('<div class="divisor"></div>', unsafe_allow_html=True)

# Filtros e Cards
col_filtros, col_cards, col_avatar = st.columns([1, 2.5, 1.5])

with col_filtros:
    st.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], key="mes")
    st.selectbox("Ano", ["2025", "2026", "2027"], key="ano")

with col_cards:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card receita">Receita<br>R$ 5.000,00</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card despesa">Despesa<br>R$ 2.450,00</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card saldo">Saldo<br>R$ 2.550,00</div>', unsafe_allow_html=True)

with col_avatar:
    st.markdown("""
        <div class="info-container">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="60" style="border-radius: 50%;">
            <p style="margin-top:10px; color:#64748B; font-size:14px;">Você gastou <b>49%</b> da sua receita este mês.</p>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)

# Área de Despesas Detalhadas
st.markdown('<div class="barra-vermelha">DESCRIÇÃO DESPESA</div>', unsafe_allow_html=True)

col_detalhes, col_grafico = st.columns([2, 2])

with col_detalhes:
    # Cards de Totais
    st.info("📌 Total a pagar no mês: **R$ 1.800,00**")
    st.warning("💳 Cartão Nubank: **R$ 450,00**")
    st.warning("💳 Cartão Visa: **R$ 200,00**")

with col_grafico:
    # Gráfico Simples de Exemplo
    chart_data = pd.DataFrame({'Categorias': ['Aluguel', 'Lazer', 'Comida'], 'Valores': [1200, 300, 950]})
    st.bar_chart(chart_data.set_index('Categorias'))

# Menu Lateral (Configurado com ícones)
with st.sidebar:
    st.title("Menu")
    st.button("📊 Dashboard")
    st.button("💸 Lançamentos")
    st.button("⚙️ Configurações")
    





