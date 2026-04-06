# pages/chat.py

import streamlit as st
from services.refinement import refine_text
from utils.db import save_history, init_db
from components.sidebar import render_sidebar
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