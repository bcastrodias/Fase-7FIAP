import streamlit as st
import boto3

# SQS setup
sqs = boto3.client("sqs", region_name="us-east-2")
QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/077227809508/FilaFase7Cap1-FIAP"

def verificar_mensagens():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1
    )

    if "Messages" in response:
        for msg in response["Messages"]:
            st.toast(f"🔔 Notificação: {msg['Body']}")
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

st.set_page_config(page_title="Dashboard Principal", layout="centered")
st.title("🚜 Dashboard de Projetos Agrícolas")

st.markdown("Selecione um dos projetos para acessar:")

if st.button("🔄 Verificar notificações"):
    verificar_mensagens()

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
