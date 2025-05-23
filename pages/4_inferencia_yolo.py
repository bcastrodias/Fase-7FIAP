import streamlit as st
from PIL import Image
from ultralytics import YOLO
import tempfile
from pathlib import Path

st.set_page_config(page_title="YOLO - Inferência", layout="centered")
st.title("🔍 Inferência com YOLOv8 - Detecção de Objetos")

# Caminho seguro para o modelo YOLOv8 treinado
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "model_60epochs.pt"

# Carregar o modelo
@st.cache_resource
def carregar_modelo(path):
    try:
        model = YOLO(str(path))
        return model
    except Exception as e:
        st.error(f"❌ Erro ao carregar o modelo: {e}")
        return None

modelo = carregar_modelo(MODEL_PATH)

# Upload da imagem
uploaded_file = st.file_uploader("Envie uma imagem para detectar objetos", type=["jpg", "jpeg", "png"])

if uploaded_file and modelo:
    imagem = Image.open(uploaded_file)
    st.image(imagem, caption="Imagem enviada", use_column_width=True)

    if st.button("🚀 Detectar objetos"):
        with st.spinner("Detectando..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                imagem.save(temp_file.name)
                caminho_temporario = temp_file.name

            resultados = modelo.predict(source=caminho_temporario, conf=0.25)

            imagem_resultado = resultados[0].plot()
            st.image(imagem_resultado, caption="Resultado da detecção", use_column_width=True)

            st.markdown("### 📌 Objetos Detectados:")
            for box in resultados[0].boxes:
                classe = modelo.names[int(box.cls[0])]
                conf = float(box.conf[0])
                st.write(f"- {classe}: {conf:.2%} de confiança")
