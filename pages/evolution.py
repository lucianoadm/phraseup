import streamlit as st
from utils.db import get_history
import pandas as pd
import altair as alt
from datetime import datetime
from components.sidebar import render_sidebar
# ---------------------------------------------------------
# 2. INICIALIZAÇÃO SEGURA DO FIREBASE (VIA SECRETS)
# ---------------------------------------------------------
# 1. CONFIGURAÇÃO (Deve ser a primeira linha)
st.set_page_config(page_title="Chat - PhraseUp", layout="centered")

# 2. INICIALIZAÇÃO SEGURA DO FIREBASE
def iniciar_firebase():
    # Se o app já estiver inicializado, apenas retorna o cliente
    if not firebase_admin._apps:
        try:
            # Puxa do st.secrets e garante que é um dicionário limpo
            fb_dict = dict(st.secrets["firebase"])
            
            # Limpeza crucial da chave privada
            if "private_key" in fb_dict:
                fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erro ao conectar ao Firebase: {e}")
            st.stop()
    
    return firestore.client()

# Inicializa o banco
db = iniciar_firebase()

# 3. TRAVA DE SEGURANÇA (Usando Session State para não dar erro ao trocar de aba)
def validar_acesso():
    # Se já validou no app.py, libera direto
    if "autenticado" in st.session_state and st.session_state["autenticado"]:
        return st.session_state.get("user_id")

    # Se não, tenta validar pela URL
    params = st.query_params
    token = params.get("token")
    t = params.get("t")
    
    if token and t:
        try:
            agora = int(time.time() * 1000)
            if (agora - int(t)) < 30000: # 30 segundos
                st.session_state["autenticado"] = True
                st.session_state["user_id"] = token
                return token
        except:
            pass

    # Se falhar em tudo
    st.error("🚫 Acesso negado. Use o Portal Cognivus.")
    st.stop()

user_id = validar_acesso()

# 4. RESTANTE DO SEU CÓDIGO...
st.title("💬 Chat PhraseUp")

# Exemplo de uso do DB e do User_ID:
# user_data = db.collection("usuarios").document(user_id).get()

# -------------------------
# 🎨 Estilo avançado
# -------------------------
st.markdown("""
<style>
.metric-card {
    background: #ffffff15;
    padding: 18px 22px;
    border-radius: 14px;
    border: 1px solid #ffffff25;
    backdrop-filter: blur(6px);
    margin-bottom: 12px;
}
.level-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    margin-right: 8px;
}
.level-basico { background: #1e40af; color: #dbeafe; }
.level-profissional { background: #065f46; color: #a7f3d0; }
.level-persuasivo { background: #92400e; color: #fcd34d; }
.insight-card {
    background: #0f172a;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #1e293b;
    margin-bottom: 10px;
    color: #e2e8f0;
}
.time-card {
    background: #1e293b;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 12px;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Título
# -------------------------
st.title("📈 Minha Evolução")
st.markdown("Acompanhe sua evolução no uso da linguagem ao longo do tempo.")

history = get_history(limit=200)

if not history:
    st.info("Nenhum dado disponível ainda.")
    st.stop()

# -------------------------
# 📊 Processamento dos dados
# -------------------------
total_texts = len(history)

total_words_input = 0
total_words_output = 0

levels_count = {
    "basico": 0,
    "profissional": 0,
    "persuasivo": 0
}

dates = []

for input_text, output_text, level, created_at in history:
    total_words_input += len(input_text.split())
    total_words_output += len(output_text.split())

    if level in levels_count:
        levels_count[level] += 1

    dates.append(datetime.strptime(created_at[:10], "%Y-%m-%d"))

avg_input = total_words_input / total_texts
avg_output = total_words_output / total_texts
gain = avg_output - avg_input

score = min(100, int((gain * 5) + total_texts))

# -------------------------
# ⏳ Tempo de uso
# -------------------------
first_use = min(dates)
days_using = (datetime.now() - first_use).days + 1
avg_texts_per_day = total_texts / days_using

# -------------------------
# 📌 Visão Geral — Cards Premium
# -------------------------
st.subheader("📌 Visão Geral")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0; font-size:22px;">{total_texts}</h3>
        <p style="opacity:0.7; margin:0;">Textos analisados</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0; font-size:22px;">{avg_input:.1f}</h3>
        <p style="opacity:0.7; margin:0;">Média palavras (antes)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0; font-size:22px;">{avg_output:.1f}</h3>
        <p style="opacity:0.7; margin:0;">Média palavras (depois)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-card">
    <h3 style="margin:0; font-size:22px;">{gain:.1f}</h3>
    <p style="opacity:0.7; margin:0;">📈 Ganho médio de vocabulário</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# ⏳ Cartões de tempo de uso
# -------------------------
st.subheader("⏳ Tempo de Uso do App")

colA, colB = st.columns(2)

with colA:
    st.markdown(f"""
    <div class="time-card">
        <h3 style="margin:0; font-size:22px;">{days_using} dias</h3>
        <p style="opacity:0.7; margin:0;">Desde o primeiro uso</p>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown(f"""
    <div class="time-card">
        <h3 style="margin:0; font-size:22px;">{avg_texts_per_day:.1f}/dia</h3>
        <p style="opacity:0.7; margin:0;">Média de textos por dia</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# 📊 Uso por nível — Badges com contraste corrigido
# -------------------------
st.subheader("🎯 Uso por nível de refinamento")

st.markdown(f"""
<span class="level-badge level-basico">Básico: {levels_count['basico']}</span>
<span class="level-badge level-profissional">Profissional: {levels_count['profissional']}</span>
<span class="level-badge level-persuasivo">Persuasivo: {levels_count['persuasivo']}</span>
""", unsafe_allow_html=True)

# -------------------------
# 📈 Gráfico de evolução
# -------------------------
st.subheader("📊 Evolução ao longo do tempo")

df = pd.DataFrame({
    "Data": dates,
    "Textos": list(range(1, len(dates) + 1))
})

chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x="Data:T",
        y="Textos:Q",
        tooltip=["Data", "Textos"]
    )
    .properties(height=300)
)

st.altair_chart(chart, use_container_width=True)

# -------------------------
# 🏆 Score de Evolução — Card + Barra
# -------------------------
st.subheader("🏆 Score de Evolução")

st.markdown(f"""
<div class="metric-card">
    <h3 style="margin:0; font-size:26px;">{score}/100</h3>
    <p style="opacity:0.7; margin:0;">Seu score atual</p>
</div>
""", unsafe_allow_html=True)

st.progress(score / 100)

# -------------------------
# 💡 Insights — Fundo corrigido
# -------------------------
st.subheader("💡 Insights")

if gain > 5:
    st.markdown("""
    <div class="insight-card">
        🚀 <strong>Vocabulário em expansão!</strong><br>
        Seu ganho médio de palavras está excelente.
    </div>
    """, unsafe_allow_html=True)

elif gain > 2:
    st.markdown("""
    <div class="insight-card">
        👍 <strong>Boa evolução!</strong><br>
        Continue praticando para melhorar ainda mais.
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="insight-card">
        📘 <strong>Você pode evoluir mais!</strong><br>
        Experimente níveis mais avançados para enriquecer seu vocabulário.
    </div>
    """, unsafe_allow_html=True)

if levels_count["persuasivo"] > levels_count["basico"]:
    st.markdown("""
    <div class="insight-card">
        🎯 <strong>Foco em impacto!</strong><br>
        Você está usando mais o nível persuasivo — ótimo para comunicação estratégica.
    </div>
    """, unsafe_allow_html=True)
