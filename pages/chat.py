import streamlit as st
import time
import sys
import os

# 1. AJUSTE DE PATH (INCISIVO: Garante que o Python ache a pasta utils, components e services)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import firebase_admin
from firebase_admin import credentials, firestore

# 2. IMPORTS LOCAIS (Obrigatórios para evitar o NameError)
from components.sidebar import render_sidebar
from utils.db import init_db, save_history, get_history
from services.refinement import refine_text

# 3. CONFIGURAÇÃO DA PÁGINA (OBRIGATÓRIO SER O PRIMEIRO COMANDO ST)
st.set_page_config(
    page_title="Cognivus LexOS - Inteligência Cognitiva",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 4. DEFINIÇÃO DA TRAVA DE SEGURANÇA (PADRÃO MASTER)
def validar_acesso():
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    params = st.query_params
    token = params.get("token")
    timestamp_str = params.get("t")
    agora_ms = int(time.time() * 1000)
    
    validade_ms = 1200000 # 20 minutos
    
    if token and timestamp_str:
        try:
            timestamp = int(timestamp_str)
            if timestamp < 10000000000:
                timestamp *= 1000
            tempo_decorrido = abs(agora_ms - timestamp)
            
            if tempo_decorrido <= validade_ms and len(token) >= 10:
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                st.query_params.clear() 
                return token
            else:
                st.error("🚫 Link de acesso expirado ou inválido.")
                st.stop()
        except Exception as e:
            st.error(f"🚫 Falha na validação: {e}")
            st.stop()
    else:
        st.warning("⚠️ Acesso restrito. Por favor, faça login no Portal oficial.")
        st.stop()

# 5. EXECUÇÃO DA VALIDAÇÃO
validar_acesso()

# 6. RENDERIZAÇÃO E LÓGICA DO APP (PRESERVAÇÃO TOTAL)
render_sidebar()
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
                # Chama sua lógica de IA original
                resultado = refine_text(user_input, level)
                save_history(user_input, resultado, level)

                st.success("Texto refinado com sucesso!")
                st.subheader("Resultado:")
                st.write(resultado)
            except Exception as e:
                st.error(f"Erro ao processar: {e}")

# Histórico rápido
st.markdown("---")
st.subheader("🕓 Últimos refinamentos")

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
