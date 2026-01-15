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
if 'categorias' not in st.session_state: 
    st.session_state.categorias = [] 

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

# --- FUNÇÃO COM CORREÇÃO DE NOME (TOPO DO SCRIPT) ---
@st.dialog("🚀 Novo Lançamento")
def modal_lancamento_categoria(categoria_nome):
    # 1. CABEÇALHO COM OPÇÃO DE CORREÇÃO
    col_tit, col_edit = st.columns([0.8, 0.2])
    
    with col_tit:
        st.subheader(f"Categoria: {categoria_nome}")
    
    with col_edit:
        # Popover para editar o nome da categoria se estiver errado
        with st.popover("✏️", help="Corrigir nome da categoria"):
            novo_nome_cat = st.text_input("Novo nome", value=categoria_nome)
            if st.button("Salvar Alteração", use_container_width=True):
                if novo_nome_cat and novo_nome_cat != categoria_nome:
                    # Atualiza na lista oficial de categorias
                    idx = st.session_state.categorias.index(categoria_nome)
                    st.session_state.categorias[idx] = novo_nome_cat
                    st.success("Nome alterado!")
                    st.rerun() # Reinicia para carregar o novo nome no formulário

    # 2. FORMULÁRIO DE LANÇAMENTO (O RESTANTE CONTINUA IGUAL)
    with st.form(key=f"form_dialog_{categoria_nome}", clear_on_submit=True):
        desc = st.text_input("Descrição da Despesa")
        
        col_tipo, col_parc = st.columns([2, 1])
        with col_tipo:
            tipo_desp = st.selectbox("Tipo", ["Variável", "Fixa"], key=f"t_d_{categoria_nome}")
        with col_parc:
            parcelas = st.number_input("Parcelas", min_value=1, value=1, key=f"p_d_{categoria_nome}")
        
        c1, c2 = st.columns([2, 4])
        with c1:
            valor = st.number_input("Valor", min_value=0.0, format="%.2f", key=f"v_d_{categoria_nome}")
        with c2:
            opcoes = [f['nome'] for f in st.session_state.formas_pagamento]
            forma_sel = st.selectbox("Pagamento", options=opcoes if opcoes else ["Dinheiro"], key=f"f_d_{categoria_nome}")
        
        data_l = st.date_input("Data", format="DD/MM/YYYY", key=f"d_d_{categoria_nome}")
        
        if st.form_submit_button("Confirmar e Salvar", use_container_width=True):
            detalhes = next((item for item in st.session_state.formas_pagamento if item["nome"] == forma_sel), None)
            
            novo_item = {
                "Categoria": categoria_nome,
                "Descrição": desc,
                "Tipo": tipo_desp,
                "Parcelas": parcelas,
                "Valor": valor,
                "Pagamento": forma_sel,
                "Data": data_l.strftime("%d/%m/%Y"),
                "Info_Pagto": detalhes
            }
            
            if 'despesas' not in st.session_state: st.session_state.despesas = []
            st.session_state.despesas.append(novo_item)
            
            st.success(f"✅ Lançamento em '{categoria_nome}' cadastrado com sucesso!")
            st.rerun()

