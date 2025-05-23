import streamlit as st

st.set_page_config(page_title="Dashboard Principal", layout="centered")
st.title("🚜 Dashboard de Projetos Agrícolas")

st.markdown("Selecione um dos projetos para acessar:")

col1, col2 = st.columns(2)

with col1:
    if st.button("1️⃣ Assistente de Plantação"):
        st.switch_page("pages/1_assistente_plantacao.py")

    if st.button("3️⃣ Visão Computacional"):
        st.switch_page("pages/4_inferencia_yolo.py")
   

with col2:
    if st.button("2️⃣ Visualização Sensores"):
        st.switch_page("pages/2_visualizacao_sensores.py")

    if st.button("4️⃣ Código IoT"):
        st.switch_page("pages/3_codigo_iot.py")

    
