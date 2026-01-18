import streamlit as st                                  # Ferramenta principal para criar a interface do seu site/app
import pandas as pd                                     # Serve para organizar os dados em tabelas (DataFrames)
import json                                             # Usado para transformar informações complexas (como dados do cartão) em texto
from datetime import date, datetime, timedelta          # Essencial para lidar com datas e prazos de vencimento
from streamlit_gsheets import GSheetsConnection         # Faz a ponte de ligação com o Google Sheets

# Inicia a conexão com a planilha usando as credenciais que você configurou nos Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 1.FUNÇÕES DE SALVAMENTO ---

def salvar_no_google(dados_lista, aba="Dados"):
    """Função que envia seus lançamentos (gastos/receitas) para a nuvem"""
    try:
        # Tenta ler a planilha atual para não apagar o que já foi salvo antes
        try:
            # ttl=0 garante que ele pegue os dados mais recentes da planilha, sem atraso
            df_antigo = conn.read(worksheet=aba, ttl=0)
        except:
            # Se a aba estiver vazia ou não existir, cria uma tabela em branco para começar
            df_antigo = pd.DataFrame()

        # Transforma a sua lista de novos lançamentos em uma tabela do Pandas
        df_novo = pd.DataFrame(dados_lista)
        
        # AJUSTE TÉCNICO: Converte colunas de data para texto antes de enviar
        # Isso evita que o Google Sheets dê erro de formato de data brasileiro/americano
        for col in df_novo.columns:
            if 'Data' in col or 'Vencimento' in col:
                df_novo[col] = df_novo[col].astype(str)
        
        # Junta os dados antigos com os novos, um embaixo do outro
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        
        # Comando que escreve de fato na sua planilha do Google
        conn.update(worksheet=aba, data=df_final)
        
        # Limpa a memória temporária do app para que ele mostre os dados novos imediatamente
        st.cache_data.clear() 
        
        # Mostra o balão verde de sucesso na tela
        st.success(f"☁️ Lançamento registrado com sucesso na aba {aba}!")
        return True
    except Exception as e:
        # Se algo der errado (ex: internet caiu), mostra o erro em vermelho
        st.error(f"Erro ao salvar lançamento: {e}")
        return False

def salvar_configuracoes_nuvem():
    """Função específica para salvar seus Cartões e Categorias na aba 'Config'"""
    try:
        # Pega as listas que estão na memória do app (Session State)
        categorias_desp = st.session_state.get("categorias", [])
        categorias_rec = st.session_state.get("categorias_receita", [])
        # Converte os dados dos cartões de 'lista' para 'texto JSON' para caber em uma célula
        formas_pag = [json.dumps(f) for f in st.session_state.get("formas_pagamento", [])]
        
        # Descobre qual lista é a maior para preencher as outras com vazio (evita erro de tabela torta)
        max_len = max(len(categorias_desp), len(categorias_rec), len(formas_pag), 1)
        
        # Função interna para completar espaços vazios com ""
        def ajustar_lista(lista, tamanho):
            return list(lista) + [""] * (tamanho - len(lista))

        # Monta a tabela de configurações para enviar
        df_config = pd.DataFrame({
            "Categorias_Despesa": ajustar_lista(categorias_desp, max_len),
            "Categorias_Receita": ajustar_lista(categorias_rec, max_len),
            "Detalhes_Pagamento": ajustar_lista(formas_pag, max_len)
        })
        
        # Envia para a aba 'Config' do seu Google Sheets
        conn.update(worksheet="Config", data=df_config)
        st.cache_data.clear() 
        st.success("✅ Configurações salvas com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar configurações: {e}")

def carregar_configuracoes_nuvem():
    """Lê a planilha 'Config' e traz seus Cartões e Categorias de volta para o app"""
    try:
        # Lê os dados da aba Config
        df_config = conn.read(worksheet="Config", ttl=0)
        
        if df_config is not None and not df_config.empty:
            # Se encontrar a coluna de Categorias, carrega elas para o app
            if "Categorias_Despesa" in df_config.columns:
                st.session_state.categorias = df_config["Categorias_Despesa"].dropna().replace("", pd.NA).dropna().tolist()
            
            # Se encontrar a coluna de Receitas, carrega elas também
            if "Categorias_Receita" in df_config.columns:
                st.session_state.categorias_receita = df_config["Categorias_Receita"].dropna().replace("", pd.NA).dropna().tolist()
                
            # Se encontrar os Cartões, transforma o texto JSON de volta em dados usáveis
            if "Detalhes_Pagamento" in df_config.columns:
                formas_json = df_config["Detalhes_Pagamento"].dropna().replace("", pd.NA).dropna().tolist()
                st.session_state.formas_pagamento = [json.loads(f) for f in formas_json]
    except Exception as e:
        # Se a planilha estiver vazia (primeiro uso), o app apenas inicia sem erro
        print(f"Aviso: Planilha vazia ou erro: {e}")

# --- 2.INICIALIZAÇÃO DO ESTADO (SESSION STATE) ---
# O Session State funciona como uma memória temporária do navegador. 
# Ele garante que, enquanto você navega no app, os dados não sumam a cada clique.

if 'categorias' not in st.session_state:
    # Cria a lista de categorias de DESPESA se ela ainda não existir
    st.session_state.categorias = [] 
    
    # Cria a lista de categorias de RECEITA (importante para o novo gráfico)
    st.session_state.categorias_receita = [] 
    
    # Cria a lista onde ficarão os detalhes dos cartões e formas de pagamento
    st.session_state.formas_pagamento = [] 
    
    # CHAMA A FUNÇÃO DE CARREGAMENTO:
    # Como definimos ela no Bloco 1, agora o app vai ao Google Sheets buscar 
    # tudo o que você já salvou assim que o site é aberto.
    carregar_configuracoes_nuvem()

# DICA PARA ALTERAR: Se você quiser que o app já comece com categorias fixas 
# (ex: 'Alimentação'), você poderia colocá-las dentro dos colchetes [].
            
# --- 3.FUNÇÕES DE LOGÍSTICA E NUVEM ---

