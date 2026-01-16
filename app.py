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
    PARA QUE SERVE: Cadastro de despesas com contador de lançamentos na sessão atual
    e opção de fluxo contínuo (sem fechar a janela).
    """
    
    # 1. CONTADOR DE LANÇAMENTOS (Sessão Atual)
    if 'cont_lanc' not in st.session_state:
        st.session_state.cont_lanc = 0

    # 2. CABEÇALHO E EDIÇÃO
    col_tit, col_edit = st.columns([0.8, 0.2])
    with col_tit:
        st.subheader(f"Categoria: {categoria_nome}")
        # EXIBE QUANTOS FORAM LANÇADOS DESDE QUE O MODAL ABRIU
        st.markdown(f"**Lançamentos realizados nesta categoria:** :blue[{st.session_state.cont_lanc}]")
    
    with col_edit:
        with st.popover("✏️"):
            novo_nome = st.text_input("Novo nome", value=categoria_nome)
            if st.button("Salvar Nome"):
                idx = st.session_state.categorias.index(categoria_nome)
                st.session_state.categorias[idx] = novo_nome
                salvar_configuracoes_nuvem()
                st.rerun()

    # 3. FORMULÁRIO DE ENTRADA
    # 'clear_on_submit=True' limpa os campos automaticamente após o sucesso
    with st.form(key=f"form_d_{categoria_nome}", clear_on_submit=True):
        desc = st.text_input("Descrição da Despesa")
        
        c_tipo, c_parc = st.columns([2, 1])
        tipo_desp = c_tipo.selectbox("Tipo", ["Variável", "Fixa"])
        parcelas = c_parc.number_input("Parcelas", min_value=1, value=1)
        
        c_val, c_pag = st.columns([2, 4])
        valor = c_val.number_input("Valor Total", min_value=0.0, format="%.2f")
        
        opcoes_pag = [f['nome'] for f in st.session_state.formas_pagamento]
        forma_sel = c_pag.selectbox("Pagamento", options=opcoes_pag if opcoes_pag else ["Dinheiro"])
        
        data_l = st.date_input("Data", format="DD/MM/YYYY")

        # CHECKBOX PARA LANÇAMENTO CONTÍNUO
        manter_aberto = st.checkbox("Marque aqui para Lançar Várias despesas", value=False)
        
        col_btn1, col_btn2 = st.columns(2)
        btn_salvar = col_btn1.form_submit_button("✅ Salvar Lançamento", use_container_width=True)
        btn_cancelar = col_btn2.form_submit_button("❌ Sair / Concluir", use_container_width=True)

        if btn_salvar:
            if not desc or valor <= 0:
                st.error("Preencha a descrição e o valor!")
            else:
                detalhes = next((i for i in st.session_state.formas_pagamento if i["nome"] == forma_sel), None)
                lista_itens = []
                
                for p in range(int(parcelas)):
                    data_parc = data_l + pd.DateOffset(months=p)
                    venc = calcular_vencimento_real(data_parc.date(), detalhes)
                    txt_parc = f"{p+1}/{int(parcelas)}" if parcelas > 1 else ""
                    
                    lista_itens.append({
                        "Data Compra": data_l.strftime("%d/%m/%Y"),
                        "Vencimento": venc.strftime("%d/%m/%Y"),
                        "Categoria": categoria_nome,
                        "Descrição": desc,
                        "Parcela": txt_parc,
                        "Tipo": tipo_desp,
                        "Valor": valor / parcelas,
                        "Pagamento": forma_sel
                    })
                
                # Envia os dados para a planilha
                salvar_no_google(lista_itens, aba="Dados")
                
                # Incrementa o contador visual
                st.session_state.cont_lanc += 1
                
                if manter_aberto:
                    st.toast(f"✅ {desc} salvo com sucesso!") # Notificação discreta no canto
                    st.rerun() # Reinicia o modal, mas como 'manter_aberto' é lido, ele volta para cá
                else:
                    st.session_state.cont_lanc = 0 # Reseta o contador para a próxima vez
                    st.rerun() # Fecha o modal

        if btn_cancelar:
            st.session_state.cont_lanc = 0 # Reseta ao sair
            st.rerun()
            
# --- 7. MODAL DE RECEITA (ENTRADAS DE DINHEIRO) ---

@st.dialog("💰 Nova Receita") # Define que esta função abre uma janela pop-up de Receita
def modal_receita_categoria(categoria_nome):
    """Cria o formulário para adicionar ganhos dentro de cada fonte/categoria de receita"""
    
    # --- CABEÇALHO COM EDIÇÃO ---
    # Coluna 1 (80% da largura) para o título | Coluna 2 (20%) para o botão de editar
    col_tit, col_edit = st.columns([0.8, 0.2])
    
    with col_tit:
        st.subheader(f"Fonte: {categoria_nome}") # Exibe o nome da fonte de renda (ex: Salário)
        
    with col_edit:
        # Abre uma caixinha de edição se o nome da fonte estiver errado
        with st.popover("✏️"):
            novo_nome = st.text_input("Novo nome", value=categoria_nome)
            if st.button("Salvar Alteração"):
                if novo_nome and novo_nome != categoria_nome:
                    # LOCALIZA: Busca a posição exata na lista de RECEITAS
                    idx = st.session_state.categorias_receita.index(categoria_nome)
                    # SUBSTITUI: Coloca o novo nome naquela posição
                    st.session_state.categorias_receita[idx] = novo_nome
                    
                    # SINCRONIZA: Salva a lista de nomes atualizada na aba 'Config' da planilha
                    salvar_configuracoes_nuvem()
                    st.rerun()

    # --- FORMULÁRIO DE ENTRADA ---
    # 'clear_on_submit=True' limpa os campos após clicar em salvar
    with st.form(key=f"form_receita_{categoria_nome}", clear_on_submit=True):
        
        # Campo para escrever o que é (ex: 'Bonus Janeiro')
        desc = st.text_input("Descrição da Receita")
        
        # Divide em duas colunas para o Valor e a Conta de destino
        c1, c2 = st.columns([2, 4])
        
        with c1:
            # PARA ALTERAR: Se quiser um valor padrão sugerido, mude 'value=0.0' para 'value=1000.0'
            valor = st.number_input("Valor", min_value=0.0, format="%.2f")
            
        with c2:
            # Busca as formas de pagamento cadastradas para saber onde o dinheiro caiu
            opcoes = [f['nome'] for f in st.session_state.formas_pagamento]
            forma = st.selectbox("Recebido via", options=opcoes if opcoes else ["Conta Corrente"])
        
        # Seleção da data em que o dinheiro entrou/entrará
        data_r = st.date_input("Data", format="DD/MM/YYYY")
        
        # BOTÃO DE CONFIRMAÇÃO
        if st.form_submit_button("Confirmar Receita", use_container_width=True):
            # Prepara os dados no formato que a planilha aceita
            # Para Receitas, a 'Data Compra' e o 'Vencimento' são o mesmo dia
            nova_rec = [{
                "Data Compra": data_r.strftime("%d/%m/%Y"),
                "Vencimento": data_r.strftime("%d/%m/%Y"),
                "Categoria": categoria_nome,
                "Descrição": desc,
                "Tipo": "RECEITA", # Identificador vital para os gráficos separarem ganhos de gastos
                "Valor": valor,
                "Pagamento": forma
            }]
            
            # ENVIO PARA NUVEM: Salva na mesma aba 'Dados' onde ficam as despesas
            # A diferença é que aqui o 'Tipo' vai como 'RECEITA'
            salvar_no_google(nova_rec, aba="Dados")
            
            st.success(f"✅ Receita de '{categoria_nome}' sincronizada com a nuvem!")
            st.rerun() # Fecha o modal e atualiza os saldos na tela principal

# --- 8. MODAL DE GERENCIAR CARTÕES E PAGAMENTOS ---

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
        
        st.info("💡 Para Cartão, coloque os dias de fechamento e vencimento. Para Dinheiro/PIX, deixe 0.")
        
        # Cria duas colunas lado a lado para os números
        col1, col2 = st.columns(2)
        # PARA ALTERAR: O intervalo é de 0 a 31 (dias do mês)
        fech = col1.number_input("Dia Fechamento", 0, 31, 0) # Dia que a fatura "vira"
        venc = col2.number_input("Dia Vencimento", 0, 31, 0) # Dia que você paga a fatura
        
        # BOTÃO DE CADASTRO
        if st.form_submit_button("Confirmar Cadastro", use_container_width=True):
            if nova_f:
                # Se a gaveta de formas não existir na memória, cria ela agora
                if 'formas_pagamento' not in st.session_state: 
                    st.session_state.formas_pagamento = []
                
                # Adiciona o novo cartão à lista na memória
                st.session_state.formas_pagamento.append({
                    "nome": nova_f, "tipo": tipo_f, "fechamento": fech, "vencimento": venc
                })
                
                # --- SINCRONIZAÇÃO COM A NUVEM ---
                # Salva a lista inteira na aba "Config" do Google Sheets
                salvar_configuracoes_nuvem()
                
                st.success(f"✅ Forma '{nova_f}' cadastrada com sucesso!")
                st.rerun() # Reinicia para mostrar a nova forma na lista abaixo

    # --- PARTE 2: LISTA DE CARTÕES EXISTENTES E EDIÇÃO ---
    # Só mostra esta parte se já existir algum cartão cadastrado
    if 'formas_pagamento' in st.session_state and st.session_state.formas_pagamento:
        st.markdown("---") # Linha divisória
        st.write("### Formas Cadastradas (Clique para Editar)")
        
        # Percorre a lista de cartões e cria um 'Expander' (caixa que abre) para cada um
        for i, item in enumerate(st.session_state.formas_pagamento):
            with st.expander(f"⚙️ Editar: {item['nome']}"):
                
                # Campos de edição já preenchidos com os dados atuais
                edit_nome = st.text_input("Nome", value=item['nome'], key=f"edit_n_{i}")
                edit_tipo = st.text_input("Tipo", value=item['tipo'], key=f"edit_t_{i}")
                
                c1, c2 = st.columns(2)
                edit_fech = c1.number_input("Fechamento", 0, 31, value=item['fechamento'], key=f"edit_f_{i}")
                edit_venc = c2.number_input("Vencimento", 0, 31, value=item['vencimento'], key=f"edit_v_{i}")
                
                # Botões de Salvar e Remover lado a lado
                col_btn1, col_btn2 = st.columns(2)
                
                # BOTÃO SALVAR ALTERAÇÃO
                if col_btn1.button("Salvar Alterações", key=f"save_{i}", use_container_width=True):
                    # Atualiza os dados na memória (Session State)
                    st.session_state.formas_pagamento[i] = {
                        "nome": edit_nome, "tipo": edit_tipo, "fechamento": edit_fech, "vencimento": edit_venc
                    }
                    # Salva a mudança na planilha do Google
                    salvar_configuracoes_nuvem()
                    st.success("Alterado com sucesso!")
                    st.rerun()
                
                # BOTÃO REMOVER CARTÃO
                if col_btn2.button("Remover", key=f"del_{i}", use_container_width=True):
                    # Tira o item da lista
                    st.session_state.formas_pagamento.pop(i)
                    # Atualiza a planilha (removendo o item de lá também)
                    salvar_configuracoes_nuvem()
                    st.rerun()
                    

# --- 9. NAVEGAÇÃO E ESTRUTURA DO PAINEL INICIAL ---

# Título que aparece no topo do menu lateral
st.sidebar.title("MENU PRINCIPAL") 

# BOTÕES DE NAVEGAÇÃO NA BARRA LATERAL
# use_container_width=True faz o botão ocupar toda a largura da barra lateral
if st.sidebar.button("📊 Painel Inicial", use_container_width=True):
    st.session_state.pagina = "Painel Inicial"

if st.sidebar.button("⚙️ Cadastros Iniciais", use_container_width=True):
    st.session_state.pagina = "Cadastros Iniciais"

if st.sidebar.button("📈 Relatórios", use_container_width=True):
    st.session_state.pagina = "Relatórios"

# Garante que a variável 'selecionado' sempre tenha um valor para não dar erro nos IFs
selecionado = st.session_state.get('pagina', "Painel Inicial")

# --- LÓGICA DA TELA: PAINEL INICIAL ---
if selecionado == "Painel Inicial":
    st.markdown("## 🏠 Painel Inicial") # Título da página
    # Aplica a linha preta grossa definida no CSS
    st.markdown('<div class="barra-preta-grossa"></div>', unsafe_allow_html=True) 

    # ORGANIZAÇÃO DO CABEÇALHO (FILTROS E CARDS COLORIDOS)
    # Os números [1.2, 1.2...] definem a largura de cada coluna. 
    # PARA ALTERAR: Se os cards ficarem apertados, aumente esses números.
    col_filtro, col_rec, col_desp, col_sal, col_vazio, col_ava = st.columns([1.5, 1.2, 1.2, 1.2, 1.5, 2.5])

    with col_filtro: 
        # Caixas de seleção para filtrar os dados da planilha
        # index=datetime.now().month - 1 faria ele abrir sempre no mês atual
        mes_sel = st.selectbox("Mês", ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], index=0)
        ano_sel = st.selectbox("Ano", ["2024", "2025", "2026"], index=2) # 2026 como padrão

    with col_rec: 
        # Card de Receita (Verde Petróleo)
        st.markdown('<div class="card receita">RECEITA<br>R$ 5.000,00</div>', unsafe_allow_html=True)

    with col_desp: 
        # Card de Despesa (Vermelho)
        st.markdown('<div class="card despesa">DESPESA<br>R$ 2.450,00</div>', unsafe_allow_html=True)

    with col_sal: 
        # Card de Saldo (Dourado)
        st.markdown('<div class="card saldo">SALDO<br>R$ 2.550,00</div>', unsafe_allow_html=True)

    with col_ava: 
        # Bloco do Avatar e Mensagem de impacto
        # PARA ALTERAR: O link em 'src' é a foto. Você pode trocar por uma foto sua no Google Drive (link direto).
        st.markdown(f'''
            <div class="avatar-container">
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="img-avatar">
                <div>Opa! Você gastou 49% do recebido em {mes_sel}!</div>
            </div>
        ''', unsafe_allow_html=True)
        # Barra de progresso visual (0.49 significa 49%)
        st.progress(0.49) 

    # Linha preta com afastamento de 70px (definida no CSS como barra-afastada)
    st.markdown('<div class="barra-afastada"></div>', unsafe_allow_html=True) 

    # --- SEÇÃO DE DETALHAMENTO (CARDS VERTICAIS) ---
    st.markdown("### Detalhamento de Despesas")
    
    # Criamos colunas para os cards verticais não ocuparem a tela inteira
    col_cards, col_espaco = st.columns([1, 2])
    
    with col_cards:
        # Card Laranja (A Pagar)
        st.markdown('<div class="card-vertical card-pagar"><b>DESPESA A PAGAR<br>R$ 1.200,00</b></div>', unsafe_allow_html=True)
        # Card Grafite (Prevista)
        st.markdown('<div class="card-vertical card-prevista"><b>DESPESA PREVISTA<br>R$ 800,00</b></div>', unsafe_allow_html=True)
        # Card Azul (Cartões Específicos)
        st.markdown('<div class="card-vertical card-cartao"><b>NUBANK<br>R$ 450,00</b></div>', unsafe_allow_html=True)

# --- 10. TELA DE CONFIGURAÇÕES E CADASTROS ---

if selecionado == "Cadastros Iniciais":
    st.markdown("## ⚙️ Configurações e Cadastros")
    st.markdown("---")
    
    # Criamos 3 colunas principais para organizar tudo verticalmente na tela
    # [1, 1, 1] significa que as 3 colunas têm o mesmo tamanho
    col_desp, col_rec, col_pgto = st.columns([1, 1, 1])

    # --- COLUNA 1: GESTÃO DE DESPESAS ---
    with col_desp:
        st.markdown("### 🔴 Categoria Despesa")
        
        # O Popover cria um menu flutuante para não ocupar espaço na tela
        with st.popover("➕ Inserir Categoria", use_container_width=True):
            n_cat = st.text_input("Nome (Ex: Casa)", key="new_cat_desp")
            if st.button("Salvar", key="btn_save_desp", use_container_width=True):
                if n_cat and n_cat not in st.session_state.categorias:
                    # Adiciona à lista temporária
                    st.session_state.categorias.append(n_cat)
                    # SALVAMENTO NA NUVEM: Envia a nova lista para o Google Sheets (Aba Config)
                    salvar_configuracoes_nuvem() 
                    st.success(f"✅ Categoria '{n_cat}' cadastrada!")
                    st.rerun() # Atualiza a tela para o botão da categoria aparecer
        
        st.write("") # Pequeno espaço vertical
        # CRIAÇÃO AUTOMÁTICA DE BOTÕES: Para cada categoria na lista, cria um botão
        for cat in st.session_state.categorias:
            # Ao clicar no botão da categoria (ex: LANCHE), abre o modal de lançamento
            if st.button(f"🔻 {cat.upper()}", use_container_width=True, key=f"btn_d_{cat}"):
                modal_lancamento_categoria(cat)

    # --- COLUNA 2: GESTÃO DE RECEITAS (GANHOS) ---
    with col_rec:
        st.markdown("### 🟢 Fonte de Receita")
        
        with st.popover("💰 Inserir Fonte", use_container_width=True):
            n_rec = st.text_input("Nome (Ex: Salário)", key="new_cat_rec")
            if st.button("Salvar", key="btn_save_rec", use_container_width=True):
                # Garante que a lista de receitas exista antes de adicionar
                if 'categorias_receita' not in st.session_state:
                    st.session_state.categorias_receita = []
                
                if n_rec and n_rec not in st.session_state.categorias_receita:
                    st.session_state.categorias_receita.append(n_rec)
                    # SINCRONIZA COM GOOGLE: Salva a nova fonte na aba Config
                    salvar_configuracoes_nuvem()
                    st.success(f"✅ Fonte '{n_rec}' cadastrada!")
                    st.rerun()
        
        st.write("") 
        # Mostra os botões de Receita (apenas se a lista existir)
        if 'categorias_receita' in st.session_state:
            for cat_r in st.session_state.categorias_receita:
                # Ao clicar, abre o modal de receita que configuramos no Bloco 7
                if st.button(f"🔺 {cat_r.upper()}", use_container_width=True, key=f"btn_r_{cat_r}"):
                    modal_receita_categoria(cat_r)

    # --- COLUNA 3: GESTÃO DE PAGAMENTOS E CARTÕES ---
    with col_pgto:
        st.markdown("### 💳 Forma Pagto/Receb")
        # Este botão abre o gerenciador completo (Cadastro, Edição e Exclusão)
        if st.button("⚙️ Gerenciar Formas", use_container_width=True):
            modal_forma_pagamento()
        
        st.write("") 
        # Lista apenas os nomes das formas já cadastradas para conferência visual
        if 'formas_pagamento' in st.session_state:
            for f in st.session_state.formas_pagamento:
                # st.caption cria um texto menor e mais discreto
                st.caption(f"✅ {f['nome']}")





























































































































































































