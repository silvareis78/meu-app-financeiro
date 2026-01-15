import streamlit as st # Importa a biblioteca principal do Streamlit
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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

    /* 12. REMOÇÃO DE BOTÕES +/- NO VALOR */
    div[data-testid="stNumberInputStepDown"], 
    div[data-testid="stNumberInputStepUp"] {
        display: none !important;              /* Esconde os botões de mais e menos dos campos de número */
    }
    div[data-testid="stNumberInputContainer"] input {
        padding-right: 1rem !important;        /* Ajusta o texto dentro da caixa após sumir o +/- */
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

# --- 3.FUNÇÕES PARA OS FORMULÁRIOS SUSPENSOS ---

@st.dialog("➕ Inserir Nova Despesa")
def modal_despesa():
    with st.form("form_desp", clear_on_submit=True):
        desc = st.text_input("Descrição")
        tipo_desp = st.selectbox("Tipo de Despesa", ["Variável", "Fixa"])
        
        # AJUSTE DE LARGURA: [1, 4] significa que a Forma de Pagamento é 4x maior que o Valor.
        # Se o nome "Forma de Pagamento" ainda quebrar, mude o 4 para 5 ou 6.
        col_v, col_f = st.columns([1, 4]) 
        
        with col_v:
            # O 'step=1.0' faz o CSS identificar que deve esconder os botões +/-
            valor = st.number_input("Valor", min_value=0.0, format="%.2f", step=1.0)
            
        with col_f:
            opcoes_f = [f['nome'] for f in st.session_state.formas_pagamento]
            # Esta caixa vai crescer conforme o número que você colocou lá no st.columns
            forma_s = st.selectbox("Forma de Pagamento", options=opcoes_f if opcoes_f else ["Dinheiro"])
        
        st.markdown("---") # Linha de separação
        
        col_parc, col_data = st.columns(2) # Divide a linha de baixo ao meio (50% cada)
        info_f = next((f for f in st.session_state.formas_pagamento if f['nome'] == forma_s), None)
        
        parcelas = 1
        if info_f and "cartão" in str(info_f.get('tipo', '')).lower():
            parcelas = col_parc.number_input("Parcelas", 1, 12, 1, step=1)
        
        data_l = col_data.date_input("Data de Lançamento", format="DD/MM/YYYY")
        
        # O botão 'Salvar' vai obedecer automaticamente a cor que você colocou no Item 13 do CSS acima
        if st.form_submit_button("Salvar Despesa", use_container_width=True):
            st.session_state.despesas.append({
                "desc": desc, "tipo_desp": tipo_desp, "valor": valor, 
                "forma": forma_s, "data": data_l, "vencimento": data_l, "parcelas": parcelas
            })
            st.rerun()
            
@st.dialog("💰 Inserir Nova Receita")
def modal_receita():
    with st.form("form_rec", clear_on_submit=True):
        desc_r = st.text_input("Descrição da Receita")
        
        # Ajustado para [2, 4] para o Valor não ficar espremido
        col_v, col_f = st.columns([2, 3])
        valor_r = col_v.number_input("Valor", min_value=0.0, format="%.2f", step=0.0)
        
        opcoes_f = [f['nome'] for f in st.session_state.formas_pagamento]
        forma_r = col_f.selectbox("Recebido via", options=opcoes_f if opcoes_f else ["Dinheiro"])
        
        data_r = st.date_input("Data do Recebimento", format="DD/MM/YYYY")
        
        if st.form_submit_button("Salvar Receita", use_container_width=True):
            st.session_state.receitas.append({
                "desc": desc_r, "valor": valor_r, "forma": forma_r, "data": data_r
            })
            st.rerun()

@st.dialog("💳 Cadastrar Forma de Pagamento")
def modal_pagamento():
    with st.form("form_pagto", clear_on_submit=True):
        # 1. Nome da Forma
        nome_f = st.text_input("Nome da Forma de Pagamento")
        
        # 2. Tipo de Pagamento (Texto livre)
        tipo_f = st.text_input("Tipo de Pagamento (Ex: Cartão de Crédito, Débito, PIX)")
        
        # 3. Nome do Banco
        banco = st.text_input("Nome do Banco")
        
        st.markdown("---")
        st.write("📅 **Configuração de Vencimento**")
        
        # 4. Campos de Fechamento e Vencimento (CORRIGIDOS)
        col_fech, col_venc = st.columns(2)
        
        # Mudamos o step para 1 para evitar o erro de tipos mistos
        dia_fechamento = col_fech.number_input("Dia de Fechamento", min_value=1, max_value=31, value=1, step=1)
        dia_vencimento = col_venc.number_input("Dia de Vencimento", min_value=1, max_value=31, value=10, step=1)
        
        # O botão de salvar DEVE estar dentro do 'with st.form'
        if st.form_submit_button("Salvar Forma de Pagamento", use_container_width=True):
            if nome_f and tipo_f:
                st.session_state.formas_pagamento.append({
                    "nome": nome_f, 
                    "tipo": tipo_f, 
                    "banco": banco,
                    "fechamento": dia_fechamento, 
                    "vencimento": dia_vencimento
                })
                st.success(f"Forma '{nome_f}' salva!")
                st.rerun()
            else:
                st.warning("Preencha o Nome e o Tipo de Pagamento.")
            
# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown("## ☰ Navegação")
    st.divider()

    # Voltamos ao seu rádio original, sem scripts de fechamento
    selecionado = st.radio(
        "Selecione a tela:",
        options=["Painel Inicial", "Despesa", "Receita", "Cartões", "Cadastros Iniciais", "Configurações"],
        key="menu_principal"
    )
    
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







































































































































