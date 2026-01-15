import streamlit as st # Importa a biblioteca principal do Streamlit
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Verificação inicial: se não existir a lista de categorias na memória, ele cria uma vazia
if 'categorias' not in st.session_state:
    st.session_state.categorias = [] # Lista que armazenará os nomes das suas categorias

# Inicializa as listas de dados se não existirem
if 'formas_pagamento' not in st.session_state:
    st.session_state.formas_pagamento = []
if 'despesas' not in st.session_state:
    st.session_state.despesas = []
if 'receitas' not in st.session_state:
    st.session_state.receitas = []
    
# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="App Financeiro") # Define layout largo e título da aba

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
    
    function recolherMenu() {
        var v_document = window.parent.document;
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
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; } /* Ajusta o respiro do topo da página */
    footer { visibility: hidden; display: none !important; } /* Esconde o rodapé 'Made with Streamlit' */
    header { background-color: transparent !important; border: none !important; } /* Deixa o cabeçalho invisível */
    
    /* 2. CARDS PRINCIPAIS */
    .card {
        padding: 30px 45px !important;        /* Aumente/diminua aqui para mudar o tamanho interno dos cards superiores */
        font-size: 20px !important;           /* Altera o tamanho da letra do valor nos cards */
        border-radius: 5px;                    /* Arredondamento das quinas dos cards */
        color: white !important;               /* Cor da letra sempre branca */
        font-weight: bold;                     /* Deixa o texto em negrito */
        text-align: center;                    /* Centraliza o texto */
        line-height: 1.1 !important;           
    }
    .receita { background-color: #008080; }    /* Mude aqui para trocar a cor do card de Receita */
    .despesa { background-color: #B22222; }    /* Mude aqui para trocar a cor do card de Despesa */
    .saldo   { background-color: #DAA520; }    /* Mude aqui para trocar a cor do card de Saldo */

    /* 3. CORES DOS CARDS VERTICAIS */
    .card-pagar { background-color: #E65100 !important; }    /* Cor do card 'A Pagar' */
    .card-prevista { background-color: #374151 !important; } /* Cor do card 'Prevista' */
    .card-cartao { background-color: #0747A6 !important; }   /* Cor do card 'Cartões' */

    /* 4. ESTILO DOS CARDS VERTICAIS */
    .card-vertical {
        padding: 12px 20px !important;         /* Espaço interno dos cards de detalhamento */
        border-radius: 10px !important;        /* Arredondamento */
        text-align: left !important;           
        margin-bottom: 10px !important;        /* Espaço entre um card e outro na vertical */
        width: 350px !important;               /* Largura do card (ajuste se ficar muito largo no PC) */
        font-size: 20px !important;            
        font-weight: 900 !important;            
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3) !important; /* Sombra preta suave */
        display: block !important;             
    }

    /* 5. AVATAR E MENSAGEM */
    .avatar-container { display: flex; align-items: center; gap: 6px; margin-top: 15px; }
    .img-avatar { width: 30px !important; height: 30px !important; border-radius: 50% !important; }

    /* 6. BARRAS DIVISÓRIAS */
    .barra-preta-grossa { border-bottom: 6px solid #000000 !important; margin-bottom: 20px !important; width: 100% !important; }
    .barra-afastada { border-bottom: 6px solid #000000 !important; margin-top: 70px !important; width: 100% !important; }

    /* 8. CAIXAS DE SELEÇÃO (MÊS E ANO) */
    [data-testid="stWidgetLabel"] p {
        font-size: 18px !important;            /* Tamanho do rótulo (ex: 'Descrição', 'Valor') */
        font-weight: bold !important;          /* Deixa os rótulos em negrito */
        color: #000000 !important;             /* Cor dos rótulos em preto */
        white-space: nowrap !important;        /* IMPEDE QUEBRA DE LINHA: Mantém o texto em uma linha só */
    }
    
    /* LARGURA FIXA PARA MÊS/ANO NO MENU LATERAL */
    div[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
        width: 150px !important;               /* Mude aqui se quiser o Mês e Ano mais largos ou estreitos */
    }

    /* CENTRALIZAÇÃO DO TEXTO DENTRO DAS CAIXAS */
    div[data-baseweb="select"] > div {
        text-align: center !important;                
        height: 35px !important;               /* Altura das caixas de seleção */
    }

    /* 11. BOTÃO DO MENU (3 BARRAS) */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #000000 !important;  /* Cor de fundo do botão do menu no mobile */
        border-radius: 10px !important;
        width: 50px !important;
        height: 50px !important;
    }
    [data-testid="stSidebarCollapsedControl"] button { color: white !important; }

    /* 12. REMOÇÃO TOTAL DE BOTÕES +/- E AJUSTE DE BORDA */
    /* Remove os botões de incremento e decremento (Sinais de + e -) */
    div[data-testid="stNumberInputStepDown"], 
    div[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"],
    .step-down, .step-up {
        display: none !important; /* Esconde os botões */
    }

    /* Remove o espaço extra que os botões ocupavam e centraliza o texto */
    div[data-testid="stNumberInputContainer"] input {
        padding-right: 10px !important; /* Ajusta o espaço interno à direita */
        -moz-appearance: textfield !important; /* Remove setas no Firefox */
    }

    /* Remove as setinhas padrão que o navegador às vezes coloca */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none !important;
        margin: 0 !important;
    }

    /* 13. ESTILO DO BOTÃO SALVAR (BOTÃO DE FORMULÁRIO) */
    div.stFormSubmitButton > button {
        background-color: #2E7D32 !important;  /* COR DO BOTÃO: Altere este código para mudar a cor do botão Salvar */
        color: white !important;               /* Cor do texto do botão */
        font-weight: bold !important;          
        border-radius: 8px !important;         /* Arredondamento do botão */
        height: 3.5rem !important;             /* Altura do botão */
        width: 100% !important;                /* Faz o botão ocupar a largura toda do formulário */
        border: none !important;               /* Remove bordas feias */
    }
    div.stFormSubmitButton > button:hover {
        background-color: #1B5E20 !important;  /* Cor de quando você passa o mouse por cima */
    }
    </style>
""", unsafe_allow_html=True)

# --- NOVO BLOCO: CADASTROS E CATEGORIAS ---

# Título Principal no topo
st.markdown("## ⚙️ Cadastros Iniciais")
st.markdown("---") # Linha horizontal para separar o título do conteúdo

# Criando colunas para organizar os botões de cadastro
# [1, 1, 1] cria 3 colunas iguais. Você pode adicionar mais se precisar de outros cadastros.
col_cat, col_forma, col_vazia = st.columns([1, 1, 1])

with col_cat:
    # Botão Inserir Categoria (Usando popover para abrir a caixa de texto)
    with st.popover("➕ Inserir Categoria", use_container_width=True):
        nova_cat = st.text_input("Nome da Nova Categoria", placeholder="Ex: Mercado")
        if st.button("Salvar Categoria", use_container_width=True):
            if nova_cat and nova_cat not in st.session_state.categorias:
                st.session_state.categorias.append(nova_cat)
                st.rerun()

with col_forma:
    # Botão para Formas de Pagamento (Seguindo a mesma lógica)
    with st.popover("💳 Inserir Forma de Pagamento", use_container_width=True):
        nova_forma = st.text_input("Ex: Cartão Nubank")
        if st.button("Salvar Forma", use_container_width=True):
            # Aqui você mantém sua lógica de salvar formas de pagamento
            st.session_state.formas_pagamento.append({"nome": nova_forma})
            st.rerun()

st.write("") # Adiciona um pequeno espaço vertical (pular linha)
st.markdown("### 📂 Selecione uma Categoria para Lançar")

# --- 3.GERADOR AUTOMÁTICO DE CATEGORIAS ---
# Este bloco cria os "botões" (expansores) para cada categoria cadastrada
for cat in st.session_state.categorias:
    
    # Cada categoria vira um expansor (que parece um botão largo)
    with st.expander(f"📁 {cat.upper()}", expanded=False):
        
        # Formulário interno para a despesa
        with st.form(key=f"form_{cat}", clear_on_submit=True):
            st.write(f"Novo lançamento em **{cat}**")
            
            desc = st.text_input("Descrição da Despesa", key=f"desc_{cat}")
            
            # Layout de colunas: [1, 4] -> o 4 deixa o campo de pagamento bem largo
            c1, c2 = st.columns([1, 4])
            
            with c1:
                # 'step=1.0' garante que o sinal de +/- não apareça pelo CSS
                valor = st.number_input("Valor", min_value=0.0, step=1.0, format="%.2f", key=f"val_{cat}")
            
            with c2:
                # Puxa as formas de pagamento cadastradas no botão ao lado
                opcoes = [f['nome'] for f in st.session_state.formas_pagamento]
                forma = st.selectbox("Forma de Pagamento", options=opcoes if opcoes else ["Dinheiro"], key=f"sel_{cat}")
            
            data_l = st.date_input("Data", format="DD/MM/YYYY", key=f"dat_{cat}")

            # Botão Salvar que herda a cor VERDE do seu CSS
            if st.form_submit_button("Confirmar Lançamento", use_container_width=True):
                # Aqui você prepara os dados para a planilha
                nova_linha = {
                    "Categoria": cat,
                    "Descrição": desc,
                    "Valor": valor,
                    "Pagamento": forma,
                    "Data": data_l
                }
                # Salva na memória (e depois chamaremos a função da planilha)
                st.session_state.despesas.append(nova_linha)
                st.success(f"Lançamento em {cat} realizado!")
                st.rerun()
    
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

elif selecionado == "Cadastros Iniciais":
    st.markdown("## ⚙️ Gestão de Cadastros")

    # Botões lado a lado
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    if col_btn1.button("➕ Inserir Despesa", use_container_width=True):
        modal_despesa()

    if col_btn2.button("💰 Inserir Receita", use_container_width=True):
        modal_receita()

    if col_btn3.button("💳 Forma de Pagamento", use_container_width=True):
        modal_pagamento()

    st.divider()
    st.write("### 📋 Lançamentos Recentes")
    
    # Exibição dos Cards embaixo (Mantendo seu estilo)
    for d in reversed(st.session_state.despesas):
        st.markdown(f"""
            <div class="card-vertical card-despesa" style="background-color: #B22222; margin-bottom:10px;">
                <b>{d['desc']}</b><br>
                R$ {d['valor']:.2f} | {d['forma']}<br>
                <small>Venc: {d['vencimento'].strftime('%d/%m/%Y')}</small>
            </div>
        """, unsafe_allow_html=True)











































































































































