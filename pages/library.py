import streamlit as st
import sys
sys.path.insert(0, ".")
from utils.db import get_library, delete_from_library
import csv, io
from components.sidebar import render_sidebar
render_sidebar()

st.markdown("""
<div class='page-header'>
  <h1>📚 Minha Biblioteca</h1>
  <p>Suas frases refinadas favoritas — seu vocabulário pessoal em construção.</p>
</div>
""", unsafe_allow_html=True)

# Carrega até 100 itens
items = get_library(100)

if not items:
    st.info("Sua biblioteca está vazia. Refine algumas frases e salve as que mais gostar!")
    st.stop()

# Export CSV
if st.button("⬇️ Exportar como CSV"):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Original", "Refinado", "Nível", "Salvo em"])

    for row in items:
        # row = (id, input_text, output_text, level, created_at)
        writer.writerow(row[1:])  # ignora o ID

    st.download_button(
        label="📥 Baixar CSV",
        data=output.getvalue(),
        file_name="phraseup_biblioteca.csv",
        mime="text/csv"
    )

st.markdown(f"**{len(items)} frase(s) salva(s)**")
st.markdown("---")

# Search
search = st.text_input("🔍 Buscar na biblioteca", placeholder="Digite uma palavra...")

for item in items:
    # Agora são 5 valores
    lib_id, original, refined, level, saved_at = item

    # Filtro de busca
    if search and search.lower() not in (original + refined).lower():
        continue

    col_card, col_del = st.columns([10, 1])

    with col_card:
        tag_class = "tag-prof" if "prof" in (level or "").lower() else "tag-pos"

        st.markdown(f"""
        <div class='lib-card'>
          <div class='lib-original'>Original: "{original}"</div>
          <span class='response-card-header {tag_class}'>{level or "Refinado"}</span>
          <div class='lib-phrase'>"{refined}"</div>
          <div class='lib-meta'>{saved_at[:10]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_del:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑", key=f"del_{lib_id}", help="Remover da biblioteca"):
            delete_from_library(lib_id)
            st.rerun()