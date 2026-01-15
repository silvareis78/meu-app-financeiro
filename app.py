import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Financeiro Pro", layout="wide", initial_sidebar_state="auto")

# 2. CSS 
st.markdown("""
    <script>
    function fecharBotoes() {
        // Seleciona botões de menu, botões de deploy e footer do Streamlit
        const botoes = document.querySelectorAll('button[title="Manage app"], .stActionButton, .stDeployButton, footer, #MainMenu, header');
        // Remove cada elemento encontrado para limpar a tela
        botoes.forEach(el => el.remove());
    }
    // Executa a função a cada 500 milissegundos para garantir que os botões não voltem
    setInterval(fecharBotoes, 500);
    </script>

    <style>
    /* 1. CONFIGURAÇÃO GERAL DA PÁGINA */
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; } /* Ajusta o respiro do topo */
    header, footer { visibility: hidden; display: none !important; } /* Esconde o cabeçalho e rodapé padrão */

    /* 2. CARDS PRINCIPAIS (RECEITA, DESPESA, SALDO) */
    .card {
        padding: 30px 45px !important;        /* Tamanho interno do card (espaçamento) */
        font-size: 20px !important;           /* Tamanho da fonte do texto principal */
        border-radius: 5px;                    /* Arredondamento das bordas */
        color: white !important;               /* Cor do texto (sempre branco) */
        font-weight: bold;                     /* Texto em negrito */
        text-align: center;                    /* Centraliza o texto horizontalmente */
        line-height: 1.1 !important;           /* Espaçamento entre as linhas do texto */
    }
    .receita { background-color: #008080; }    /* Cor Verde Petróleo para Receita */
    .despesa { background-color: #B22222; }    /* Cor Vermelha para Despesa */
    .saldo   { background-color: #DAA520; }    /* Cor Dourada para Saldo */

    /* 3. CORES DOS CARDS VERTICAIS (DETALHAMENTO) */
    .card-pagar { background-color: #E65100 !important; }    /* Laranja Sólido (A Pagar) */
    .card-prevista { background-color: #374151 !important; } /* Grafite Sólido (Prevista) */
    .card-cartao { background-color: #0747A6 !important; }   /* Azul Royal (Cartões) */

    /* 4. ESTILO DOS CARDS VERTICAIS (EM FILA) */
    .card-vertical {
        /* --- AJUSTE DE COMPRIMENTO (ALTURA) --- */
        display: flex !important;               /* Ativa o modo flexível */
        flex-direction: column !important;      /* Empilha o nome e o valor um sob o outro */
        justify-content: center !important;     /* Centraliza verticalmente (meio da altura) */
        align-items: center !important;         /* Centraliza horizontalmente (meio da largura) */
        text-align: center !important;          /* Garante que o texto de cada linha fique no centro */

        /* --- DIMENSÕES (Ajuste conforme sua preferência) --- */
        width: 200px !important;                /* Largura do card */
        height: 90px !important;               /* Altura fixa para dar espaço às duas linhas */

        /* --- ESTILO VISUAL --- */
        border-radius: 10px !important;         /* Bordas arredondadas */
        text-align: center !important;          /* Alinha o texto ao centro */
        margin-bottom: 12px !important;         /* Espaço entre um card e outro */
        font-size: 25px !important;             /* Texto levemente maior */
        font-weight: 900 !important;            /* Negrito máximo */
        color: #FFFFFF !important;              /* Texto branco */
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3) !important; /* Sombra */
    }

    /* 5. AVATAR E MENSAGEM DO TOPO */
    .avatar-container {
        display: flex;                         /* Alinha imagem e texto lado a lado */
        align-items: center;                   /* Centraliza verticalmente foto e texto */
        gap: 6px;                              /* Espaço entre a foto e a frase */
        font-size: 10px;                       /* Tamanho pequeno da fonte */
        line-height: 1.1;                      /* Altura da linha do texto */
        margin-top: 15px;                      /* Distância do topo */
        color: #1E293B !important;             /* Cor cinza escuro para o texto */
    }
    .img-avatar {
        width: 30px !important;                /* Largura da imagem do avatar */
        height: 30px !important;               /* Altura da imagem do avatar */
        border-radius: 50% !important;         /* Faz a imagem ficar redonda */
        object-fit: cover !important;          /* Não distorce a imagem ao redimensionar */
    }

    /* 6. BARRAS DIVISÓRIAS (PRETAS) */
    .barra-preta-grossa {
        border-bottom: 6px solid #000000 !important; /* Estilo da primeira barra */
        margin-bottom: 20px !important;               /* Espaço abaixo da barra */
        margin-top: 10px !important;                  /* Espaço acima da barra */
        display: block !important;                    /* Garante visualização total */
        width: 100% !important;                       /* Largura total da tela */
    }
    .barra-afastada {
        border-bottom: 6px solid #000000 !important; /* Estilo da segunda barra */
        width: 100% !important;                       /* Largura total da tela */
        margin-top: 70px !important;                  /* Distância de 3cm do conteúdo acima */
        margin-bottom: 20px !important;               /* Espaço abaixo da barra */
        display: block !important;                    /* Garante visualização total */
    }

    /* 7. ESPAÇAMENTO COMPLEMENTAR */
    .espaco-cards {
        margin-top: 55px !important;                  /* Empurra os cards principais para baixo */
    }   

    /* 8. CAIXAS DE SELEÇÃO (MÊS E ANO) */
    [data-testid="stWidgetLabel"] p {
        font-size: 18px !important;                   /* Tamanho da palavra 'Mês' e 'Ano' */
        font-weight: bold !important;                 /* Títulos em negrito */
        color: #000000 !important;                    /* Cor preta sólida */
        margin-bottom: -5px !important;               /* Aproxima o título da caixa */
    }
    div[data-testid="stSelectbox"] {
        width: 150px !important;                      /* Largura da caixa de seleção */
        margin-top: 5px !important;                   /* Ajuste de posição */
    }
    div[data-baseweb="select"] > div {
        text-align: center !important;                /* Centraliza o texto do mês/ano */
        justify-content: center !important;           /* Alinha ao centro */
        display: flex !important;                     /* Ativa o modo flexível */
        align-items: center !important;               /* Centralização vertical */
        padding-left: 1px !important;                 /* Ajuste fino lateral */
        padding-right: 10px !important;               /* Espaço para a seta */
        height: 35px !important;                      /* Altura da caixa */
        min-height: 35px !important;                  /* Altura mínima da caixa */
    }
    div[data-baseweb="select"] [data-testid="stSelectbox"] div:last-child {
        margin-right: -1px !important;                /* Cola a seta no canto direito */
    }
    div[data-baseweb="select"] span {
        white-space: nowrap !important;               /* Impede quebra de linha no texto */
        overflow: visible !important;                 /* Permite ver o texto todo */
        font-size: 14px !important;                   /* Tamanho da fonte interna */
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #1E293B;                               /* Cor padrão para parágrafos Markdown */
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

# --- 5. DETALHAMENTO DE DESPESAS ---
st.markdown('<p class="titulo-secao">Detalhamento de Despesas</p>', unsafe_allow_html=True)

# Verifique se NÃO existe nenhum espaço antes de 'st.markdown' abaixo:
st.markdown('<div class="card-vertical card-pagar"><b>DESPESA A PAGAR<br>R$ 1.200,00</b></div>', unsafe_allow_html=True)
st.markdown('<div class="card-vertical card-prevista"><b>DESPESA PREVISTA<br>R$ 800,00</b></div>', unsafe_allow_html=True)
st.markdown('<div class="card-vertical card-cartao"><b>NUBANK<br>R$ 450,00</b></div>', unsafe_allow_html=True)
st.markdown('<div class="card-vertical card-cartao"><b>INTER<br>R$ 320,00</b></div>', unsafe_allow_html=True)
st.markdown('<div class="card-vertical card-cartao"><b>OUTROS<br>R$ 150,00</b></div>', unsafe_allow_html=True)





































































































