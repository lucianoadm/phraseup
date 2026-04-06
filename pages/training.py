# pages/training.py

import streamlit as st
from services.refinement import refine_text
from components.sidebar import render_sidebar
render_sidebar()

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