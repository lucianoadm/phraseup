# pages/training.py

import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore
from services.refinement import refine_text
from components.sidebar import render_sidebar

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO (Primeiro comando Streamlit)
# ---------------------------------------------------------
st.set_page_config(page_title="Training - PhraseUp", layout="centered")

# ---------------------------------------------------------
# 2. INICIALIZAÇÃO SEGURA DO FIREBASE (VIA SECRETS)
# ---------------------------------------------------------
def iniciar_firebase():
    if not firebase_admin._apps:
        try:
            if "firebase" not in st.secrets:
                st.error("Configuração 'firebase' não encontrada nos Secrets.")
                st.stop()
                
            fb_dict = dict(st.secrets["firebase"])
            
            # Limpeza da chave PEM para evitar erros de Padding
            if "private_key" in fb_dict:
                fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n").strip()
                
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erro ao conectar ao Firebase: {e}")
            st.stop()
    
    return firestore.client()

# Inicializa o banco de dados
db = iniciar_firebase()

# ---------------------------------------------------------
# 3. TRAVA DE SEGURANÇA COGNIVUS (TOKEN + SESSION STATE)
# ---------------------------------------------------------
def validar_acesso():
    # 1. Verifica se já está validado na sessão atual (permite troca de abas)
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    # 2. Se não, verifica parâmetros na URL (vinda do Portal)
    params = st.query_params
    token = params.get("token")
    timestamp = params.get("t")
    
    if token and timestamp:
        try:
            agora_ms = int(time.time() * 1000)
            tempo_decorrido = agora_ms - int(timestamp)
            
            # Margem de 30 segundos para o primeiro carregamento
            if tempo_decorrido < 30000 and len(token) >= 10:
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                return token
        except:
            pass

    # 3. Bloqueio caso falhe URL e Sessão
    st.error("🚫 Acesso restrito ou link expirado.")
    st.info("Por favor, acesse através do Portal Cognivus.")
    st.stop()

# Executa a validação
user_id = validar_acesso()

# ---------------------------------------------------------
# 4. RENDERIZAÇÃO E LÓGICA DO APP
# ---------------------------------------------------------
st.title("🎯 Treinamento LexOS")
render_sidebar()

# Prossiga com a lógica de treinamento abaixo...

# Exemplo de uso do DB e do User_ID:
# user_data = db.collection("usuarios").document(user_id).get()

st.title("🔁 Modo Treino")

st.markdown("Pratique e melhore sua escrita com desafios.")

# -------------------------
# 🎯 Frases para treino
# -------------------------

challenges = [
    "preciso melhorar esse texto urgente",
    "acho que isso não ficou muito bom",
    "podemos fazer isso depois",
    "me manda isso quando puder",
    "não gostei muito disso"
]

if "challenge" not in st.session_state:
    import random
    st.session_state.challenge = random.choice(challenges)

st.subheader("📝 Desafio")

st.write("Refine a frase abaixo:")

st.info(st.session_state.challenge)

# -------------------------
# ✍️ Entrada do usuário
# -------------------------

user_answer = st.text_area("Sua versão refinada:", height=150)

# -------------------------
# 🤖 Comparação com IA
# -------------------------

if st.button("Validar resposta", use_container_width=True):

    if not user_answer.strip():
        st.warning("Digite sua versão antes de validar.")
    else:
        with st.spinner("Analisando..."):

            # resposta ideal da IA
            ai_answer = refine_text(st.session_state.challenge, "profissional")

            st.subheader("📊 Comparação")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Sua versão:**")
                st.write(user_answer)

            with col2:
                st.markdown("**Versão sugerida pela IA:**")
                st.write(ai_answer)

            # feedback simples
            user_len = len(user_answer.split())
            ai_len = len(ai_answer.split())

            st.markdown("---")
            st.subheader("💡 Feedback")

            if user_len >= ai_len:
                st.success("Boa! Sua resposta está bem estruturada.")
            else:
                st.info("Tente enriquecer mais sua construção.")

# -------------------------
# 🔄 Novo desafio
# -------------------------

if st.button("🔄 Novo desafio"):
    import random
    st.session_state.challenge = random.choice(challenges)
    st.rerun()
