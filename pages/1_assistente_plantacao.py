import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assistente de Plantação", layout="centered")
st.title("🌱 Assistente Virtual de Plantação")

# Inicializa sessão
if "dados_cultivos" not in st.session_state:
    st.session_state.dados_cultivos = []

nomes_insumos = ['Nitrogênio', 'Fósforo', 'Potássio', 'Cálcio']

def nome_cultura(cultura):
    return "Soja" if cultura == "Soja" else "Cana-de-açúcar"

def calcular_fileiras_e_insumos(largura_campo, comprimento_fileira, espacamento, quantidade_por_metro):
    numero_fileiras = largura_campo / espacamento
    total_metros_pulverizar = numero_fileiras * comprimento_fileira
    quantidade_total_insumo = total_metros_pulverizar * quantidade_por_metro
    return numero_fileiras, quantidade_total_insumo

def estimar_tempo(cultura, ciclos):
    if cultura == "Soja":
        return ciclos * 4, ciclos * 6
    else:
        return ciclos * 12, ciclos * 18

# MENU DE BOTÕES
st.subheader("Selecione uma funcionalidade:")
opcao = st.radio("", [
    "➕ Inserir novo cultivo",
    "📋 Visualizar histórico",
    "📥 Exportar CSV"
])

if opcao == "➕ Inserir novo cultivo":
    with st.form("entrada_dados"):
        cultura = st.selectbox("Cultura:", ["Soja", "Cana-de-açúcar"])
        largura = st.number_input("Largura (m):", min_value=1.0)
        comprimento = st.number_input("Comprimento (m):", min_value=1.0)
        num_safras = st.number_input("Safras por ano:", min_value=1, max_value=5, step=1)

        nitro = st.checkbox("Nitrogênio")
        fosforo = st.checkbox("Fósforo")
        pota = st.checkbox("Potássio")
        cal = st.checkbox("Cálcio")

        enviar = st.form_submit_button("Calcular")

    if enviar:
        tamanho = largura * comprimento
        espacamento = 0.5 if cultura == "Soja" else 1.5
        quantidade_por_metro = 500
        numero_fileiras, quantidade_total_insumo = calcular_fileiras_e_insumos(
            largura, comprimento, espacamento, quantidade_por_metro)
        min_tempo, max_tempo = estimar_tempo(cultura, num_safras)

        doses = {
            "Soja": [5, 10, 10, 3],
            "Cana-de-açúcar": [10, 10, 20, 6]
        }
        dose = doses[cultura]
        total_insumos = [
            (tamanho * num_safras * dose[0]) / 1000 if nitro else 0,
            (tamanho * num_safras * dose[1]) / 1000 if fosforo else 0,
            (tamanho * num_safras * dose[2]) / 1000 if pota else 0,
            (tamanho * num_safras * dose[3]) / 1000 if cal else 0,
        ]

        dados = {
            "Cultura": cultura,
            "Largura (m)": largura,
            "Comprimento (m)": comprimento,
            "Área (m²)": tamanho,
            "Safras": num_safras,
            "Tempo mínimo (meses)": min_tempo,
            "Tempo máximo (meses)": max_tempo,
            "Nº fileiras": round(numero_fileiras),
            "Insumo total (L)": round(quantidade_total_insumo / 1000, 2),
            "Nitrogênio (kg)": total_insumos[0],
            "Fósforo (kg)": total_insumos[1],
            "Potássio (kg)": total_insumos[2],
            "Cálcio (kg)": total_insumos[3]
        }

        st.session_state.dados_cultivos.append(dados)
        st.success("✅ Dados adicionados com sucesso.")

elif opcao == "📋 Visualizar histórico":
    if not st.session_state.dados_cultivos:
        st.warning("Nenhum dado registrado.")
    else:
        df = pd.DataFrame(st.session_state.dados_cultivos)
        st.dataframe(df)

elif opcao == "📥 Exportar CSV":
    if not st.session_state.dados_cultivos:
        st.warning("Nenhum dado disponível.")
    else:
        df = pd.DataFrame(st.session_state.dados_cultivos)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", csv, file_name="dados_cultivos.csv", mime="text/csv")
