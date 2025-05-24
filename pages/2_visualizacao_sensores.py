import streamlit as st
import pandas as pd
import sqlite3
import os
import numpy as np
from datetime import datetime, timedelta
import boto3


sns = boto3.client("sns", region_name="us-east-2")  # ajuste a região
TOPIC_ARN = "arn:aws:sns:us-east-2:077227809508:Fase7Cap1-FIAP" 

st.set_page_config(page_title="Visualização de Sensores", layout="wide")
st.title("📊 Dados dos Sensores e Zonas de Plantação")

DB_PATH = "dados_farmtech.db"

# Função para inicializar o banco com a estrutura definida
def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS Sensor_ph;
    DROP TABLE IF EXISTS Sensor_nutrientes;
    DROP TABLE IF EXISTS Sensor_umidade;
    DROP TABLE IF EXISTS Zona_plantacao;

    CREATE TABLE Zona_plantacao (
        id_zona_plantacao INTEGER PRIMARY KEY,
        nome_zona VARCHAR,
        descricao MEDIUMTEXT
    );

    CREATE TABLE Sensor_ph (
        id_sensor_ph INTEGER PRIMARY KEY,
        valor_ph FLOAT,
        data_hora DATETIME,
        id_zona_plantacao INTEGER,
        FOREIGN KEY(id_zona_plantacao) REFERENCES Zona_plantacao(id_zona_plantacao)
    );

    CREATE TABLE Sensor_umidade (
        id_sensor_umidade INTEGER PRIMARY KEY,
        valor_umidade DOUBLE,
        data_hora DATETIME,
        id_zona_plantacao INTEGER,
        FOREIGN KEY(id_zona_plantacao) REFERENCES Zona_plantacao(id_zona_plantacao)
    );

    CREATE TABLE Sensor_nutrientes (
        id_sensor_nutrientes INTEGER PRIMARY KEY,
        valor_potassio DOUBLE,
        valor_fosforo DOUBLE,
        data_hora DATETIME,
        id_zona_plantacao INTEGER,
        FOREIGN KEY(id_zona_plantacao) REFERENCES Zona_plantacao(id_zona_plantacao)
    );
    """)
    conn.commit()
    conn.close()
    st.success("✅ Banco de dados inicializado com sucesso!")

def popular_dados_aleatorios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Inserir zonas
    zonas = [
        ("Zona Norte", "Área com maior incidência solar."),
        ("Zona Sul", "Área mais sombreada."),
        ("Zona Central", "Área de irrigação intensiva."),
    ]
    cursor.executemany("INSERT INTO Zona_plantacao (nome_zona, descricao) VALUES (?, ?);", zonas)
    conn.commit()

    # Pegar os IDs gerados
    cursor.execute("SELECT id_zona_plantacao FROM Zona_plantacao;")
    zona_ids = [row[0] for row in cursor.fetchall()]

    # Inserir dados nos sensores
    for _ in range(20):
        data_aleatoria = datetime.now() - timedelta(days=np.random.randint(0, 30))

        # Umidade
        cursor.execute("""
            INSERT INTO Sensor_umidade (valor_umidade, data_hora, id_zona_plantacao)
            VALUES (?, ?, ?)
        """, (round(np.random.uniform(30, 90), 2), data_aleatoria, np.random.choice(zona_ids)))

        # pH
        cursor.execute("""
            INSERT INTO Sensor_ph (valor_ph, data_hora, id_zona_plantacao)
            VALUES (?, ?, ?)
        """, (round(np.random.uniform(5.0, 7.5), 2), data_aleatoria, np.random.choice(zona_ids)))

        # Nutrientes
        cursor.execute("""
            INSERT INTO Sensor_nutrientes (valor_potassio, valor_fosforo, data_hora, id_zona_plantacao)
            VALUES (?, ?, ?, ?)
        """, (
            round(np.random.uniform(50, 200), 1),
            round(np.random.uniform(20, 80), 1),
            data_aleatoria,
            np.random.choice(zona_ids)
        ))

    conn.commit()
    conn.close()
    st.success("✅ Tabelas populadas com dados aleatórios!")
    st.rerun()

# Inicializar automaticamente se o banco não existir
if not os.path.exists(DB_PATH):
    inicializar_banco()
    st.success("✅ Banco de dados criado automaticamente.")
else:
    if st.button("🛠️ Recriar Banco de Dados"):
        inicializar_banco()
    if st.button("📥 Popular com dados aleatórios"):
        popular_dados_aleatorios()
# Função para carregar e exibir uma tabela
@st.cache_data
def carregar_tabela(nome_tabela):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(f"SELECT * FROM {nome_tabela}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar {nome_tabela}: {e}")
        return pd.DataFrame()

# Alerta para enunciar umidade crítica   
def enviar_alerta_umidade(sensor_id):
    mensagem = f"Umidade crítica no sensor {sensor_id}"
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=mensagem,
        Subject="⚠️ Alerta de Umidade Crítica"
    )


# Abas para visualizar cada tabela
abas = st.tabs([
    "🌾 Zonas de Plantação",
    "💧 Sensor de Umidade",
    "🧪 Sensor de pH",
    "🌱 Sensor de Nutrientes"
])

with abas[0]:
    st.subheader("🌾 Zonas de Plantação")
    df_zonas = carregar_tabela("Zona_plantacao")
    st.dataframe(df_zonas)

with abas[1]:
    st.subheader("💧 Sensor de Umidade")
    df_umidade = carregar_tabela("Sensor_umidade")
    st.dataframe(df_umidade)

    df_critico = df_umidade[df_umidade["valor_umidade"] < 50]

    for _, row in df_critico.iterrows():
        enviar_alerta_umidade(row["id_sensor_umidade"])

with abas[2]:
    st.subheader("🧪 Sensor de pH")
    df_ph = carregar_tabela("Sensor_ph")
    st.dataframe(df_ph)

with abas[3]:
    st.subheader("🌱 Sensor de Nutrientes")
    df_nutrientes = carregar_tabela("Sensor_nutrientes")
    st.dataframe(df_nutrientes)
