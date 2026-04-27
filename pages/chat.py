# pages/chat.py

import streamlit as st
from services.refinement import refine_text
from utils.db import save_history, init_db
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
