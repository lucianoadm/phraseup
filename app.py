import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore
# Seus outros imports permanecem iguais...

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="PhraseUp",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. INICIALIZAÇÃO SEGURA DO FIREBASE
def iniciar_firebase():
    if not firebase_admin._apps:
        fb_dict = dict(st.secrets["firebase"])
        if "private_key" in fb_dict:
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n").strip()
        cred = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = iniciar_firebase()

# 3. TRAVA DE SEGURANÇA (COM MEMÓRIA DE SESSÃO)
def validar_acesso():
    # AQUI ESTÁ A CORREÇÃO: Se já validamos antes, apenas libera o acesso
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state["user_id"]

    params = st.query_params
    token = params.get("token")
    timestamp = params.get("t")
    agora_ms = int(time.time() * 1000)
    
    # Aumentei para 10 minutos (600000ms) para evitar erros de lentidão no primeiro acesso
    validade_ms = 600000 
    
    if token and timestamp:
        try:
            # abs() corrige problemas caso os relógios dos servidores estejam levemente dessincronizados
            tempo_decorrido = abs(agora_ms - int(timestamp))
            
            if tempo_decorrido <= validade_ms and len(token) >= 10:
                # SALVA NA SESSÃO: Isso permite que o usuário mude de página sem ser expulso
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                return token
            else:
                st.error(f"🚫 Link expirado. Atraso de {tempo_decorrido // 1000}s.")
                st.stop()
        except:
            st.error("🚫 Erro nos parâmetros de segurança.")
            st.stop()
    else:
        st.warning("⚠️ Acesso restrito. Por favor, use o Portal oficial.")
        st.stop()

# Executa a trava
user_id = validar_acesso()

# 4. RENDERIZAÇÃO
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
