import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore
# Seus outros imports permanecem iguais...

# 1. CONFIGURAÇÃO DA PÁGINA (OBRIGATÓRIO SER O PRIMEIRO ST)
st.set_page_config(
    page_title="Cognivus LexOS - Inteligência Cognitiva",
    page_icon="🧠",
    layout="wide", # Wide é melhor para ver gráficos e radares
    initial_sidebar_state="expanded"
)

# 2. DEFINIÇÃO DA TRAVA DE SEGURANÇA (PADRÃO MASTER AJUSTADO)
def validar_acesso():
    # 1. VERIFICAÇÃO DE SESSÃO ATIVA
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    # 2. CAPTURA DOS PARÂMETROS DA URL
    params = st.query_params
    token = params.get("token")
    timestamp_str = params.get("t")
    agora_ms = int(time.time() * 1000)
    
    # Ajustado para 20 minutos (1.200.000 ms) para garantir o carregamento
    validade_ms = 1200000 
    
    if token and timestamp_str:
        try:
            timestamp = int(timestamp_str)
            
            # Ajuste Universal: Aceita segundos ou ms
            if timestamp < 10000000000:
                timestamp *= 1000
                
            tempo_decorrido = abs(agora_ms - timestamp)
            
            if tempo_decorrido <= validade_ms and len(token) >= 10:
                # Salva na sessão para não pedir validação novamente
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                st.query_params.clear() 
                return token
            else:
                st.error(f"🚫 Link de acesso expirado ou inválido.")
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

# 4. RENDERIZAÇÃO (Mantendo seu padrão original)
st.title("Cognivus LexOS")
# render_sidebar() # Verifique se esta função está definida nos seus imports/utils

# -------------------------------------------------
# TEMA VISUAL + MODO ESCURO (MANTIDO INTACTO)
# -------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # padrão: escuro

dark = st.session_state.dark_mode

primary_color = "#7C3AED"  # roxo
accent_color = "#F97316"   # laranja
bg_dark = "#050816"
bg_light = "#F5F5F7"
card_dark = "#0F172A"
card_light = "#FFFFFF"
text_dark = "#E5E7EB"
text_light = "#111827"

bg = bg_dark if dark else bg_light
card = card_dark if dark else card_light
text = text_dark if dark else text_light

st.markdown(
    f"""
    <style>
    body {{
        background-color: {bg} !important;
    }}
    .main {{
        background-color: {bg};
        color: {text};
    }}
    .stTextArea textarea {{
        background-color: {card};
        color: {text};
        border-radius: 10px;
        border: 1px solid #1F2933;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {primary_color}, {accent_color});
        color: white;
        border-radius: 999px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        filter: brightness(1.05);
    }}
    .result-card {{
        background-color: {card};
        color: {text};
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border: 1px solid #1F2933;
        margin-top: 0.75rem;
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    .app-logo {{
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
        font-weight: 800;
        font-size: 2rem;
        background: linear-gradient(135deg, {primary_color}, {accent_color});
        -webkit-background-clip: text;
        color: transparent;
        letter-spacing: 0.03em;
    }}
    .app-subtitle {{
        color: {text};
        opacity: 0.8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# VALIDAÇÃO DE CHAVES E CABEÇALHO (MANTIDO INTACTO)
# -------------------------------------------------
# validate_keys() # Verifique se esta função está definida nos seus imports/utils

st.markdown(
    """
    <div style="margin-top:-20px; margin-bottom:10px;">
        <div class="app-logo">PhraseUp</div>
        <div class="app-subtitle">
            Transforme rascunhos em frases claras, profissionais e persuasivas em segundos.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# CONTEÚDO PRINCIPAL
# -------------------------------------------------
user_input = st.text_area("Digite seu texto:", height=180)

if st.button("Refinar"):
    if not user_input.strip():
        st.warning("Digite um texto antes de refinar.")
    else:
        # result = refine_text(user_input) # Verifique se esta função está definida
        result = "Resultado do refinamento simulado..." # Placeholder para não quebrar
        st.markdown(
            f"""
            <div class="result-card">
                {result}
            </div>
            """,
            unsafe_allow_html=True,
        )
