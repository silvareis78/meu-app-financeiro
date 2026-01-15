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
        padding: 30px 45px !important; 
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

    /* Cores Fortes e Sólidas para tirar o esbranquiçado */
    .card-pagar { background-color: #E65100 !important; } 
    .card-prevista { background-color: #374151 !important; } 
    .card-cartao { background-color: #0747A6 !important; } 

    /* CORREÇÃO: Faltava a abertura de chave '{' após .card-vertical */
    .card-vertical {
        padding: 12px 20px !important;
        border-radius: 10px !important;
        text-align: left !important;
        margin-bottom: 10px !important;
        width: 350px !important;
        font-size: 20px !important; 
        font-weight: 900 !important; 
        color: #FFFFFF !important;  
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3) !important;
        display: block !important;
    }

    /* 3. AVATAR E FRASE (CORRIGIDO ERRO DE DIGITAÇÃO EM 'COLOR') */
    .avatar-container {
        display: flex;
        align-items: center;
        gap: 6px;             
        font-size: 10px;       
        line-height: 1.1;
        margin-top: 15px;
        color: #1E293B !important; /* Estava 'olor' */
    }

    .img-avatar {
        width: 30px !important;  
        height: 30px !important;
        border-radius: 50% !important; 
        object-fit: cover !important;
    }

    /* 4. ESTILO DA BARRA GROSSA */
    .barra-preta-grossa {
        border-bottom: 6px solid #000000 !important;
        margin-bottom: 20px !important;
        margin-top: 10px !important;
        display: block !important;
        width: 100% !important;
    }

    /* 5. SEGUNDA BARRA COM AFASTAMENTO */
    .barra-afastada {
        border-bottom: 6px solid #000000 !important; 
        width: 100% !important;
        margin-top: 70px !important; 
        margin-bottom: 20px !important;
        display: block !important;
    }
    
    /* 6. ESPAÇO PARA DESCER OS CARDS */
    .espaco-cards {
        margin-top: 55px !important; 
    }   

    /* 7. CAIXA DE COMBINAÇÃO (SELECTBOX) */
    [data-testid="stWidgetLabel"] p {
        font-size: 18px !important; 
        font-weight: bold !important;
        color: #000000 !important;
        margin-bottom: -5px !important;
    }

    div[data-testid="stSelectbox"] {
        width: 150px !important; 
        margin-top: 5px !important;
    }
    
    div[data-baseweb="select"] > div {
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
        padding-left: 1px !important; 
        padding-right: 10px !important;
        height: 35px !important;
        min-height: 35px !important;
    }
    
    div[data-baseweb="select"] [data-testid="stSelectbox"] div:last-child {
        margin-right: -1px !important; 
    }

    div[data-baseweb="select"] span {
        white-space: nowrap !important;
        overflow: visible !important;
        font-size: 14px !important;
    }

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
col_espaco, col_filtro, col_espaco, col_rec, col_espaco, col_desp, col_espaco, col_sal, col_espaco, col_ava, col_espaco = st.columns([0.3, 1, 0.3, 1.3, 0.3, 1.3, 0.3, 1.3, 0.3, 2, 0.3])

with col_filtro:
    meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
             "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    
    # Certifique-se de que estas linhas abaixo tenham exatamente o mesmo alinhamento
    st.selectbox("Mês:", meses, index=7, key="combo_mes")
    st.selectbox("Ano:", ["2024", "2025", "2026"], index=0, key="combo_ano")

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
    # Avatar e frase 
    st.markdown("""
        <div class="avatar-container">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="img-avatar">
            <div>Opa! Você gastou <b>49%</b> do que recebeu!</div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(0.49)


# --- 5. DETALHAMENTO DE DESPESAS (ABAIXO DA BARRA) ---
st.markdown('<p class="titulo-secao">Detalhamento de Despesas</p>', unsafe_allow_html=True)

    st.markdown('<div class="card card-pagar">DESPESA A PAGAR<br>R$ 1.200,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card card-prevista">DESPESA PREVISTA<br>R$ 800,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card card-cartao">NUBANK<br>R$ 450,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card card-cartao">INTER<br>R$ 320,00</div>', unsafe_allow_html=True)
    st.markdown('<div class="card card-cartao">OUTROS<br>R$ 150,00</div>', unsafe_allow_html=True)






























































































