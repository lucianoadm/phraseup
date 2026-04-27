import streamlit as st
import time                    # <--- ESSENCIAL para validar o tempo
import firebase_admin          # <--- ESSENCIAL para o banco
from firebase_admin import credentials, firestore

# Seus serviços e componentes
from services.refinement import refine_text
# Certifique-se que init_db não conflite com a inicialização manual abaixo
from utils.db import save_history 
from components.sidebar import render_sidebar

# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="PhraseUp - Chat", page_icon="💬")

# 2. INICIALIZAÇÃO SEGURA DO FIREBASE
def iniciar_firebase():
    if not firebase_admin._apps:
        fb_dict = dict(st.secrets["firebase"])
        if "private_key" in fb_dict:
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = iniciar_firebase()

# 3. TRAVA DE SEGURANÇA COGNIVUS
def validar_acesso():
    # Tenta validar pela URL (entrada vinda do portal)
    params = st.query_params
    token = params.get("token")
    timestamp = params.get("t")
    agora_ms = int(time.time() * 1000)
    validade_ms = 20000 
    
    if token and timestamp:
        try:
            tempo_decorrido = agora_ms - int(timestamp)
            if tempo_decorrido < validade_ms and len(token) >= 10:
                # Opcional: guardar na session_state para não pedir token ao trocar de aba
                st.session_state["user_id"] = token
                return token
        except:
            pass

    # Se falhar na URL, verifica se já validou no app.py (Session State)
    if "user_id" in st.session_state:
        return st.session_state["user_id"]

    # Se não houver nenhum dos dois, bloqueia
    st.error("🚫 Acesso restrito ou sessão expirada.")
    st.info("Por favor, acesse através do Portal Cognivus.")
    st.stop()

# Executa a trava
user_id = validar_acesso()

# 4. RENDERIZAÇÃO E LÓGICA DO CHAT
st.title("💬 Chat Inteligente")
render_sidebar()
# ... resto do seu código

# ---------------------------------------------------------
# 4. RENDERIZAÇÃO E LÓGICA DO APP
# ---------------------------------------------------------
render_sidebar()

# Inicializa o banco ao carregar a página
init_db()

st.title("💬 Refinador de Linguagem")

st.markdown("Aprimore sua escrita com inteligência artificial.")

# Entrada do usuário
user_input = st.text_area(
    "Digite seu texto:",
    height=200,
    placeholder="Ex: preciso melhorar esse texto aqui..."
)

# Nível de refinamento
level = st.selectbox(
    "Nível de refinamento",
    ["basico", "profissional", "persuasivo"],
    index=1
)

# Botão de ação
if st.button("✨ Refinar texto", use_container_width=True):

    if not user_input.strip():
        st.warning("Digite um texto antes de refinar.")
    else:
        with st.spinner("Refinando..."):

            try:
                resultado = refine_text(user_input, level)

                # Salva no histórico
                save_history(user_input, resultado, level)

                st.success("Texto refinado com sucesso!")

                # Resultado
                st.subheader("Resultado:")
                st.write(resultado)

            except Exception as e:
                st.error(f"Erro ao processar: {e}")

# Histórico rápido (últimos registros)
st.markdown("---")
st.subheader("🕓 Últimos refinamentos")

from utils.db import get_history

history = get_history(limit=5)

if history:
    for input_text, output_text, lvl, created_at in history:
        with st.expander(f"{lvl.upper()} • {created_at[:19]}"):
            st.markdown("**Original:**")
            st.write(input_text)

            st.markdown("**Refinado:**")
            st.write(output_text)
else:
    st.info("Nenhum histórico ainda.")
