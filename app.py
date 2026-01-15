import streamlit as st # Importa a biblioteca principal do Streamlit

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="App Financeiro") # Define layout largo e título da aba

# 2. CSS CUSTOMIZADO
st.markdown("""
    <script>
    function fecharBotoes() {
        const itensParaEsconder = document.querySelectorAll('.stActionButton, .stDeployButton, footer, #MainMenu');
        itensParaEsconder.forEach(el => el.style.display = 'none');
        const header = document.querySelector('header');
        if (header) {
            header.style.backgroundColor = 'transparent';
            header.style.border = 'none';
        }
    }
    
    // Versão otimizada para Celular
    function recolherMenu() {
        var v_document = window.parent.document;
        // Tenta encontrar o botão de fechar (X) ou a seta do menu lateral
        var botaoFechar = v_document.querySelector('button[kind="headerNoContext"]');
        var sidebar = v_document.querySelector('[data-testid="stSidebar"]');
        
        if (sidebar && sidebar.getAttribute('aria-expanded') === 'true' && botaoFechar) {
            botaoFechar.click();
        }
    }

    setInterval(fecharBotoes, 500);
    </script>
    <style>
    /* 1. CONFIGURAÇÃO GERAL */
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; }
    
    /* Mantém o header existindo (para o botão não sumir) mas invisível */
    footer { visibility: hidden; display: none !important; } 
    header { background-color: transparent !important; border: none !important; box-shadow: none !important; }
    
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
        padding: 12px 20px !important;         /* Espaçamento interno reduzido */
        border-radius: 10px !important;        /* Bordas mais arredondadas */
        text-align: left !important;           /* Alinha o texto à esquerda */
        margin-bottom: 10px !important;        /* Espaço entre um card e outro */
        width: 350px !important;               /* Largura fixa para os cards verticais */
        font-size: 20px !important;            /* Texto grande para facilitar leitura */
        font-weight: 900 !important;            /* Negrito extra forte */
        color: #FFFFFF !important;             /* Texto branco para contraste */
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3) !important; /* Sombra para profundidade */
        display: block !important;             /* Garante que ocupem a linha toda */
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

    /* 9. Garante que o botão de abrir o menu (setinha/barras) sempre esteja visível e preto */
    button[kind="headerNoContext"] {
        display: flex !important;
        visibility: visible !important;
        color: black !important;
        background-color: transparent !important;
    } 

    /* 10. MENU LATERAL (Ajuste de fonte) */
    [data-testid="stSidebar"] { background-color: #F8FAFC !important; } /* Cor de fundo do menu */
    .stRadio > div { gap: 10px !important; } /* Espaçamento entre itens do menu */

  /* 11. BOTÃO DAS 3 BARRAS (SEMPRE VISÍVEL) */
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        z-index: 999999 !important;
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        background-color: #000000 !important; /* Fundo preto para destaque */
        border-radius: 5px !important;
        width: 40px !important;
        height: 40px !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button {
        color: white !important; /* Ícone branco */
    }

    /* 12. FORÇAR O FECHAMENTO NO CELULAR AO CLICAR */
    @media (max-width: 768px) {
        /* Garante que o menu não fique travado aberto no mobile */
        [data-testid="stSidebar"][aria-expanded="true"] {
            max-width: 80vw !important; /* Ajusta largura no celular */
        }
        
        /* O segredo: quando a página atualiza (rerun), o CSS reseta o estado do menu */
        section[data-testid="stSidebar"] {
            transition: all 0.3s ease-in-out;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MENU LATERAL (VERSÃO COM FECHAMENTO AUTOMÁTICO GARANTIDO) ---
with st.sidebar:
    st.markdown("## ☰ Navegação")
    st.divider()
    
    telas = ["Painel Inicial", "Despesa", "Receita", "Cartões", "Cadastros Iniciais", "Configurações"]
    
    if 'selecionado' not in st.session_state:
        st.session_state.selecionado = "Painel Inicial"

    for tela in telas:
        if st.button(tela, use_container_width=True, type="primary" if st.session_state.selecionado == tela else "secondary"):
            st.session_state.selecionado = tela
            st.rerun() # O RERUN é o que ativa o CSS de fechar

    selecionado = st.session_state.selecionado
    
# 4. LÓGICA DE NAVEGAÇÃO
if selecionado == "Painel Inicial":
    st.markdown("## 🏠 Painel Inicial") # Título da tela principal
    st.markdown('<div class="barra-preta-grossa"></div>', unsafe_allow_html=True) # Primeira barra preta

    # Organização do Cabeçalho (Filtros, Cards e Avatar)
    col_filtro, col_rec, col_desp, col_sal, col_vazio, col_ava = st.columns([1.2, 1.2, 1.2, 1.2, 2.5, 2.0])

    with col_filtro: # Filtros de Mês e Ano
        st.selectbox("Mês", ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], index=0)
        st.selectbox("Ano", ["2024", "2025", "2026"], index=0)

    with col_rec: # Bloco de Receita
        st.markdown('<div class="espaco-cards"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card receita">RECEITA<br>R$ 5.000,00</div>', unsafe_allow_html=True)

    with col_desp: # Bloco de Despesa
        st.markdown('<div class="espaco-cards"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card despesa">DESPESA<br>R$ 2.450,00</div>', unsafe_allow_html=True)

    with col_sal: # Bloco de Saldo
        st.markdown('<div class="espaco-cards"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card saldo">SALDO<br>R$ 2.550,00</div>', unsafe_allow_html=True)

    with col_ava: # Bloco do Avatar
        st.markdown('<div class="avatar-container"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="img-avatar"><div>Opa! Você gastou 49% do recebido!</div></div>', unsafe_allow_html=True)
        st.progress(0.49) # Barra de progresso abaixo do avatar

    st.markdown('<div class="barra-afastada"></div>', unsafe_allow_html=True) # Segunda barra (afastamento 3cm)

    # DETALHAMENTO DAS DESPESAS (Cards Verticais Centralizados)
    st.markdown("### Detalhamento de Despesas")
    st.markdown('<div class="card-vertical card-pagar"><b>DESPESA A PAGAR<br>R$ 1.200,00</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-vertical card-prevista"><b>DESPESA PREVISTA<br>R$ 800,00</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-vertical card-cartao"><b>NUBANK<br>R$ 450,00</b></div>', unsafe_allow_html=True)

elif selecionado == "Despesa":
    st.markdown("## 💸 Gestão de Despesas") # Título da tela de despesas
    st.info("Aqui você poderá cadastrar novas despesas.")

elif selecionado == "Receita":
    st.markdown("## 💰 Gestão de Receitas") # Título da tela de receitas
    st.success("Aqui você poderá cadastrar novas receitas.")

















































































































