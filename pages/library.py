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

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO (Deve ser a primeira linha de Streamlit)
# ---------------------------------------------------------
st.set_page_config(page_title="Library - PhraseUp", layout="centered")

# ---------------------------------------------------------
# 2. INICIALIZAÇÃO SEGURA DO FIREBASE (VIA SECRETS)
# ---------------------------------------------------------
def iniciar_firebase():
    if not firebase_admin._apps:
        try:
            if "firebase" not in st.secrets:
                st.error("Chave 'firebase' não encontrada no Secrets.")
                st.stop()
                
            fb_dict = dict(st.secrets["firebase"])
            
            if "private_key" in fb_dict:
                fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n").strip()
                
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erro ao conectar ao Firebase: {e}")
            st.stop()
    
    return firestore.client()

# Inicializa o banco
db = iniciar_firebase()

# ---------------------------------------------------------
# 3. TRAVA DE SEGURANÇA COGNIVUS (TOKEN + SESSION STATE)
# ---------------------------------------------------------
def validar_acesso():
    # 1. Verifica se já está validado na sessão (permite navegar entre abas)
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    # 2. Se não, verifica a URL (entrada vinda do Portal)
    params = st.query_params
    token = params.get("token")
    timestamp = params.get("t")
    
    if token and timestamp:
        try:
            agora_ms = int(time.time() * 1000)
            tempo_decorrido = agora_ms - int(timestamp)
            
            # Validade de 30 segundos para entrada inicial
            if tempo_decorrido < 30000 and len(token) >= 10:
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                return token
        except:
            pass

    # 3. Bloqueio caso falhe URL e Sessão
    st.error("🚫 Acesso negado ou sessão expirada.")
    st.info("Por favor, acesse o sistema através do Portal Cognivus.")
    st.stop()

# Executa a trava
user_id = validar_acesso()

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
