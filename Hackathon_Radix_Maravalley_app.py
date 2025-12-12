import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Hackathon Energia • VTS", layout="wide")

st.sidebar.title("⚡ Hackathon — Soluções para Energia")
menu = st.sidebar.selectbox(
    "Selecione uma solução:",
    [
        "📉 Monitoramento de Perdas e Fraudes",
        "🔆 Previsão de Geração Solar",
        "🏭 Digital Twin de Subestação / Solar"
    ]
)

# ============================================================
# 1) MONITORAMENTO DE FRAUDES (SEM SKLEARN)
# ============================================================
if menu == "📉 Monitoramento de Perdas e Fraudes":
    st.title("📉 Monitoramento Inteligente de Perdas e Fraudes (Sem sklearn)")
    st.write("Detecção simplificada baseada em Z-Score.")

    file = st.file_uploader("Upload CSV com a coluna 'consumption'", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write("Pré-visualização dos dados:")
        st.dataframe(df.head())

        if "consumption" not in df.columns:
            st.error("O CSV precisa da coluna 'consumption'.")
            st.stop()

        df["mean"] = df["consumption"].rolling(10, min_periods=1).mean()
        df["std"] = df["consumption"].rolling(10, min_periods=1).std().fillna(0)
        df["z_score"] = (df["consumption"] - df["mean"]) / df["std"].replace(0, 1)

        threshold = st.slider("Sensibilidade (Z-score)", 1.5, 5.0, 3.0)
        df["anomaly"] = df["z_score"].abs() > threshold

        st.metric("Total de possíveis fraudes:", int(df["anomaly"].sum()))

        st.subheader("📉 Gráfico de Consumo")
        st.line_chart(df["consumption"])

        st.subheader("🔴 Pontos suspeitos")
        st.write(df[df["anomaly"]])

        st.download_button(
            "Baixar relatório",
            df.to_csv(index=False).encode("utf-8"),
            file_name="fraudes_detectadas.csv"
        )

# ============================================================
# 2) PREVISÃO DE GERAÇÃO SOLAR (SEM SKLEARN)
# ============================================================
elif menu == "🔆 Previsão de Geração Solar":
    st.title("🔆 Previsão Simples de Geração Solar")
    st.write("Modelo linear simples sem dependências externas.")

    irr = st.slider("Irradiância (W/m²)", 0, 1200, 800)
    temp = st.slider("Temperatura (°C)", -10, 80, 35)

    # modelo manual
    power = irr * 0.18 - temp * 0.3
    if power < 0:
        power = 0

    st.metric("Geração Estimada (kW)", f"{power:.2f}")

    st.bar_chart(pd.DataFrame({"Potência (kW)": [power]}))

# ============================================================
# 3) DIGITAL TWIN (SEM PLOTLY)
# ============================================================
elif menu == "🏭 Digital Twin de Subestação / Solar":
    st.title("🏭 Digital Twin Simplificado (Sem Plotly)")

    tensao = st.slider("Tensão (kV)", 10, 500, 69)
    corrente = st.slider("Corrente (A)", 0, 3000, 450)
    temperatura = st.slider("Temperatura (°C)", -10, 120, 45)

    potencia_mva = (tensao * corrente * 1000) / (np.sqrt(3) * 1e6)

    st.metric("Potência Aparente (MVA)", f"{potencia_mva:.3f}")

    st.subheader("Temperatura do Sistema")
    st.line_chart(pd.DataFrame({"Temperatura": [temperatura]}))

    st.write("Simulação simples e compatível com ambientes restritos.")



