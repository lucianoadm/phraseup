# pages/training.py

import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore
from services.refinement import refine_text
from components.sidebar import render_sidebar

# 1. CONFIGURAÇÃO DA PÁGINA (OBRIGATÓRIO SER O PRIMEIRO ST)
st.set_page_config(
    page_title="Cognivus LexOS - Inteligência Cognitiva",
    page_icon="🧠",
    layout="wide", # Wide é melhor para ver gráficos e radares
    initial_sidebar_state="expanded"
)

# 2. DEFINIÇÃO DA TRAVA DE SEGURANÇA (PADRÃO MASTER AJUSTADO)
def validar_acesso():
    # Verifica se já houve validação nesta sessão ativa do navegador
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    params = st.query_params
    token = params.get("token")
    timestamp_str = params.get("t")
    agora_ms = int(time.time() * 1000)
    
    # Janela Master de 20 minutos (1.200.000 ms) para evitar erros de link expirado
    validade_ms = 1200000 
    
    if token and timestamp_str:
        try:
            timestamp = int(timestamp_str)
            
            # Normalização Universal: Trata segundos ou milissegundos
            if timestamp < 10000000000:
                timestamp *= 1000
                
            # Uso de abs() para mitigar dessincronização de relógio entre cliente/servidor
            tempo_decorrido = abs(agora_ms - timestamp)
            
            if tempo_decorrido <= validade_ms and len(token) >= 10:
                # Registra sucesso na sessão para navegação livre entre abas
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                st.query_params.clear() 
                return token
            else:
                st.error("🚫 Link de acesso expirado ou inválido.")
                st.info("Por favor, acesse o sistema através do Portal Cognivus.")
                st.stop()
        except Exception as e:
            st.error(f"🚫 Parâmetros de segurança corrompidos: {e}")
            st.stop()
    else:
        st.warning("⚠️ Acesso restrito. Por favor, faça login no Portal oficial.")
        st.stop()

# 3. EXECUÇÃO DA VALIDAÇÃO
validar_acesso()

# ---------------------------------------------------------
# 4. RENDERIZAÇÃO E LÓGICA DO APP (PRESERVAÇÃO TOTAL)
# ---------------------------------------------------------
st.title("🎯 Treinamento LexOS")
render_sidebar()

st.title("🔁 Modo Treino")
st.markdown("Pratique e melhore sua escrita com desafios.")

# 🎯 Frases para treino (Mantido original)
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

# ✍️ Entrada do usuário
user_answer = st.text_area("Sua versão refinada:", height=150)

# 🤖 Comparação com IA
if st.button("Validar resposta", use_container_width=True):
    if not user_answer.strip():
        st.warning("Digite sua versão antes de validar.")
    else:
        with st.spinner("Analisando..."):
            # Resposta profissional da IA
            ai_answer = refine_text(st.session_state.challenge, "profissional")

            st.subheader("📊 Comparação")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Sua versão:**")
                st.write(user_answer)

            with col2:
                st.markdown("**Versão sugerida pela IA:**")
                st.write(ai_answer)

            # Lógica de feedback (Mantido original)
            user_len = len(user_answer.split())
            ai_len = len(ai_answer.split())

            st.markdown("---")
            st.subheader("💡 Feedback")

            if user_len >= ai_len:
                st.success("Boa! Sua resposta está bem estruturada.")
            else:
                st.info("Tente enriquecer mais sua construção.")

# 🔄 Novo desafio
if st.button("🔄 Novo desafio"):
    import random
    st.session_state.challenge = random.choice(challenges)
    st.rerun()
