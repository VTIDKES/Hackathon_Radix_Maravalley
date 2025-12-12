# Hackathon_Radix_Maravalley_app_no_sklearn.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Hackathon Energia • VTS (sem sklearn)", layout="wide")

st.sidebar.title("⚡ Hackathon — Soluções para Energia")
menu = st.sidebar.selectbox(
    "Selecione uma solução:",
    [
        "📉 Monitoramento de Perdas e Fraudes",
        "🔆 Previsão de Geração Solar",
        "🏭 Digital Twin de Subestação / Solar"
    ]
)

# Simples detector de anomalias baseado em z-score (sem sklearn)
def simple_anomaly_score(value, window_mean, window_std):
    if window_std == 0:
        return 0.0
    return abs((value - window_mean) / window_std)

if menu == "📉 Monitoramento de Perdas e Fraudes":
    st.title("📉 Monitoramento Inteligente de Perdas e Fraudes (Sem sklearn)")
    st.write("Exemplo sem dependência de scikit-learn. Upload CSV com colunas: id,timestamp,consumption")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        # assumimos coluna 'consumption'
        if 'consumption' not in df.columns:
            st.error("CSV precisa ter coluna 'consumption'")
        else:
            # calcula z-score simples por janela
            df['mean7'] = df['consumption'].rolling(7, min_periods=1).mean()
            df['std7'] = df['consumption'].rolling(7, min_periods=1).std().fillna(0)
            df['anom_score'] = df.apply(lambda r: simple_anomaly_score(r['consumption'], r['mean7'], r['std7']), axis=1)
            # marca como anomalia se score > threshold (ex: 3)
            threshold = st.slider("Threshold z-score para considerar anomalia", 1.5, 6.0, 3.0)
            df['is_anomaly'] = df['anom_score'] > threshold
            st.metric("Total de anomalias", int(df['is_anomaly'].sum()))
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=df['consumption'], mode='lines', name='consumption'))
            fig.add_trace(go.Scatter(y=df.loc[df['is_anomaly'],'consumption'], mode='markers', name='anomaly'))
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("Baixar resultados CSV", df.to_csv(index=False).encode('utf-8'), file_name='anomaly_results.csv')

elif menu == "🔆 Previsão de Geração Solar":
    st.title("🔆 Previsão de Geração Solar (Regressão simples)")
    irradiancia = st.slider("Irradiância (W/m²)", 0, 1200, 800)
    temperatura = st.slider("Temperatura (°C)", -10, 80, 35)
    # regressão linear analítica (sem sklearn): potência = a*irr + b*temp + c
    # usamos parâmetros fictícios
    a = 0.2
    b = -0.3
    c = 50
    power = a * irradiancia + b * temperatura + c
    power = max(power, 0)
    st.metric("Geração estimada (kW)", f"{power:.2f}")
    fig = go.Figure(go.Bar(x=["Geração"], y=[power]))
    st.plotly_chart(fig, use_container_width=True)

elif menu == "🏭 Digital Twin de Subestação / Solar":
    st.title("🏭 Digital Twin Simplificado (sem sklearn)")
    tensao = st.slider("Tensão (kV)", 10, 500, 69)
    corrente = st.slider("Corrente (A)", 0, 3000, 450)
    temperatura = st.slider("Temperatura (°C)", -10, 120, 45)
    potencia = (tensao * 1000 * corrente) / (np.sqrt(3) * 1000)
    st.metric("Potência Aparente (MVA)", f"{potencia/1e6:.3f}")
    fig = go.Figure()
    fig.add_trace(go.Indicator(mode="number+gauge", value=temperatura, title={"text":"Temperatura"}, gauge={"axis":{"range":[-10,120]}}))
    st.plotly_chart(fig, use_container_width=True)


