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

    /* 2. CARDS (Conforme você ajustou: Grandes e Espaçados) */
    .card {
        padding: 20px 25px !important; 
        font-size: 20px !important;
        border-radius: 5px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        line-height: 1.1 !important;
    }
    .receita { background-color: #008080; } 
    .despesa { background-color: #B22222; } 
    .saldo   { background-color: #DAA520; } 

    /* 3. AVATAR E FRASE */
    .avatar-container {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        line-height: 1.2;
        margin-top: -5px;
    } 

    /* 4. ESTILO DA BARRA GROSSA (Corrigida a posição) */
    .barra-preta-grossa {
        border-bottom: 6px solid #000000 !important;
        margin-bottom: 20px !important;
        margin-top: 10px !important;
        display: block !important;
        width: 100% !important;

    }
   /* 5. SEGUNDA BARRA COM AFASTAMENTO DE 3CM */
    .barra-afastada {
        border-bottom: 6px solid #000000 !important; /* Mesma espessura da primeira */
        width: 100% !important;
        margin-top: 115px !important; /* Isso equivale a +- 3 centímetros */
        margin-bottom: 20px !important;
        display: block !important;

    }
    
    /* 6. ESPAÇO PARA DESCER OS CARDS */
    .espaco-cards {
        margin-top: 55px !important; /* Empurra os cards para baixo */
    }   
    

    /* 7. CAIXA DE COMBINAÇÃO (SELECTBOX) - CORRIGIDO */
    
    /* Estilo do nome 'Mês' e 'Ano' (Rótulo) */
    [data-testid="stWidgetLabel"] p {
        font-size: 18px !important; 
        font-weight: bold !important;
        color: #000000 !important;
        margin-bottom: -5px !important;
    }

    /* Largura da caixa aumentada para 170px para caber 'SETEMBRO' e 'FEVEREIRO' */
    div[data-testid="stSelectbox"] {
        width: 150px !important; 
        margin-top: 5px !important;
    }
    
    /* Centralização real do texto compensando a seta lateral */
    div[data-baseweb="select"] > div {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
        /* Adicionamos padding igual nos dois lados para o texto ficar no meio real */
        padding-left: 1px !important; 
        padding-right: 10px !important;
        height: 35px !important;
        min-height: 35px !important;
    }
    
    /* COMANDO ESPECÍFICO PARA MOVER A SETA */
    div[data-baseweb="select"] [data-testid="stSelectbox"] div:last-child {
        margin-right: -1px !important; /* Puxa a seta para a extrema direita */
    }
    /* AJUSTE PARA O TEXTO NÃO CORTAR */
    div[data-baseweb="select"] span {
        white-space: nowrap !important;
        overflow: visible !important;
        font-size: 14px !important;
    }
    
    /* Garante que o texto não tente "pular" de linha ou se esconder */
    div[data-baseweb="select"] span {
        white-space: nowrap !important;
        overflow: visible !important;
    }

    /* Cor do texto nos parágrafos gerais */
    div[data-testid="stMarkdownContainer"] p {
        color: #1E293B;
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

# --- LINHA ÚNICA ---
col_filtro, col_rec, col_desp, col_sal, col_ava = st.columns([1.2, 1.2, 1.2, 1.2, 2.5])

with col_filtro:
    meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
             "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    
    # Certifique-se de que estas linhas abaixo tenham exatamente o mesmo alinhamento
    st.selectbox("Mês", meses, index=7, key="combo_mes")
    st.selectbox("Ano", ["2024", "2025", "2026"], index=0, key="combo_ano")

st.markdown('<div class="barra-afastada"></div>', unsafe_allow_html=True)

with col_rec:
    st.markdown('<div class="espaco-cards"></div>', unsafe_allow_html=True) # ADICIONE ISSO
    st.markdown('<div class="card receita">RECEITA<br>R$ 5.000,00</div>', unsafe_allow_html=True)

with col_desp:
    st.markdown('<div class="espaco-cards"></div>', unsafe_allow_html=True) # ADICIONE ISSO
    st.markdown('<div class="card despesa">DESPESA<br>R$ 2.450,00</div>', unsafe_allow_html=True)

with col_sal:
    st.markdown('<div class="espaco-cards"></div>', unsafe_allow_html=True) # ADICIONE ISSO
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




































































