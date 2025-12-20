import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================
st.set_page_config(page_title="Solar RN - Monitoramento e Previsão", page_icon="☀️", layout="wide")

# ============================================================================
# 1. CARREGAMENTO DE DADOS (API ANEEL - FILTRO RN)
# ============================================================================
@st.cache_data(ttl=3600)
def carregar_dados_rn():
    """Busca usinas do RN na API da ANEEL"""
    url = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"
    resource_id = "b1bd71e7-d0ad-4214-9053-cbd58e9564a7"
    
    # Filtro específico para o Rio Grande do Norte
    params = {
        "resource_id": resource_id,
        "filters": '{"SigUF": "RN"}',
        "limit": 3000  # Limite seguro para não travar a memória
    }

    try:
        response = requests.get(url, params=params)
        dados = response.json()
        
        if not dados.get('success'):
            return gerar_dados_simulados()

        df = pd.DataFrame(dados['result']['records'])
        
        # Tratamento e Limpeza
        df_final = pd.DataFrame()
        df_final['Nome'] = df.get('NomEmpreendimento', 'Usina Solar')
        df_final['Municipio'] = df.get('NomMunicipio', 'Desconhecido')
        df_final['Fonte'] = df.get('DscFonteGeracao', 'Solar')
        
        # Converter Potência (texto '30,5' para float 30.5)
        def limpar_float(x):
            try:
                return float(str(x).replace(',', '.'))
            except:
                return 0.0
                
        df_final['Potencia_kW'] = df.get('MdaPotenciaInstaladaKW', 0).apply(limpar_float)
        
        # Coordenadas (Latitude/Longitude)
        # Se a API não der coordenadas, estimamos algo no centro do RN para não quebrar o mapa
        if 'NumCoordNEmpreendimento' in df.columns:
            df_final['lat'] = df['NumCoordNEmpreendimento'].apply(limpar_float)
            df_final['lon'] = df['NumCoordEEmpreendimento'].apply(limpar_float)
            # Filtra coordenadas zeradas ou fora do Brasil
            df_final = df_final[(df_final['lat'] < 0) & (df_final['lon'] < -30)]
        else:
            # Fallback se a coluna não existir
            return gerar_dados_simulados()

        return df_final

    except Exception as e:
        st.warning(f"Usando dados offline devido a erro na API: {e}")
        return gerar_dados_simulados()

def gerar_dados_simulados():
    """Gera dados fakes de Natal/Mossoró caso a API falhe"""
    np.random.seed(84)
    n = 200
    return pd.DataFrame({
        'Nome': [f'Usina Solar RN {i}' for i in range(n)],
        'Municipio': np.random.choice(['Natal', 'Mossoró', 'Parnamirim', 'Caicó', 'Assu'], n),
        'Fonte': 'Radiação Solar',
        'Potencia_kW': np.random.uniform(5, 75, n),
        'lat': np.random.uniform(-6.2, -5.2, n),
        'lon': np.random.uniform(-37.3, -35.2, n)
    })

# ============================================================================
# 2. MODELO DE PREVISÃO (MACHINE LEARNING)
# ============================================================================
@st.cache_resource
def treinar_modelo():
    """Treina um modelo simples para prever geração baseada no clima"""
    # Criando dados históricos simulados (já que não temos histórico real agora)
    # Relação física: Geração = Irradiância * Eficiência - PerdaPorCalor
    n_amostras = 1000
    irradiancia = np.random.uniform(0, 1200, n_amostras) # W/m2
    temperatura = np.random.uniform(20, 40, n_amostras)  # Graus Celsius
    potencia_instalada = np.random.choice([10, 30, 50, 75], n_amostras) # kWp
    
    # Fórmula física simulada com ruído
    eficiencia = 0.15
    perda_calor = 0.004 # 0.4% por grau acima de 25C
    
    geracao_real = (irradiancia * eficiencia * potencia_instalada / 1000) * (1 - (temperatura - 25) * perda_calor)
    geracao_real = np.maximum(geracao_real, 0) # Não existe geração negativa
    
    df_treino = pd.DataFrame({
        'irradiancia': irradiancia,
        'temperatura': temperatura,
        'potencia_instalada': potencia_instalada,
        'geracao_kwh': geracao_real
    })
    
    X = df_treino[['irradiancia', 'temperatura', 'potencia_instalada']]
    y = df_treino['geracao_kwh']
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    return model

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================
def main():
    st.title("☀️ Monitoramento Solar - Rio Grande do Norte")
    
    # Carregar dados
    df_usinas = carregar_dados_rn()
    modelo = treinar_modelo()
    
    # Abas
    tab1, tab2 = st.tabs(["🗺️ Empreendimentos no RN", "🔮 Previsão de Geração"])
    
    # --- ABA 1: MAPA E DADOS ATUAIS ---
    with tab1:
        st.header("Usinas Conectadas")
        
        col1, col2, col3 = st.columns(3)
        total_kw = df_usinas['Potencia_kW'].sum()
        col1.metric("Total de Usinas (RN)", len(df_usinas))
        col2.metric("Potência Instalada Total", f"{total_kw/1000:.2f} MW")
        col3.metric("Cidade com Mais Usinas", df_usinas['Municipio'].mode()[0])
        
        # Mapa Simples (Plotly)
        fig_map = px.scatter_mapbox(
            df_usinas,
            lat="lat",
            lon="lon",
            color="Potencia_kW",
            size="Potencia_kW",
            hover_name="Municipio",
            hover_data=["Potencia_kW", "Nome"],
            zoom=6.5,
            center={"lat": -5.8, "lon": -36.5}, # Centro do RN
            mapbox_style="carto-positron",
            title="Distribuição Geográfica - Rio Grande do Norte",
            color_continuous_scale="Oranges"
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        with st.expander("Ver Tabela Detalhada"):
            st.dataframe(df_usinas, use_container_width=True)

    # --- ABA 2: SIMULADOR DE PREVISÃO ---
    with tab2:
        st.header("Estimativa de Geração (IA)")
        st.markdown("Simule quanto uma usina no RN geraria agora com base nas condições do tempo.")
        
        col_input, col_result = st.columns([1, 2])
        
        with col_input:
            st.subheader("Condições Atuais")
            potencia_user = st.selectbox("Tamanho da Usina (kWp)", [5, 10, 30, 50, 75, 100, 500])
            irr_user = st.slider("☀️ Irradiância Solar (W/m²)", 0, 1200, 800)
            temp_user = st.slider("🌡️ Temperatura Ambiente (°C)", 15, 45, 32)
            
            # Botão de previsão
            input_data = pd.DataFrame({
                'irradiancia': [irr_user],
                'temperatura': [temp_user],
                'potencia_instalada': [potencia_user]
            })
            predicao = modelo.predict(input_data)[0]
        
        with col_result:
            st.subheader("Resultado da Previsão")
            
            # Mostrador (Gauge)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = predicao,
                title = {'text': "Geração Estimada (kW)"},
                gauge = {
                    'axis': {'range': [0, potencia_user], 'tickwidth': 1},
                    'bar': {'color': "#FDB813"},
                    'steps': [
                        {'range': [0, potencia_user*0.3], 'color': "lightgray"},
                        {'range': [potencia_user*0.3, potencia_user*0.7], 'color': "gray"}
                    ],
                }
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.info(
                f"ℹ️ Uma usina de **{potencia_user} kWp** no Rio Grande do Norte, "
                f"com sol de **{irr_user} W/m²** e calor de **{temp_user}°C**, "
                f"estaria gerando aproximadamente **{predicao:.2f} kW** agora."
            )

if __name__ == "__main__":
    main()


