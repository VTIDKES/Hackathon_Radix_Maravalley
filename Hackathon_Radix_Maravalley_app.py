import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

st.set_page_config(page_title="Hackathon Energia • VTS", layout="wide")

# ======================================================
#  MENU LATERAL
# ======================================================
st.sidebar.title("⚡ Hackathon — Soluções para Energia")
menu = st.sidebar.selectbox(
    "Selecione uma solução:",
    [
        "📉 Monitoramento de Perdas e Fraudes",
        "🔆 Previsão de Geração Solar",
        "🏭 Digital Twin de Subestação / Solar"
    ]
)

# ======================================================
# 1. PERDAS E FRAUDES
# ======================================================
if menu == "📉 Monitoramento de Perdas e Fraudes":
    st.title("📉 Monitoramento Inteligente de Perdas e Fraudes (Furto de Energia)")
    st.write("Simulação simples de um modelo de detecção de anomalias de consumo.")

    # Dados fictícios
    st.subheader("🔢 Dados do Cliente")
    consumo = st.number_input("Consumo mensal (kWh)", 0, 5000, 320)
    variacao = st.number_input("Variação mensal (%)", 0, 200, 12)
    fator_noite = st.number_input("Fator de consumo noturno (%)", 0, 100, 50)
    
    if st.button("Analisar"):
        # Simulação de modelo
        score = (variacao * 0.4) + (100 - fator_noite) * 0.3 + (500 - abs(consumo - 350)) * 0.2
        score = max(0, min(score / 10, 100))

        st.metric("Probabilidade de fraude", f"{score:.1f}%")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            gauge={'axis': {'range': [0, 100]}},
            title={'text': "Risco"}
        ))
        st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 2. PREVISÃO DE GERAÇÃO SOLAR
# ======================================================
elif menu == "🔆 Previsão de Geração Solar":
    st.title("🔆 Previsão Inteligente de Geração Solar")
    st.write("Modelo simples baseado em regressão linear.")

    irradiancia = st.slider("Irradiância (W/m²)", 0, 1200, 800)
    temperatura = st.slider("Temperatura do módulo (°C)", -10, 80, 35)

    # Modelo fictício simples
    power = (irradiancia * 0.75) - (temperatura * 0.5)

    if power < 0:
        power = 0

    st.metric("Geração estimada (kW)", f"{power:.2f}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Geração"],
        y=[power]
    ))
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 3. DIGITAL TWIN
# ======================================================
elif menu == "🏭 Digital Twin de Subestação / Solar":
    st.title("🏭 Digital Twin Simplificado")

    st.write("""
    Este Digital Twin simula valores básicos de operação de uma subestação ou usina solar.
    """)

    tensao = st.slider("Tensão (kV)", 10, 500, 69)
    corrente = st.slider("Corrente (A)", 0, 3000, 450)
    temperatura = st.slider("Temperatura (°C)", -10, 120, 45)

    potencia = (tensao * 1000 * corrente) / (np.sqrt(3) * 1000)

    st.metric("Potência Aparente (MVA)", f"{potencia/1e6:.3f}")

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=temperatura,
        title={"text": "Temperatura"},
        gauge={"axis": {"range": [-10, 120]}}
    ))    
    st.plotly_chart(fig, use_container_width=True)

