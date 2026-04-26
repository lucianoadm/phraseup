import streamlit as st
from core.config import validate_keys
from services.refinement import refine_text
from components.sidebar import render_sidebar

import streamlit as st

def verificar_acesso_portal():
    # Tenta obter o token e o timestamp da URL
    query_params = st.query_params
    token = query_params.get("token")
    
    if not token:
        # Se não houver token, bloqueia tudo e para o script
        st.error("🚫 Acesso Negado: Este módulo deve ser acedido através do Portal Cognivus.")
        st.info("Por favor, faça login em: https://cognivus.com.br")
        st.stop() # Interrompe a execução do app aqui

# Chamar a verificação antes de qualquer outra coisa
verificar_acesso_portal()

# ... restante do seu código (layout, lógica, etc.)

# Configuração da página (sempre antes de qualquer renderização)
st.set_page_config(
    page_title="PhraseUp",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Renderiza a sidebar global
render_sidebar()

# -------------------------------------------------
# CONFIGURAÇÃO BÁSICA
# -------------------------------------------------

st.set_page_config(
    page_title="PhraseUp",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# TEMA VISUAL + MODO ESCURO
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
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        padding: 10px 0;
        background-color: rgba(15,23,42,0.92);
        text-align: center;
        font-size: 12px;
        color: #CBD5F5;
        border-top: 1px solid #1F2937;
        z-index: 9999;
    }}
    .footer a {{
        color: #E5E7EB;
        text-decoration: none;
        margin: 0 8px;
    }}
    .footer a:hover {{
        color: #FFFFFF;
    }}
    .footer img {{
        vertical-align: middle;
        margin-right: 4px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------
# VALIDAÇÃO INICIAL
# -------------------------------------------------
validate_keys()

# -------------------------------------------------
# CABEÇALHO PRINCIPAL COM LOGO
# -------------------------------------------------
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
        result = refine_text(user_input)
        st.markdown(
            f"""
            <div class="result-card">
                {result}
            </div>
            """,
            unsafe_allow_html=True,
        )