# --- FUNÇÃO DO FORMULÁRIO DE RECEITA (TOPO DO SCRIPT) ---
@st.dialog("💰 Nova Receita")
def modal_receita_categoria(categoria_nome):
    with st.form(key=f"form_receita_{categoria_nome}", clear_on_submit=True):
        st.subheader(f"Fonte: {categoria_nome}")
        
        desc = st.text_input("Descrição da Receita (Ex: Salário Mensal)")
        
        # Layout de colunas: [2, 4] conforme seu padrão
        c1, c2 = st.columns([2, 4])
        with c1:
            valor = st.number_input("Valor Recebido", min_value=0.0, step=1.0, format="%.2f", key=f"val_r_{categoria_nome}")
        with c2:
            # Puxa as formas de pagamento cadastradas
            opcoes = [f['nome'] for f in st.session_state.formas_pagamento]
            forma = st.selectbox("Recebido via", options=opcoes if opcoes else ["Conta Corrente"], key=f"sel_r_{categoria_nome}")
        
        data_r = st.date_input("Data do Recebimento", format="DD/MM/YYYY", key=f"dat_r_{categoria_nome}")
        
        st.markdown("---")
        
        # Botão Salvar
        if st.form_submit_button("Confirmar Receita", use_container_width=True):
            nova_rec = {
                "Tipo": "Receita",
                "Categoria": categoria_nome,
                "Descrição": desc,
                "Valor": valor, 
                "Pagamento": forma,
                "Data": data_r.strftime("%d/%m/%Y")
            }
            
            # Garante que a lista de despesas/transações exista
            if 'despesas' not in st.session_state:
                st.session_state.despesas = []
            
            # Adiciona na lista geral
            st.session_state.despesas.append(nova_rec)
            
            # Mensagem de sucesso com a variável correta
            st.success(f"✅ Receita de '{categoria_nome}' cadastrada com sucesso!")
            
            # Reinicia para fechar o diálogo e atualizar a tela
            st.rerun()

# --- FUNÇÃO ATUALIZADA: GERENCIAR FORMAS DE PAGAMENTO (TOPO DO SCRIPT) ---
@st.dialog("💳 Gerenciar Formas de Pagamento")
def modal_forma_pagamento():
    with st.form(key="form_cadastro_pagamento", clear_on_submit=True):
        st.write("### Cadastrar Nova")
        
        # Inputs de texto livre conforme solicitado
        nova_f = st.text_input("Nome da Forma (Ex: Nubank)")
        tipo_forma = st.text_input("Tipo da Forma (Ex: Cartão de Crédito, Débito, Pix)")
        
        st.info("Se for Cartão de Crédito, preencha os dias abaixo. Caso contrário, deixe em 0.")
        
        col1, col2 = st.columns(2)
        with col1:
            fechamento = st.number_input("Dia Fechamento", min_value=0, max_value=31, value=0)
        with col2:
            vencimento = st.number_input("Dia Vencimento", min_value=0, max_value=31, value=0)
        
        st.markdown("---")
        
        if st.form_submit_button("Confirmar Cadastro", use_container_width=True):
            if nova_f:
                if 'formas_pagamento' not in st.session_state:
                    st.session_state.formas_pagamento = []
                
                # Salva os dados na memória
                st.session_state.formas_pagamento.append({
                    "nome": nova_f,
                    "tipo": tipo_forma,
                    "fechamento": fechamento,
                    "vencimento": vencimento
                })
                
                # Mensagem de sucesso ANTES do rerun
                st.success(f"✅ Forma de Pagamento '{nova_f}' cadastrada com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, insira o nome da forma de pagamento.")

    # --- LISTA PARA CORREÇÃO E VISUALIZAÇÃO ---
    if 'formas_pagamento' in st.session_state and st.session_state.formas_pagamento:
        st.markdown("---")
        st.write("### Formas Já Cadastradas")
        for i, item in enumerate(st.session_state.formas_pagamento):
            with st.expander(f"✅ {item['nome']} ({item['tipo']})"):
                if item['fechamento'] > 0:
                    st.write(f"📅 Fechamento: Dia {item['fechamento']}")
                    st.write(f"💰 Vencimento: Dia {item['vencimento']}")
                else:
                    st.write("ℹ️ Forma de pagamento à vista.")
                
                # Botão de remover com chave única
                if st.button("Remover", key=f"del_f_{i}", use_container_width=True):
                    nome_removido = st.session_state.formas_pagamento[i]['nome']
                    st.session_state.formas_pagamento.pop(i)
                    st.warning(f"A forma '{nome_removido}' foi removida.")
                    st.rerun()
                    