def calcular_vencimento_real(data_compra, detalhes_pagto):
    """Lógica que decide se a compra cai na fatura atual ou na próxima"""
    
    # Importamos aqui dentro para garantir que o comando 'date' funcione sem erros
    import datetime 

    # Se a forma de pagamento não tiver regras de fechamento (ex: Dinheiro), 
    # a data de vencimento é o próprio dia da compra.
    if not detalhes_pagto or detalhes_pagto.get('fechamento', 0) == 0:
        return data_compra 
    
    # Extraímos o dia, mês e ano da data que você selecionou no calendário
    dia_c = data_compra.day
    mes_v = data_compra.month
    ano_v = data_compra.year
    
    # REGRA: Se o dia da compra for maior ou igual ao dia que a fatura fecha,
    # jogamos o vencimento para o mês seguinte.
    if dia_c >= detalhes_pagto['fechamento']:
        mes_v += 1
        # Se o mês passar de 12 (Dezembro), voltamos para 1 (Janeiro) e somamos 1 ano
        if mes_v > 12:
            mes_v = 1
            ano_v += 1
            
    # Retorna a data final montada. 
    # PARA ALTERAR: Se quiser que vença 2 meses depois, basta somar +2 no mes_v.
    return datetime.date(ano_v, mes_v, detalhes_pagto['vencimento'])

def salvar_no_google(dados_lista, aba="Dados"):
    """Pega os seus lançamentos e empilha na sua planilha do Google"""
    try:
        # Tenta ler o que já existe na aba (ex: 'Dados' ou 'Receitas')
        try:
            df_antigo = conn.read(worksheet=aba, ttl=0)
        except:
            # Se a aba estiver vazia, começamos do zero
            df_antigo = pd.DataFrame()

        # Transforma a sua lista de gastos/receitas em uma tabela
        df_novo = pd.DataFrame(dados_lista)
        
        # AJUSTE DE COMPATIBILIDADE: O Google Sheets prefere receber datas como 'Texto'.
        # Percorremos as colunas e, se o nome tiver 'Data' ou 'Vencimento', virá texto.
        for col in df_novo.columns:
            if 'Data' in col or 'Vencimento' in col:
                df_novo[col] = df_novo[col].astype(str)

        # Junta a tabela antiga com a nova (empilhamento)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        
        # Manda o comando final para atualizar a planilha na nuvem
        conn.update(worksheet=aba, data=df_final)
        
        # Limpa o cache para os novos dados aparecerem nos gráficos imediatamente
        st.cache_data.clear()
        return True
    except Exception as e:
        # Se houver erro (ex: falta de permissão na planilha), avisa o usuário
        st.error(f"Erro ao salvar no Google Sheets: {e}")
        return False

# --- 4.INICIALIZAÇÃO DO APP E NAVEGAÇÃO ---

# O Session State evita que o Python "esqueça" suas listas cada vez que você clica em algo.
# Este bloco garante que, ao abrir o app, tudo esteja pronto para uso.

if 'categorias' not in st.session_state:
    # Cria as gavetas vazias na memória do navegador
    st.session_state.categorias = []           # Para Gastos
    st.session_state.categorias_receita = []   # Para Ganhos
    st.session_state.formas_pagamento = []     # Para Cartões/Dinheiro
    
    # Tenta carregar as informações que já estão salvas no seu Google Sheets.
    # Isso impede que o app comece do zero toda vez que você entrar.
    carregar_configuracoes_nuvem()

# Controle de Navegação: Define qual página deve aparecer primeiro.
if 'pagina' not in st.session_state:
    # PARA ALTERAR: Se quiser que o app abra direto em "Lançamentos", 
    # basta trocar o texto abaixo para "Lançamentos".
    st.session_state.pagina = "Painel Inicial"

# DICA TÉCNICA: O 'st.session_state.pagina' funciona como um marcador de livro.
# Ele avisa ao código em qual aba do menu o usuário clicou por último.
        
# --- 5.CONFIGURAÇÃO DA PÁGINA E ESTILIZAÇÃO (CSS/JS) ---

# Define que o app usará toda a largura da tela e define o nome que aparece na aba do navegador
st.set_page_config(layout="wide", page_title="App Financeiro") 

