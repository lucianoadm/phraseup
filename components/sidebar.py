import streamlit as st

def render_sidebar():
    # Cores baseadas no seu design
    primary_color = "#7C3AED"
    accent_color = "#F97316"

    # CSS INCISIVO: Remove os botões redundantes do topo e limpa a interface
    st.markdown("""
        <style>
            /* Oculta a navegação padrão do Streamlit (botões automáticos no topo) */
            [data-testid="stSidebarNav"] {
                display: none;
            }
            /* Remove espaçamentos excessivos no topo da sidebar */
            [data-testid="stSidebar"] .stMarkdown {
                padding-top: 0px;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # -----------------------------
        # CABEÇALHO (LOGO + AVATAR)
        # -----------------------------
        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:20px;">
                <div style="
                    width:80px; height:80px; border-radius:50%; margin:0 auto 12px auto;
                    background: radial-gradient(circle at 30% 30%, {accent_color}, {primary_color});
                    display:flex; align-items:center; justify-content:center;
                    color:white; font-size:36px; font-weight:800; box-shadow: 0 0 12px #00000033;
                ">P</div>
                <h2 style="margin:0; font-size:24px;">PhraseUp</h2>
                <p style="font-size:14px; opacity:0.8;">Refinamento inteligente de texto.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -----------------------------
        # CONFIGURAÇÕES
        # -----------------------------
        st.toggle("Modo escuro", value=True, key="dark_mode", help="Alterne o tema")
        st.divider()

        # -----------------------------
        # NAVEGAÇÃO (Única e Personalizada)
        # -----------------------------
        st.markdown("**Navegação**")
        
        try:
            # Usando page_link para navegação fluida entre os arquivos existentes
            st.page_link("app.py", label="Início", icon="🏠")
            st.page_link("pages/chat.py", label="Chat", icon="💬")
            st.page_link("pages/library.py", label="Biblioteca", icon="📚")
            st.page_link("pages/evolution.py", label="Evolução", icon="📈")
            st.page_link("pages/training.py", label="Treinamento", icon="🎓")
        except Exception:
            st.info("Arquivos de páginas não detectados ou caminhos incorretos.")

        st.divider()

        # -----------------------------
        # RODAPÉ (CRÉDITOS)
        # -----------------------------
        st.markdown(
            f"""
            <div style="font-size:13px; line-height:1.6;">
                <strong>Criado por Luciano P. de Moura</strong><br>
                Construído com Python & IA.
                <br><br>
                <a href="https://github.com/lucianoadm" style="text-decoration:none;">🐙 GitHub</a><br>
                <a href="https://linkedin.com/in/luciano-paiva-b0b01a19b" style="text-decoration:none;">💼 LinkedIn</a>
            </div>
            <div style="font-size:11px; margin-top:20px; opacity:0.6;">
                © 2026 — Todos os direitos reservados.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Para testar localmente
if __name__ == "__main__":
    render_sidebar()
