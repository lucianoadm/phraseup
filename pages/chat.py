import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore

# 1. CONFIGURAÇÃO (Deve ser a primeira linha)
st.set_page_config(page_title="Chat - PhraseUp", layout="centered")

# 2. INICIALIZAÇÃO SEGURA DO FIREBASE
def iniciar_firebase():
    # Se o app já estiver inicializado, apenas retorna o cliente
    if not firebase_admin._apps:
        try:
            # Puxa do st.secrets e garante que é um dicionário limpo
            fb_dict = dict(st.secrets["firebase"])
            
            # Limpeza crucial da chave privada
            if "private_key" in fb_dict:
                fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erro ao conectar ao Firebase: {e}")
            st.stop()
    
    return firestore.client()

# Inicializa o banco
db = iniciar_firebase()

# 3. TRAVA DE SEGURANÇA (Usando Session State para não dar erro ao trocar de aba)
def validar_acesso():
    # Se já validou no app.py, libera direto
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    # Se não, tenta validar pela URL
    params = st.query_params
    token = params.get("token")
    t = params.get("t")
    
    if token and t:
        try:
            agora = int(time.time() * 1000)
            if (agora - int(t)) < 30000: # 30 segundos
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                return token
        except:
            pass

    # Se falhar em tudo
    st.error("🚫 Acesso negado. Use o Portal Cognivus.")
    st.stop()

user_id = validar_acesso()

# 4. RESTANTE DO SEU CÓDIGO...
st.title("💬 Chat PhraseUp")

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
