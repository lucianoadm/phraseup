import streamlit as st
import sys
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Configuração de path e imports locais
sys.path.insert(0, ".")
from utils.db import get_library, delete_from_library
import csv, io
from components.sidebar import render_sidebar

# 1. CONFIGURAÇÃO DA PÁGINA (OBRIGATÓRIO SER O PRIMEIRO ST)
st.set_page_config(
    page_title="Cognivus LexOS - Inteligência Cognitiva",
    page_icon="🧠",
    layout="wide", # Wide é melhor para ver gráficos e radares
    initial_sidebar_state="expanded"
)

# 2. DEFINIÇÃO DA TRAVA DE SEGURANÇA
def validar_acesso():
    params = st.query_params
    token = params.get("token")
    timestamp = params.get("t")
    agora_ms = int(time.time() * 1000)
    
    # Aumentei para 20s porque apps com muitas bibliotecas (pandas, plotly, wordcloud) 
    # demoram um pouco mais para carregar no servidor.
    validade_ms = 20000 
    
    if token and timestamp:
        try:
            tempo_decorrido = agora_ms - int(timestamp)
            if tempo_decorrido > validade_ms or len(token) < 10:
                st.error("🚫 Link de acesso expirado ou inválido.")
                st.info("Por favor, acesse o sistema através do Portal Cognivus.")
                st.stop()
        except ValueError:
            st.error("🚫 Parâmetros de segurança corrompidos.")
            st.stop()
    else:
        st.warning("⚠️ Acesso restrito. Por favor, faça login no Portal oficial.")
        st.stop()

# 3. EXECUÇÃO DA VALIDAÇÃO
validar_acesso()

# ---------------------------------------------------------
# 4. RENDERIZAÇÃO E LÓGICA DO APP
# ---------------------------------------------------------
st.title("📚 Biblioteca LexOS")
render_sidebar()

# Seu código continua aqui...

# Exemplo de uso do DB e do User_ID:
# user_data = db.collection("usuarios").document(user_id).get()


st.markdown("""
<div class='page-header'>
  <h1>📚 Minha Biblioteca</h1>
  <p>Suas frases refinadas favoritas — seu vocabulário pessoal em construção.</p>
</div>
""", unsafe_allow_html=True)

# Carrega até 100 itens
items = get_library(100)

if not items:
    st.info("Sua biblioteca está vazia. Refine algumas frases e salve as que mais gostar!")
    st.stop()

# Export CSV
if st.button("⬇️ Exportar como CSV"):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Original", "Refinado", "Nível", "Salvo em"])

    for row in items:
        # row = (id, input_text, output_text, level, created_at)
        writer.writerow(row[1:])  # ignora o ID

    st.download_button(
        label="📥 Baixar CSV",
        data=output.getvalue(),
        file_name="phraseup_biblioteca.csv",
        mime="text/csv"
    )

st.markdown(f"**{len(items)} frase(s) salva(s)**")
st.markdown("---")

# Search
search = st.text_input("🔍 Buscar na biblioteca", placeholder="Digite uma palavra...")

for item in items:
    # Agora são 5 valores
    lib_id, original, refined, level, saved_at = item

    # Filtro de busca
    if search and search.lower() not in (original + refined).lower():
        continue

    col_card, col_del = st.columns([10, 1])

    with col_card:
        tag_class = "tag-prof" if "prof" in (level or "").lower() else "tag-pos"

        st.markdown(f"""
        <div class='lib-card'>
          <div class='lib-original'>Original: "{original}"</div>
          <span class='response-card-header {tag_class}'>{level or "Refinado"}</span>
          <div class='lib-phrase'>"{refined}"</div>
          <div class='lib-meta'>{saved_at[:10]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_del:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑", key=f"del_{lib_id}", help="Remover da biblioteca"):
            delete_from_library(lib_id)
            st.rerun()
