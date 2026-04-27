import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore
from core.config import validate_keys
from services.refinement import refine_text
from components.sidebar import render_sidebar

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA (OBRIGATÓRIO: PRIMEIRO COMANDO)
# ---------------------------------------------------------
st.set_page_config(
    page_title="PhraseUp",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="expanded"
)

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
