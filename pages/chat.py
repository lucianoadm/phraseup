import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore

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
