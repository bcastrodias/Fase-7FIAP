import streamlit as st
import pandas as pd
import sqlite3
import os

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

# Inicializar automaticamente se o banco não existir
if not os.path.exists(DB_PATH):
    inicializar_banco()
    st.success("✅ Banco de dados criado automaticamente.")
else:
    if st.button("🛠️ Recriar Banco de Dados"):
        inicializar_banco()

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

with abas[2]:
    st.subheader("🧪 Sensor de pH")
    df_ph = carregar_tabela("Sensor_ph")
    st.dataframe(df_ph)

with abas[3]:
    st.subheader("🌱 Sensor de Nutrientes")
    df_nutrientes = carregar_tabela("Sensor_nutrientes")
    st.dataframe(df_nutrientes)
