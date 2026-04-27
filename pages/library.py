import streamlit as st
import sys
sys.path.insert(0, ".")
from utils.db import get_library, delete_from_library
import csv, io
from components.sidebar import render_sidebar
# ---------------------------------------------------------
# 2. INICIALIZAÇÃO SEGURA DO FIREBASE (VIA SECRETS)
# ---------------------------------------------------------
def iniciar_firebase():
    if not firebase_admin._apps:
        # Puxa os dados do Secrets
        fb_dict = dict(st.secrets["firebase"])
        
        # LIMPEZA CRUCIAL: Remove escapes extras e garante que a chave 
        # seja lida corretamente pelo motor do Firebase
        if "private_key" in fb_dict:
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            
        cred = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# ---------------------------------------------------------
# 3. TRAVA DE SEGURANÇA COGNIVUS (TOKEN + TIMESTAMP)
# ---------------------------------------------------------
def validar_acesso():
    params = st.query_params
    token = params.get("token")
    timestamp = params.get("t")
    agora_ms = int(time.time() * 1000)
    
    # Validade de 20 segundos (margem para carregamento do server)
    validade_ms = 20000 
    
    if token and timestamp:
        try:
            tempo_decorrido = agora_ms - int(timestamp)
            
            # Se o link for velho ou o token for inválido
            if tempo_decorrido > validade_ms or len(token) < 10:
                st.error("🚫 Link de acesso expirado ou inválido.")
                st.info("Por favor, acesse o sistema através do Portal Cognivus.")
                st.stop()
            return token # Retorna o UID do usuário para uso posterior
        except (ValueError, TypeError):
            st.error("🚫 Parâmetros de segurança corrompidos.")
            st.stop()
    else:
        st.warning("⚠️ Acesso restrito. Por favor, use o Portal oficial.")
        st.stop()

# Executa a trava
user_id = validar_acesso()

# ---------------------------------------------------------
# 4. RENDERIZAÇÃO E LÓGICA DO APP
# ---------------------------------------------------------
st.title("Cognivus LexOS")
render_sidebar()

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