st.markdown("""
    <script>
    // Esta função esconde botões nativos do Streamlit que poluem o visual (Deploy, MainMenu, etc)
    function fecharBotoes() {
        const itensParaEsconder = document.querySelectorAll('.stActionButton, .stDeployButton, footer, #MainMenu');
        itensParaEsconder.forEach(el => el.style.display = 'none');
        const header = document.querySelector('header');
        if (header) {
            header.style.backgroundColor = 'transparent'; // Torna o topo invisível
            header.style.border = 'none';
        }
    }
    
    // Função que tenta recolher o menu lateral automaticamente em telas menores
    function recolherMenu() {
        var v_document = window.parent.document;
        var botaoFechar = v_document.querySelector('button[kind="headerNoContext"]');
        var sidebar = v_document.querySelector('[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute('aria-expanded') === 'true' && botaoFechar) {
            botaoFechar.click();
        }
    }
    // Executa a limpeza visual a cada meio segundo para garantir que botões novos não apareçam
    setInterval(fecharBotoes, 500);
    </script>

    <style>
    /* 1. CONFIGURAÇÃO GERAL DA PÁGINA */
    /* padding-top: reduz o espaço branco no topo | margin-top: puxa o conteúdo para cima */
    .block-container { padding-top: 1rem !important; margin-top: -20px !important; } 
    footer { visibility: hidden; display: none !important; } /* Remove o rodapé original */
    header { background-color: transparent !important; border: none !important; } /* Remove a barra superior */
    
    /* 2. CARDS PRINCIPAIS (Receita, Despesa, Saldo) */
    .card {
        padding: 30px 45px !important;        /* INTERNO: Mude aqui para engordar ou emagrecer o card */
        font-size: 20px !important;           /* TEXTO: Tamanho da fonte dos valores */
        border-radius: 5px;                    /* QUINAS: Aumente para 20px se quiser mais arredondado */
        color: white !important;               /* COR DO TEXTO: Sempre branco para contraste */
        font-weight: bold;                     /* ESTILO: Texto em negrito */
        text-align: center;                    /* ALINHAMENTO: Centraliza o valor no card */
        line-height: 1.1 !important;           /* ESPAÇAMENTO: Entre linhas do texto */
    }
    .receita { background-color: #008080; }    /* COR: Verde Petróleo (Receitas) */
    .despesa { background-color: #B22222; }    /* COR: Vermelho Tijolo (Despesas) */
    .saldo   { background-color: #DAA520; }    /* COR: Dourado (Saldo Final) */

    /* 3. CORES DOS CARDS VERTICAIS (Detalhamento) */
    .card-pagar { background-color: #E65100 !important; }    /* Laranja escuro */
    .card-prevista { background-color: #374151 !important; } /* Cinza grafite */
    .card-cartao { background-color: #0747A6 !important; }   /* Azul royal */

    /* 4. ESTILO DOS CARDS VERTICAIS */
    .card-vertical {
        padding: 12px 20px !important;         /* Tamanho interno */
        border-radius: 10px !important;        /* Bordas arredondadas */
        text-align: left !important;           /* Texto alinhado à esquerda */
        margin-bottom: 10px !important;        /* DISTÂNCIA: Espaço para o card de baixo */
        width: 350px !important;               /* LARGURA: Tamanho fixo do card lateral */
        font-size: 20px !important;            
        font-weight: 900 !important;           
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3) !important; /* Sombra para dar profundidade */
        display: block !important;             
    }

    /* 5. AVATAR E MENSAGENS DE BOAS-VINDAS */
    .avatar-container { display: flex; align-items: center; gap: 6px; margin-top: 15px; }
    .img-avatar { width: 30px !important; height: 30px !important; border-radius: 50% !important; }

    /* 6. BARRAS DIVISÓRIAS (Linhas Pretas) */
    /* border-bottom: grossura da linha | margin: distância para os outros itens */
    .barra-preta-grossa { border-bottom: 6px solid #000000 !important; margin-bottom: 20px !important; width: 100% !important; }
    .barra-afastada { border-bottom: 6px solid #000000 !important; margin-top: 70px !important; width: 100% !important; }

    /* 8. LABELS (Nomes dos campos de digitação como 'Descrição', 'Valor') */
    [data-testid="stWidgetLabel"] p {
        font-size: 18px !important;            /* Tamanho da letra */
        font-weight: bold !important;          /* Negrito */
        color: #000000 !important;             /* Cor preta */
        white-space: nowrap !important;        /* Não deixa o nome quebrar em duas linhas */
    }
    
    /* 9. LARGURA DOS SELECTBOX (Mês e Ano no Menu) */
    div[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
        width: 150px !important;               /* Mude para 200px se quiser que fiquem maiores */
    }

    /* 10. CAIXAS DE SELEÇÃO (Combobox) */
    div[data-baseweb="select"] > div {
        text-align: center !important;         /* Centraliza o texto escolhido */
        height: 35px !important;               /* Altura da caixa onde se clica */
    }

    /* 11. BOTÃO DO MENU MOBILE (3 Barras) */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #000000 !important;  /* Fundo preto para destaque no celular */
        border-radius: 10px !important;
        width: 50px !important;
        height: 50px !important;
    }
    [data-testid="stSidebarCollapsedControl"] button { color: white !important; }

    /* 12. CAMPOS DE NÚMERO (Remoção dos sinais de + e -) */
    div[data-testid="stNumberInputStepDown"], 
    div[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none !important; /* Esconde os botões laterais de aumentar/diminuir */
    }

    div[data-testid="stNumberInputContainer"] input {
        padding-right: 10px !important; /* Ajusta o texto dentro da caixa sem os botões */
    }

    /* 13. BOTÃO SALVAR (O botão que fica dentro dos Formulários) */
    div.stFormSubmitButton > button {
        background-color: #2E7D32 !important;  /* COR: Verde Floresta */
        color: white !important;               /* Texto branco */
        font-weight: bold !important;          
        border-radius: 8px !important;         /* Bordas suavemente arredondadas */
        height: 3.5rem !important;             /* Altura (grande para facilitar o toque) */
        width: 100% !important;                /* Ocupa a largura total da coluna */
        border: none !important;               
    }
    div.stFormSubmitButton > button:hover {
        background-color: #1B5E20 !important;  /* Cor quando passa o mouse (Verde Escuro) */
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. MODAL DE LANÇAMENTO (JANELA FLUTUANTE) ---

@st.dialog("🚀 Novo Lançamento")
def modal_lancamento_categoria(categoria_nome):
    """
    PARA QUE SERVE: Cadastro de despesas com ajuste de fuso horário.
    """
    import datetime
    import pytz # Certifique-se de que o pytz está no seu requirements.txt

    # 1. GARANTE QUE O CONTADOR EXISTE
    if 'cont_lanc' not in st.session_state:
        st.session_state.cont_lanc = 0

    # --- AJUSTE DE DATA (FUSO HORÁRIO BRASIL) ---
    fuso_br = pytz.timezone('America/Sao_Paulo')
    data_hoje = datetime.datetime.now(fuso_br).date()

    # --- CABEÇALHO COM EDIÇÃO ---
    col_tit, col_edit = st.columns([0.8, 0.2])
    with col_tit:
        st.subheader(f"Categoria: {categoria_nome}")
    with col_edit:
        with st.popover("✏️"):
            novo_nome = st.text_input("Renomear:", value=categoria_nome)
            if st.button("Confirmar"):
                if novo_nome and novo_nome != categoria_nome:
                    idx = st.session_state.categorias.index(categoria_nome)
                    st.session_state.categorias[idx] = novo_nome
                    salvar_configuracoes_nuvem()
                    st.rerun()

    # Placeholder para o contador atualizar na hora
    placeholder_cont = st.empty()
    placeholder_cont.info(f"🔢 Lançamentos realizados: **{st.session_state.cont_lanc}**")
    
    manter_aberto = st.checkbox(
        "Marque aqui para Lançar Várias despesas", 
        key=f"persist_check_{categoria_nome}"
    )

    # 2. FORMULÁRIO
    with st.form(key=f"form_final_{categoria_nome}", clear_on_submit=True):
        desc = st.text_input("Descrição da Despesa")
        
        c1, c2 = st.columns([2, 1])
        tipo_desp = c1.selectbox("Tipo", ["Variável", "Fixa"])
        parcelas = c2.number_input("Parcelas", min_value=1, value=1)
        
        c3, c4 = st.columns([2, 4])
        valor = c3.number_input("Valor Total", min_value=0.0, format="%.2f")
        
        opcoes_pag = [f['nome'] for f in st.session_state.formas_pagamento]
        forma_sel = c4.selectbox("Pagamento", options=opcoes_pag if opcoes_pag else ["Dinheiro"])
        
        # AQUI A DATA USA O data_hoje CALCULADO COM FUSO BRASIL
        data_l = st.date_input("Data", value=data_hoje, format="DD/MM/YYYY")

        btn_salvar = st.form_submit_button("✅ Salvar Lançamento", use_container_width=True)

    # 3. LÓGICA DE SALVAMENTO (Dentro do Modal Despesa)
    if btn_salvar:
        if not desc or valor <= 0:
            st.error("Preencha descrição e valor!")
        else:
            st.session_state.cont_lanc += 1
            
            detalhes = next((i for i in st.session_state.formas_pagamento if i["nome"] == forma_sel), None)
            lista_itens = []
            
            # --- NOVA LÓGICA DE STATUS ---
            # Se for Cartão OU a categoria for Empréstimo, o status é "Não Realizado"
            if "Cartão" in forma_sel or categoria_nome == "Empréstimo":
                status_auto = "Não Realizado"
            else:
                status_auto = "Realizado"
            
            for p in range(int(parcelas)):
                data_parc = data_l + pd.DateOffset(months=p)
                venc = calcular_vencimento_real(data_parc.date(), detalhes)
                
                # Parcela vazia se for 1, senão 1/2, 2/2...
                txt_parc = f"{p+1}/{int(parcelas)}" if int(parcelas) > 1 else ""
                
                lista_itens.append({
                    "Data Compra": data_l.strftime("%d/%m/%Y"),
                    "Vencimento": venc.strftime("%d/%m/%Y"),
                    "Categoria": categoria_nome,
                    "Descrição": desc,
                    "Parcela": txt_parc,
                    "Tipo": tipo_desp,
                    "Valor": valor / parcelas,
                    "Pagamento": forma_sel,
                    "Status": status_auto  # Aplica o status definido acima
                })
            
            salvar_no_google(lista_itens, aba="Dados")
            
            placeholder_cont.info(f"🔢 Lançamentos realizados: **{st.session_state.cont_lanc}**")
            st.toast(f"✅ {desc} salvos!")

            if not st.session_state[f"persist_check_{categoria_nome}"]:
                st.session_state.cont_lanc = 0
                st.rerun()

    if st.button("❌ Sair / Concluir", use_container_width=True):
        st.session_state.cont_lanc = 0
        st.rerun()
            
# --- 7. MODAL DE RECEITA (ENTRADAS DE DINHEIRO) ---

@st.dialog("💰 Nova Receita")
def modal_receita_categoria(fonte_nome):
    """
    PARA QUE SERVE: Cadastro de entradas financeiras com as mesmas melhorias do modal de despesas.
    """
    import datetime
    import pytz

    # 1. GARANTE QUE O CONTADOR EXISTE
    if 'cont_receita' not in st.session_state:
        st.session_state.cont_receita = 0

    # --- AJUSTE DE DATA (FUSO HORÁRIO BRASIL) ---
    fuso_br = pytz.timezone('America/Sao_Paulo')
    data_hoje = datetime.datetime.now(fuso_br).date()

    # --- CABEÇALHO COM EDIÇÃO ---
    col_tit, col_edit = st.columns([0.8, 0.2])
    with col_tit:
        st.subheader(f"Fonte: {fonte_nome}")
    with col_edit:
        with st.popover("✏️"):
            novo_nome = st.text_input("Renomear Fonte:", value=fonte_nome)
            if st.button("Confirmar Nome"):
                if novo_nome and novo_nome != fonte_nome:
                    # Ajuste aqui conforme sua lista de fontes de receita
                    if fonte_nome in st.session_state.fontes_receita:
                        idx = st.session_state.fontes_receita.index(fonte_nome)
                        st.session_state.fontes_receita[idx] = novo_nome
                        salvar_configuracoes_nuvem()
                        st.rerun()

    # Placeholder para o contador atualizar na hora
    placeholder_cont = st.empty()
    placeholder_cont.success(f"💵 Receitas lançadas agora: **{st.session_state.cont_receita}**")
    
    # Checkbox externa para não resetar com o formulário
    manter_aberto = st.checkbox(
        "Marque para Lançar Várias receitas", 
        key=f"persist_receita_{fonte_nome}"
    )

    # 2. FORMULÁRIO DE ENTRADA
    with st.form(key=f"form_receita_{fonte_nome}", clear_on_submit=True):
        desc = st.text_input("Descrição da Receita (Ex: Salário, Venda, etc)")
        
        c1, c2 = st.columns(2)
        valor = c1.number_input("Valor Recebido", min_value=0.0, format="%.2f")
        
        # Busca as contas de destino (Onde o dinheiro vai cair)
        opcoes_pag = [f['nome'] for f in st.session_state.formas_pagamento]
        conta_destino = c2.selectbox("Receber em:", options=opcoes_pag if opcoes_pag else ["Dinheiro"])
        
        data_r = st.date_input("Data do Recebimento", value=data_hoje, format="DD/MM/YYYY")

        btn_salvar = st.form_submit_button("✅ Salvar Receita", use_container_width=True)

    # 3. LÓGICA DE SALVAMENTO
    if btn_salvar:
        if not desc or valor <= 0:
            st.error("Preencha a descrição e o valor!")
        else:
            # Incrementa contador antes do salvamento
            st.session_state.cont_receita += 1
            
            # Prepara o dado para a planilha
            novo_item = [{
                "Data Compra": data_r.strftime("%d/%m/%Y"), # Mantemos o padrão da coluna
                "Vencimento": data_r.strftime("%d/%m/%Y"),
                "Categoria": fonte_nome,
                "Descrição": desc,
                "Parcela": "",
                "Tipo": "Receita", # Identificador para os cálculos futuros
                "Valor": valor,
                "Pagamento": conta_destino              
            }]
            
            # Salva no Google Sheets (Aba Dados)
            salvar_no_google(novo_item, aba="Dados")
            
            # Atualiza visualmente o contador e limpa campos
            placeholder_cont.success(f"💵 Receitas lançadas agora: **{st.session_state.cont_receita}**")
            st.toast(f"💰 Receita '{desc}' salva!")

            # Controle de fechamento
            if not st.session_state[f"persist_receita_{fonte_nome}"]:
                st.session_state.cont_receita = 0
                st.rerun()

    # 4. BOTÃO DE SAIR
    if st.button("❌ Concluir", use_container_width=True):
        st.session_state.cont_receita = 0
        st.rerun()

# --- 8. MODAL DE GERENCIAR CARTÕES E PAGAMENTOS (COM LIMITE DE GASTOS) ---

@st.dialog("💳 Gerenciar Formas de Pagamento") # Cria a janela flutuante para cartões
def modal_forma_pagamento():
    """Permite cadastrar, editar e excluir cartões ou contas (PIX, Dinheiro, etc)"""
    
    # --- PARTE 1: CADASTRO DE NOVO CARTÃO/CONTA ---
    with st.form(key="form_cadastro_pagamento", clear_on_submit=True):
        st.write("### Cadastrar Nova")
        
        # Campo para o nome (Ex: Nubank, Itaú, Dinheiro)
        nova_f = st.text_input("Nome da Forma (Ex: Nubank)")
        # Campo para o tipo (Ex: Crédito, Débito, PIX)
        tipo_f = st.text_input("Tipo (Ex: Cartão de Crédito)")
        
        st.info("💡 Para Cartão, preencha fechamento, vencimento e limite. Para Dinheiro/PIX, deixe 0.")
        
        # Grid para números
        col1, col2, col3 = st.columns(3)
        fech = col1.number_input("Fechamento", 0, 31, 0)
        venc = col2.number_input("Vencimento", 0, 31, 0)
        limite_cad = col3.number_input("Limite Gasto (R$)", min_value=0.0, step=100.0, value=0.0)
        
        # BOTÃO DE CADASTRO
        if st.form_submit_button("Confirmar Cadastro", use_container_width=True):
            if nova_f:
                # Se a gaveta de formas não existir na memória, cria ela agora
                if 'formas_pagamento' not in st.session_state: 
                    st.session_state.formas_pagamento = []
                
                # Adiciona o novo cartão à lista na memória com o campo de limite
                st.session_state.formas_pagamento.append({
                    "nome": nova_f, 
                    "tipo": tipo_f, 
                    "fechamento": fech, 
                    "vencimento": venc,
                    "limite_sugerido": limite_cad # Novo campo aqui
                })
                
                # --- SINCRONIZAÇÃO COM A NUVEM ---
                salvar_configuracoes_nuvem()
                
                st.success(f"✅ Forma '{nova_f}' cadastrada com sucesso!")
                st.rerun()

    # --- PARTE 2: LISTA DE CARTÕES EXISTENTES E EDIÇÃO ---
    if 'formas_pagamento' in st.session_state and st.session_state.formas_pagamento:
        st.markdown("---") # Linha divisória
        st.write("### Formas Cadastradas (Clique para Editar)")
        
        for i, item in enumerate(st.session_state.formas_pagamento):
            with st.expander(f"⚙️ Editar: {item['nome']}"):
                
                edit_nome = st.text_input("Nome", value=item['nome'], key=f"edit_n_{i}")
                edit_tipo = st.text_input("Tipo", value=item['tipo'], key=f"edit_t_{i}")
                
                c1, c2, c3 = st.columns(3)
                edit_fech = c1.number_input("Fechamento", 0, 31, value=item['fechamento'], key=f"edit_f_{i}")
                edit_venc = c2.number_input("Vencimento", 0, 31, value=item['vencimento'], key=f"edit_v_{i}")
                
                # Melhoria: Recupera o limite sugerido (se não existir, inicia 0.0)
                limite_atual = float(item.get('limite_sugerido', 0.0))
                edit_limite = c3.number_input("Limite (R$)", min_value=0.0, step=100.0, value=limite_atual, key=f"edit_l_{i}")
                
                col_btn1, col_btn2 = st.columns(2)
                
                # BOTÃO SALVAR ALTERAÇÃO
                if col_btn1.button("Salvar Alterações", key=f"save_{i}", use_container_width=True):
                    st.session_state.formas_pagamento[i] = {
                        "nome": edit_nome, 
                        "tipo": edit_tipo, 
                        "fechamento": edit_fech, 
                        "vencimento": edit_venc,
                        "limite_sugerido": edit_limite # Novo campo aqui
                    }
                    salvar_configuracoes_nuvem()
                    st.success("Alterado com sucesso!")
                    st.rerun()
                
                # BOTÃO REMOVER CARTÃO
                if col_btn2.button("Remover", key=f"del_{i}", use_container_width=True):
                    st.session_state.formas_pagamento.pop(i)
                    salvar_configuracoes_nuvem()
                    st.rerun()
                    
# --- 9. NAVEGAÇÃO E ESTRUTURA DO PAINEL INICIAL (VERSÃO FORÇADA INLINE) ---

# Título que aparece no topo do menu lateral
st.sidebar.title("MENU PRINCIPAL") 

# BOTÕES DE NAVEGAÇÃO NA BARRA LATERAL (Alinhamento forçado via Style)
if st.sidebar.button("📊 Painel Inicial", use_container_width=True):
    st.session_state.pagina = "Painel Inicial"
if st.sidebar.button("⚙️ Cadastros Iniciais", use_container_width=True):
    st.session_state.pagina = "Cadastros Iniciais"
if st.sidebar.button("📋 Visualizar Lançamentos", use_container_width=True):
    st.session_state.pagina = "Visualizar Lançamentos"
if st.sidebar.button("💳 Cartões", use_container_width=True):
    st.session_state.pagina = "Cartões"

# CSS para tentar alinhar o botão (se o inline falhar no sidebar)
st.markdown("""<style> 
    [data-testid="stSidebar"] button {text-align: left !important; justify-content: flex-start !important; display: flex !important;}
</style>""", unsafe_allow_html=True)

selecionado = st.session_state.get('pagina', "Painel Inicial")

if selecionado == "Painel Inicial":
    st.markdown("## 🏠 Painel de Controle")

# --- LINHA 1: FILTROS E DESEMPENHO ---
    col_per, col_des = st.columns([0.7, 2.3])

    with col_per:
        with st.container(height=160, border=True):
            # 1. Título do quadro
            st.markdown("<div style='margin-top: 20px; margin-bottom: 5px; font-size: 0.9rem;'>🔍 <b>Período</b></div>", unsafe_allow_html=True)
            
            # --- BLOCO MÊS ---
            st.markdown("<div style='margin-top: 8px; margin-bottom: 0px; font-size: 0.75rem;'><b>Selecione o Mês:</b></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:-8px;'></div>", unsafe_allow_html=True) 
            mes_sel = st.selectbox("Mês", ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], index=0, key="mes_filtro", label_visibility="collapsed")
            
            # --- BLOCO ANO (APROXIMADO DA CAIXA ACIMA) ---
            st.markdown("<div style='margin-top: -10px; font-size: 0.75rem;'><b>Selecione o Ano:</b></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: -25px;'></div>", unsafe_allow_html=True)
            ano_sel = st.selectbox("Ano", ["2024", "2025", "2026"], index=2, key="ano_filtro", label_visibility="collapsed")

    with col_des:
        with st.container(height=160, border=True):
            # Mantendo o quadro de desempenho conforme o ajuste anterior que você aprovou
            consumo = 49  
            cor_b = "#008080" if consumo < 75 else "#FF4B4B"
            
            st.markdown(f"""
                <div style="margin-top: -5px;">
                    <span style="font-size: 0.85rem; font-weight: bold; color: #555; text-transform: uppercase;">Desempenho de Gastos em {mes_sel}</span>
                    <h3 style="margin: 0px; padding: 0px;">{consumo}% <span style="font-size: 0.9rem; font-weight: normal; color: #666;">utilizado</span></h3>
                </div>
            """, unsafe_allow_html=True)
            
            barra_html = f"""
            <div style="width: 100%; background-color: #E0E0E0; border-radius: 10px; height: 22px; border: 1px solid #CCC; overflow: hidden; margin-top: 5px;">
                <div style="width: {consumo}%; background-color: {cor_b}; height: 100%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 2px; font-size: 10px; font-weight: bold; color: #444; padding: 0 5px;">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
            </div>
            """
            st.markdown(barra_html, unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 0.8rem; margin-top: 5px; color: #2E7D32;'>🟢 Gastos saudáveis para este período.</div>", unsafe_allow_html=True)
            
    # --- LINHA 2: RESUMO FINANCEIRO (KPIs) - CORREÇÃO DE OVERFLOW ---
    with st.container(border=True):
        st.markdown("**💰 Consolidado Mensal**")
        c1, c2, c3 = st.columns(3)
        
        # Cards com largura travada em 100% e box-sizing
        with c1:
            st.markdown(f'<div style="background-color:#008080; color:white; padding:15px; border-radius:8px; width:100%; box-sizing:border-box; text-align:center;">RECEITA<br><b style="font-size:1.2rem;">R$ 5.000,00</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="background-color:#FF4B4B; color:white; padding:15px; border-radius:8px; width:100%; box-sizing:border-box; text-align:center;">DESPESA<br><b style="font-size:1.2rem;">R$ 2.450,00</b></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div style="background-color:#D4AF37; color:white; padding:15px; border-radius:8px; width:100%; box-sizing:border-box; text-align:center;">SALDO<br><b style="font-size:1.2rem;">R$ 2.550,00</b></div>', unsafe_allow_html=True)

    # --- LINHA 3: STATUS DETALHADO ---
    st.markdown("### 📊 Status por Categoria")
    with st.container(border=True):
        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown('<div style="background-color:#FF914D; color:white; padding:15px; border-radius:8px; width:100%; box-sizing:border-box; text-align:center;"><b>A PAGAR</b><br>R$ 1.200,00</div>', unsafe_allow_html=True)
        with d2:
            st.markdown('<div style="background-color:#666666; color:white; padding:15px; border-radius:8px; width:100%; box-sizing:border-box; text-align:center;"><b>PREVISTA</b><br>R$ 800,00</div>', unsafe_allow_html=True)
        with d3:
            st.markdown('<div style="background-color:#007BFF; color:white; padding:15px; border-radius:8px; width:100%; box-sizing:border-box; text-align:center;"><b>NUBANK</b><br>R$ 450,00</div>', unsafe_allow_html=True)
            

# --- 10. TELA DE CONFIGURAÇÕES E CADASTROS (SCROLL FORÇADO) ---

if selecionado == "Cadastros Iniciais":
    st.markdown("## ⚙️ Configurações e Cadastros")
    st.markdown("---")
    
    # CSS para forçar a barra de rolagem a ser tratada corretamente pelo navegador
    st.markdown("""
        <style>
            [data-testid="stVerticalBlock"] > div:has(div.stVerticalBlockBorder) > div {
                overflow-y: auto !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    col_desp, col_rec, col_pgto = st.columns([1, 1, 1])

    # --- COLUNA 1: GESTÃO DE DESPESAS ---
    with col_desp:
        with st.container(border=True):
            st.markdown("### 🔻 Categoria Despesa")
            
            with st.popover("➕ Inserir Categoria", use_container_width=True):
                n_cat = st.text_input("Nome (Ex: Casa)", key="new_cat_desp")
                if st.button("Salvar", key="btn_save_desp", use_container_width=True):
                    if n_cat and n_cat not in st.session_state.categorias:
                        st.session_state.categorias.append(n_cat)
                        salvar_configuracoes_nuvem() 
                        st.success(f"Categoria '{n_cat}' cadastrada!")
                        st.rerun() 
            
            st.markdown("---")
            
            # Usando height para forçar o scroll nativo do Streamlit
            with st.container(height=250, border=False):
                for i, cat in enumerate(st.session_state.categorias):
                    c_item, c_del = st.columns([0.8, 0.2])
                    with c_item:
                        if st.button(f"🔻 {cat.upper()}", use_container_width=True, key=f"btn_d_{cat}_{i}"):
                            modal_lancamento_categoria(cat)
                    with c_del:
                        if st.button("🗑️", key=f"del_d_{cat}_{i}"):
                            st.session_state.categorias.remove(cat)
                            salvar_configuracoes_nuvem()
                            st.rerun()

    # --- COLUNA 2: GESTÃO DE RECEITAS (GANHOS) ---
    with col_rec:
        with st.container(border=True):
            st.markdown("### 💹 Fonte de Receita")
            
            with st.popover("💰 Inserir Fonte", use_container_width=True):
                n_rec = st.text_input("Nome (Ex: Salário)", key="new_cat_rec")
                if st.button("Salvar", key="btn_save_rec", use_container_width=True):
                    if 'categorias_receita' not in st.session_state:
                        st.session_state.categorias_receita = []
                    if n_rec and n_rec not in st.session_state.categorias_rece_ita:
                        st.session_state.categorias_receita.append(n_rec)
                        salvar_configuracoes_nuvem()
                        st.success(f"Fonte '{n_rec}' cadastrada!")
                        st.rerun() 
            
            st.markdown("---")
            
            with st.container(height=250, border=False):
                if 'categorias_receita' in st.session_state:
                    for i, cat_r in enumerate(st.session_state.categorias_receita):
                        c_item_r, c_del_r = st.columns([0.8, 0.2])
                        with c_item_r:
                            if st.button(f"💹 {cat_r.upper()}", use_container_width=True, key=f"btn_r_{cat_r}_{i}"):
                                modal_receita_categoria(cat_r)
                        with c_del_r:
                            if st.button("🗑️", key=f"del_r_{cat_r}_{i}"):
                                st.session_state.categorias_receita.remove(cat_r)
                                salvar_configuracoes_nuvem()
                                st.rerun()

    # --- COLUNA 3: GESTÃO DE PAGAMENTOS E CARTÕES ---
    with col_pgto:
        with st.container(border=True):
            st.markdown("### 💳 Forma Pagamento")
            
            if st.button("⚙️ Criar Pagamento", use_container_width=True):
                modal_forma_pagamento()
            
            st.markdown("---")
            
            with st.container(height=250, border=False):
                if 'formas_pagamento' in st.session_state:
                    for i, f in enumerate(st.session_state.formas_pagamento):
                        c_item_f, c_del_f = st.columns([0.8, 0.2])
                        with c_item_f:
                            st.caption(f"✅ {f['nome']}")
                        with c_del_f:
                            if st.button("🗑️", key=f"del_f_{f['nome']}_{i}"):
                                st.session_state.formas_pagamento.pop(i)
                                salvar_configuracoes_nuvem()
                                st.rerun()

# --- 11. TELA DE VISUALIZAÇÃO (LISTVIEW EM UM QUADRO ÚNICO) ---

if selecionado == "Visualizar Lançamentos":
    st.markdown("## 📊 Histórico de Lançamentos")

    LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1PyE9M6KLjJDtIDuCO5DCCTTcz-jsVr3Gj3Cv9yrxPE0/export?format=xlsx"

    try:
        # Lendo a planilha
        df_geral = pd.read_excel(LINK_PLANILHA, sheet_name='Dados')

        if not df_geral.empty:
            # --- 1. FORMATAÇÃO DAS DATAS ---
            df_geral['Data Compra'] = pd.to_datetime(df_geral['Data Compra'], errors='coerce')
            df_geral['Vencimento'] = pd.to_datetime(df_geral['Vencimento'], errors='coerce')

            # --- QUADRO ÚNICO PARA FILTROS E TABELA ---
            with st.container(border=True):
                st.markdown("### 🔍 Filtros e Lançamentos")
                
                # Mantendo a sua disposição original de colunas para os filtros
                c1, c2, c3, vazio_dir = st.columns([0.6, 0.8, 1.2, 5])
                
                with c1:
                    df_geral['Mes_Filtro'] = df_geral['Vencimento'].dt.strftime('%m/%Y')
                    meses = sorted(df_geral['Mes_Filtro'].dropna().unique())
                    mes_sel = st.selectbox("Mês:", ["Todos"] + meses)
                
                with c2:
                    categorias = sorted(df_geral['Categoria'].dropna().unique())
                    cat_sel = st.selectbox("Categoria:", ["Todas"] + categorias)
                    
                with c3:
                    pagamentos = sorted(df_geral['Pagamento'].dropna().unique())
                    pag_sel = st.selectbox("Pagamento:", ["Todos"] + pagamentos)

                # Lógica de filtragem (sem alterações)
                df_display = df_geral.copy()
                if mes_sel != "Todos":
                    df_display = df_display[df_display['Mes_Filtro'] == mes_sel]
                if cat_sel != "Todas":
                    df_display = df_display[df_display['Categoria'] == cat_sel]
                if pag_sel != "Todos":
                    df_display = df_display[df_display['Pagamento'] == pag_sel]

                # Formatação para exibição
                df_display['Data Compra'] = df_display['Data Compra'].dt.date
                df_display['Vencimento'] = df_display['Vencimento'].dt.date

                # --- 2. TRATAMENTO DA PARCELA (LÓGICA ORIGINAL) ---
                if 'Parcela' in df_display.columns:
                    def limpar_parcela(row):
                        if str(row.get('Tipo', '')).lower() == 'receita':
                            return ""
                        val = row['Parcela']
                        if pd.isna(val) or str(val).lower() in ['nat', 'nan', 'none', '']:
                            return ""
                        if isinstance(val, (pd.Timestamp, datetime.date)):
                            return f"{val.day}/{val.month}"
                        if str(val).strip() == "None":
                            return ""
                        return str(val)
                    
                    df_display['Parcela'] = df_display.apply(limpar_parcela, axis=1)

                # Configuração de colunas da tabela
                config_datas = {
                    "Data Compra": st.column_config.DateColumn("Data", format="DD/MM/YYYY", width=90),
                    "Vencimento": st.column_config.DateColumn("Vencimento", format="DD/MM/YYYY", width=90),
                    "Descrição": st.column_config.TextColumn("Descrição", width=300),
                    "Categoria": st.column_config.TextColumn("Categoria", width=120),
                    "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f", width=100),
                    "Parcela": st.column_config.TextColumn("Parcela", width=65),
                    "Pagamento": st.column_config.TextColumn("Pagamento", width=150),
                    "Tipo": st.column_config.TextColumn("Tipo", width=70),
                    "Status": st.column_config.TextColumn("Status", width=100)
                }

                st.markdown("---") # Linha divisória dentro do quadro

                # Abas dentro do quadro único
                tab1, tab2, tab3 = st.tabs(["📑 Geral", "🔴 Despesas", "🟢 Receitas"])

                df_receitas = df_display[df_display['Tipo'] == 'Receita'].copy()
                df_despesas = df_display[df_display['Tipo'].isin(['Fixa', 'Variável'])].copy()
                cols_exibir = [c for c in df_display.columns if c != 'Mes_Filtro']

                with tab1:
                    st.dataframe(df_display[cols_exibir], use_container_width=True, hide_index=True, column_config=config_datas, height=600)

                with tab2:
                    if not df_despesas.empty:
                        st.dataframe(df_despesas[cols_exibir], use_container_width=True, hide_index=True, column_config=config_datas, height=600)
                        st.metric("Total Gasto", f"R$ {df_despesas['Valor'].sum():,.2f}")

                with tab3:
                    if not df_receitas.empty:
                        st.dataframe(df_receitas[cols_exibir], use_container_width=True, hide_index=True, column_config=config_datas, height=600)
                        st.metric("Total Recebido", f"R$ {df_receitas['Valor'].sum():,.2f}")

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")


# --- 12. TELA DE CARTÕES (CÓDIGO COMPLETO E CORRIGIDO) ---

if selecionado == "Cartões":
    st.markdown("## 💳 Painel de Cartões de Crédito")
    
    LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1PyE9M6KLjJDtIDuCO5DCCTTcz-jsVr3Gj3Cv9yrxPE0/export?format=xlsx"

    try:
        import json
        from datetime import datetime
        
        df_geral = pd.read_excel(LINK_PLANILHA, sheet_name='Dados')
        df_config = pd.read_excel(LINK_PLANILHA, sheet_name='Config') 

        # --- TRATAMENTO DA COLUNA PARCELA ---
        def formatar_parcela(val):
            if pd.isna(val) or str(val).lower() in ['nan', 'none', 'nat']: return ""
            if isinstance(val, pd.Timestamp) or hasattr(val, 'month'): return f"{val.day}/{val.month}"
            val_str = str(val)
            if val_str.endswith('.0'): return val_str[:-2]
            return val_str

        df_geral['Parcela'] = df_geral['Parcela'].apply(formatar_parcela)

        if not df_config.empty and 'Detalhes_Pagamento' in df_config.columns:
            def extrair_json(x):
                try: return json.loads(x.replace("'", '"'))
                except: return {}
            
            df_detalhes = pd.DataFrame(df_config['Detalhes_Pagamento'].apply(extrair_json).tolist())
            df_cartoes = df_detalhes[df_detalhes['tipo'] == 'Cartão de Crédito']

            # --- LINHA SUPERIOR: FILTROS E META (ALINHAMENTO EXATO) ---
            col_esq, col_dir = st.columns(2)

            with col_esq:
                with st.container(border=True):
                    st.markdown("🔍 **Filtros de Busca**")
                    cartao_sel = st.selectbox("Escolha o Cartão:", sorted(df_cartoes['nome'].unique()))
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        df_geral['Vencimento'] = pd.to_datetime(df_geral['Vencimento'], errors='coerce')
                        df_geral['Mes_Venc'] = df_geral['Vencimento'].dt.strftime('%m/%Y')
                        meses_disp = sorted(df_geral['Mes_Venc'].dropna().unique(), reverse=True)
                        mes_atual = datetime.now().strftime('%m/%Y')
                        indice_padrao = meses_disp.index(mes_atual) if mes_atual in meses_disp else 0
                        mes_sel = st.selectbox("Mês de Fechamento:", meses_disp, index=indice_padrao)
                    with c2:
                        tipo_compra = st.selectbox("Tipo de Lançamento:", ["Tudo", "À Vista", "Parcelado"])

            # Dados da Meta e Cálculos
            info = df_cartoes[df_cartoes['nome'] == cartao_sel].iloc[0]
            df_fatura = df_geral[(df_geral['Pagamento'] == cartao_sel) & (df_geral['Mes_Venc'] == mes_sel)].copy()
            total_fatura = df_fatura['Valor'].sum()
            limite_fixo = float(info.get('limite_sugerido', 0.0))

            with col_dir:
                with st.container(border=True):
                    st.markdown("🎯 **Meta de Limite**")
                    
                    if limite_fixo > 0:
                        percentual = min((total_fatura / limite_fixo) * 100, 100.0)
                        cor_barra = "#2e7d32" if percentual < 85 else "#d32f2f"
                        disponivel = limite_fixo - total_fatura
                        
                        # Espaçamento para alinhar altura com o quadro da esquerda
                        st.markdown('<div style="padding-top: 10px;"></div>', unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div style="margin-bottom: 5px;">
                                <span style="font-size: 16px; font-weight: bold;">Limite:</span> 
                                <span style="font-size: 24px; font-weight: bold; color: #1E88E5;">R$ {limite_fixo:,.2f}</span>
                            </div>
                            <div style="width: 100%; background-color: #e0e0e0; border-radius: 8px; height: 28px;">
                                <div style="width: {percentual}%; background-color: {cor_barra}; height: 28px; border-radius: 8px; text-align: center; color: white; font-size: 14px; font-weight: bold; line-height: 28px;">
                                    {percentual:.1f}%
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; padding: 2px 5px; color: #555; margin-bottom: 10px;">
                                <span>0%</span>
                                <span>50%</span>
                                <span>100%</span>
                            </div>
                        """, unsafe_allow_html=True)

                        # MENSAGEM DE STATUS CORRIGIDA
                        if disponivel < 0:
                            st.markdown(f"<div style='background-color: #ffebee; padding: 5px; border-radius: 5px; text-align: center; color: #d32f2f; font-weight: bold;'>⚠️ Limite Excedido em R$ {abs(disponivel):,.2f}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='background-color: #e8f5e9; padding: 5px; border-radius: 5px; text-align: center; color: #2e7d32; font-weight: bold;'>✅ Valor Disponível: R$ {disponivel:,.2f}</div>", unsafe_allow_html=True)
                        
                        # Espaçador inferior para igualar a altura final
                        st.markdown('<div style="padding-bottom: 15px;"></div>', unsafe_allow_html=True)
                    else:
                        st.info("💡 Limite não configurado para este cartão.")
                        st.write("")
                        st.write("")
                        st.write("")

            # --- PROCESSAMENTO DOS TOTAIS E EXIBIÇÃO ---
            df_fatura = df_fatura.sort_values(by='Vencimento', ascending=True)
            mask_parcelado = df_fatura['Parcela'].str.contains('/', na=False)
            total_avista = df_fatura[~mask_parcelado]['Valor'].sum()
            total_parcelado = df_fatura[mask_parcelado]['Valor'].sum()

            if tipo_compra == "À Vista": df_exibir = df_fatura[~mask_parcelado]
            elif tipo_compra == "Parcelado": df_exibir = df_fatura[mask_parcelado]
            else: df_exibir = df_fatura

            f_dia = int(float(info.get('fechamento', 0))) if str(info.get('fechamento')).replace('.','').isdigit() else '?'
            v_dia = int(float(info.get('vencimento', 0))) if str(info.get('vencimento')).replace('.','').isdigit() else '?'

            # --- QUADRO 2: RESUMO DA FATURA ---
            with st.container(border=True):
                col_t, col_d = st.columns([1, 1])
                with col_t: st.markdown("<div style='text-align: left; font-size: 20px; font-weight: bold;'>📊 Resumo da Fatura</div>", unsafe_allow_html=True)
                with col_d:
                    st.markdown(f"<div style='text-align: right; line-height: 1.2;'><span style='font-size: 18px; font-weight: bold;'>Fechamento:</span> <span style='font-size: 16px;'>{f_dia}</span><br><span style='font-size: 18px; font-weight: bold;'>Vencimento:</span> <span style='font-size: 16px;'>{v_dia}</span></div>", unsafe_allow_html=True)
                st.markdown("---") 
                c_v1, c_v2, c_v3 = st.columns(3)
                with c_v1: st.metric("Total à Vista", f"R$ {total_avista:,.2f}")
                with c_v2: st.metric("Total Parcelado", f"R$ {total_parcelado:,.2f}")
                with c_v3: st.metric("Total da Fatura", f"R$ {total_fatura:,.2f}")

            # --- QUADRO 3: ITENS DA FATURA ---
            with st.container(border=True):
                st.markdown(f"📝 **Itens da Fatura ({tipo_compra})**")
                if not df_exibir.empty:
                    df_exibir['Venc_View'] = df_exibir['Vencimento'].dt.date
                    df_exibir['Valor_Formatado'] = df_exibir['Valor'].apply(lambda x: f"R$ {x:,.2f}")
                    st.dataframe(df_exibir[["Venc_View", "Descrição", "Valor_Formatado", "Parcela", "Status"]], use_container_width=True, hide_index=True, height=400)
                else:
                    st.info("Nenhum lançamento encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar a tela: {e}")













































































































































































































































































































































