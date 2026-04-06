import streamlit as st

def render_sidebar():
    # Cores baseadas no seu design
    primary_color = "#7C3AED"
    accent_color = "#F97316"
    text_color = "#31333F"  # Cor padrão do texto (ajuste para branco se o tema for escuro)

    with st.sidebar:
        # -----------------------------
        # CABEÇALHO (LOGO + AVATAR)
        # -----------------------------
        # Removi o container de texto interno para evitar conflitos de renderização
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
        # NAVEGAÇÃO (Onde geralmente ocorre o erro)
        # -----------------------------
        st.markdown("**Navegação**")
        
        # O st.page_link só funciona se os arquivos existirem. 
        # Se estiver testando apenas o layout, use botões ou markdown simples.
        try:
            st.page_link("app.py", label="Início", icon="🏠")
            st.page_link("pages/library.py", label="Biblioteca", icon="📚")
            st.page_link("pages/evolution.py", label="Evolução", icon="📈")
            st.page_link("pages/training.py", label="Treinamento", icon="🎓")
        except Exception:
            # Fallback caso os arquivos .py não estejam criados
            st.info("Arquivos de páginas não detectados.")
            st.write("🏠 Início")
            st.write("📚 Biblioteca")

        st.divider()

        # -----------------------------
        # RODAPÉ (CRÉDITOS)
        # -----------------------------
        # Use st.markdown para links externos de forma limpa
        st.markdown(
            f"""
            <div style="font-size:13px; line-height:1.6;">
                <strong>Criado por Luciano Paiva</strong><br>
                Construído com Python & IA.
                <br><br>
                <a href="https://github.com/lucianoadm" style="text-decoration:none;">🐙 GitHub</a><br>
                <a href="https://linkedin.com/in/luciano-paiva-b0b01a19b" style="text-decoration:none;">💼 LinkedIn</a>
            </div>
            <div style="font-size:11px; margin-top:20px; opacity:0.6;">
                © 2024 — Todos os direitos reservados.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Para testar localmente
if __name__ == "__main__":
    render_sidebar()
