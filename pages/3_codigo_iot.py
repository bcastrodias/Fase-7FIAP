import streamlit as st
from pathlib import Path

# Caminho para o arquivo .ino (relativo à raiz do projeto)
ino_path = Path("sketch.ino")

# Tenta abrir o arquivo .ino
try:
    with open(ino_path, "r", encoding="utf-8") as f:
        ino_code = f.read()
except FileNotFoundError:
    st.error(f"Arquivo não encontrado: {ino_path}")
    st.stop()

# Interface Streamlit
st.set_page_config(page_title="Page 3 - Código IoT", layout="wide")
st.title("🔌 Código do Projeto IoT")

st.markdown("### Arquivo: `sketchIOT.ino`")
st.code(ino_code, language='cpp')
