import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão Financeira", layout="wide")

# 2. ESTILO VISUAL (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        border-bottom: 5px solid #10b981;
    }
    [data-testid="stMetricValue"] { color: #1e293b; font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXÃO COM A PLANILHA
url = "https://docs.google.com/spreadsheets/d/1PyE9M6KLjJDtIDuCO5DCCTTcz-jsVr3Gj3Cv9yrxPE0/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    df = conn.read(spreadsheet=url)
    df = df.dropna(how='all')
    
    # Padronizando nomes das colunas (Tira espaços e deixa a primeira letra maiúscula)
    df.columns = [c.strip().title() for c in df.columns]

    # Tratando a coluna 'Valor' para virar número real
    if 'Valor' in df.columns:
        df['Valor'] = df['Valor'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    df = pd.DataFrame()

# 4. BARRA LATERAL
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://www.w3schools.com/howto/img_avatar.png", width=100)
    st.markdown("### Olá, Renan Soares")
    st.divider()
    menu = st.radio("Navegação", ["Painel Inicial", "Configurações"])

# 5. CONTEÚDO PRINCIPAL
if menu == "Painel Inicial":
    st.title("📊 Painel Financeiro")
    
    if not df.empty:
        # Cálculos para os cards
        # Se não houver coluna 'Status', ele mostra 0 para evitar erro
        total_pago = 0
        if 'Status' in df.columns:
            total_pago = df[df['Status'].str.strip().str.title() == 'Pago']['Valor'].sum()
        
        total_geral = df['Valor'].sum()
        pendente = total_geral - total_pago

        # Exibição dos Cards (Igual às fotos)
        col1, col2, col3 = st.columns(3)
        col1.metric("TOTAL PAGO", f"R$ {total_pago:,.2f}")
        col2.metric("PENDENTE", f"R$ {pendente:,.2f}")
        col3.metric("TOTAL GERAL", f"R$ {total_geral:,.2f}")

        st.divider()
        
        # Tabela Detalhada
        st.subheader("📋 Detalhes da Planilha")
        
        # Colorindo a coluna Status se ela existir
        if 'Status' in df.columns:
            def color_status(val):
                color = '#10b981' if str(val).strip().title() == 'Pago' else '#f97316'
                return f'color: {color}; font-weight: bold'
            
            st.dataframe(df.style.applymap(color_status, subset=['Status']), use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Planilha carregada, mas sem dados para exibir.")