# --- 1. NAVEGAÇÃO POR BOTÕES (SIDEBAR) ---
st.sidebar.title("MENU PRINCIPAL") # Título do menu

# Criamos botões que, ao serem clicados, mudam o valor de 'selecionado' no session_state
if st.sidebar.button("📊 Painel Inicial", use_container_width=True):
    st.session_state.pagina = "Painel Inicial"

if st.sidebar.button("⚙️ Cadastros Iniciais", use_container_width=True):
    st.session_state.pagina = "Cadastros Iniciais"

if st.sidebar.button("📈 Relatórios", use_container_width=True):
    st.session_state.pagina = "Relatórios"

# Define um valor padrão caso o usuário tenha acabado de abrir o app
if 'pagina' not in st.session_state:
    st.session_state.pagina = "Painel Inicial"

# Atribuímos o valor da página à variável 'selecionado' para não quebrar seus IFs abaixo
selecionado = st.session_state.pagina

# 2. LÓGICA DE NAVEGAÇÃO
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

# --- TELA: CADASTROS INICIAIS ---
if selecionado == "Cadastros Iniciais":
    st.markdown("## ⚙️ Configurações e Cadastros")
    st.markdown("---")

    # Criamos 3 colunas principais para organizar tudo verticalmente
    col_desp, col_rec, col_pgto = st.columns([1, 1, 1])

    # --- COLUNA 1: DESPESAS ---
    with col_desp:
        st.markdown("### 🔴 Categoria Despesa")
        # Botão de Inserir no topo da coluna
        with st.popover("➕ Inserir Categoria", use_container_width=True):
            n_cat = st.text_input("Nome (Ex: Casa)", key="new_cat_desp")
            if st.button("Salvar", key="btn_save_desp", use_container_width=True):
                if n_cat and n_cat not in st.session_state.categorias:
                    st.session_state.categorias.append(n_cat)
                    st.rerun()
        
        st.write("") # Pequeno espaço
        # BOTÕES DAS CATEGORIAS CRIADAS (Aparecem logo abaixo)
        for cat in st.session_state.categorias:
            if st.button(f"🔻 {cat.upper()}", use_container_width=True, key=f"btn_d_{cat}"):
                modal_lancamento_categoria(cat)

    # --- COLUNA 2: RECEITAS ---
    with col_rec:
        st.markdown("### 🟢 Fonte de Receita")
        # Botão de Inserir no topo da coluna
        with st.popover("💰 Inserir Fonte", use_container_width=True):
            n_rec = st.text_input("Nome (Ex: Salário)", key="new_cat_rec")
            if st.button("Salvar", key="btn_save_rec", use_container_width=True):
                if 'categorias_receita' not in st.session_state:
                    st.session_state.categorias_receita = []
                if n_rec and n_rec not in st.session_state.categorias_receita:
                    st.session_state.categorias_receita.append(n_rec)
                    st.rerun()
        
        st.write("") # Pequeno espaço
        # BOTÕES DAS FONTES CRIADAS (Aparecem logo abaixo)
        if 'categorias_receita' in st.session_state:
            for cat_r in st.session_state.categorias_receita:
                if st.button(f"🔺 {cat_r.upper()}", use_container_width=True, key=f"btn_r_{cat_r}"):
                    modal_receita_categoria(cat_r)

    # --- COLUNA 3: FORMAS DE PAGAMENTO ---
    with col_pgto:
        st.markdown("### 💳 Forma Pagto/Receb")
        # Botão de Gerenciar no topo (abre o formulário suspenso que já tem a lista)
        if st.button("⚙️ Gerenciar Formas", use_container_width=True):
            modal_forma_pagamento()
        
        st.write("") # Pequeno espaço
        # LISTA SIMPLES APENAS PARA VISUALIZAR (Sem ação de botão, já que a forma é usada no formulário)
        if 'formas_pagamento' in st.session_state:
            for f in st.session_state.formas_pagamento:
                st.caption(f"✅ {f['nome']}")
























































































































































