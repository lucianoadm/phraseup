# pages/training.py

import streamlit as st
from services.refinement import refine_text
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
