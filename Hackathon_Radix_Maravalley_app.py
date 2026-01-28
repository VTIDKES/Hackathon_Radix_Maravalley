"""
CPFL LABS | TEMA 3
Smart Meter Insights Platform com Mapa Interativo do RN
Localização: Natal, Parnamirim e Rio Grande do Norte
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="CPFL LABS | TEMA 3",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Estilo CPFL Profissional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header principal com gradiente CPFL */
    .main-header {
        background: linear-gradient(135deg, #003D5C 0%, #00668C 50%, #0099CC 100%);
        color: white;
        padding: 2rem 2.5rem;
        margin: -1rem -1rem 2.5rem -1rem;
        border-bottom: 4px solid #00A9CE;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.95;
        font-weight: 400;
    }
    
    .main-header .location {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Sidebar profissional */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FAFB 0%, #F0F4F7 100%);
        border-right: 2px solid #D5DDE5;
    }
    
    /* Métricas profissionais */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #003D5C;
        letter-spacing: -0.5px;
    }
    
    /* Cards de seção */
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 5px solid #00A9CE;
        transition: all 0.3s;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #003D5C;
        margin-bottom: 1.2rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 24px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.3rem 0.2rem;
    }
    
    .badge-normal { 
        background: linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%);
        color: #2E7D32;
    }
    
    .badge-alerta { 
        background: linear-gradient(135deg, #FFE082 0%, #FFD54F 100%);
        color: #F57C00;
    }
    
    .badge-critico { 
        background: linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%);
        color: #C62828;
    }
</style>
""", unsafe_allow_html=True)

# Coordenadas reais de Natal e Parnamirim, RN
LOCATIONS = {
    'Natal - Ponta Negra': {'lat': -5.8836, 'lon': -35.1732, 'alimentador': 'AL-NAT-04'},
    'Natal - Capim Macio': {'lat': -5.8479, 'lon': -35.2008, 'alimentador': 'AL-NAT-07'},
    'Natal - Candelária': {'lat': -5.8024, 'lon': -35.2137, 'alimentador': 'AL-NAT-04'},
    'Natal - Lagoa Nova': {'lat': -5.8324, 'lon': -35.2050, 'alimentador': 'AL-NAT-07'},
    'Parnamirim - Centro': {'lat': -5.9154, 'lon': -35.2628, 'alimentador': 'AL-PAR-02'},
    'Parnamirim - Nova Parnamirim': {'lat': -5.9058, 'lon': -35.2754, 'alimentador': 'AL-PAR-05'},
    'Parnamirim - Cotovelo': {'lat': -5.9842, 'lon': -35.1891, 'alimentador': 'AL-PAR-02'},
    'São Gonçalo do Amarante': {'lat': -5.7931, 'lon': -35.3264, 'alimentador': 'AL-PAR-05'},
}

@st.cache_data
def generate_smart_meter_data_with_location(num_meters=50, days=7):
    """Gera dados com coordenadas geográficas reais"""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='15min')
    
    data = []
    locations_list = list(LOCATIONS.keys())
    
    for meter_id in range(1, num_meters + 1):
        # Atribuir localização
        location_name = np.random.choice(locations_list)
        location_data = LOCATIONS[location_name]
        
        # Adicionar pequena variação nas coordenadas (simulando medidores próximos)
        lat_variation = np.random.uniform(-0.01, 0.01)
        lon_variation = np.random.uniform(-0.01, 0.01)
        
        id_medidor = f"RN-{39200 + meter_id:05d}"
        consumo_base = np.random.uniform(2.0, 4.5)
        
        for ts in timestamps:
            hora = ts.hour
            
            # Padrão de consumo RN (calor)
            if 12 <= hora <= 15:
                fator = 3.2
            elif 18 <= hora <= 22:
                fator = 2.8
            elif 6 <= hora <= 8:
                fator = 1.8
            elif 0 <= hora <= 5:
                fator = 0.5
            else:
                fator = 1.2
            
            potencia = consumo_base * fator * np.random.uniform(0.88, 1.12)
            
            # Anomalias
            if np.random.random() < 0.015:
                potencia = potencia * 4.5 if np.random.random() < 0.5 else 0.02
            
            tensao = 127 + np.random.normal(0, 2.5)
            if np.random.random() < 0.012 and 12 <= hora <= 15:
                tensao = np.random.uniform(108, 117)
            
            fator_pot = np.random.uniform(0.87, 0.97)
            if np.random.random() < 0.025:
                fator_pot = np.random.uniform(0.62, 0.75)
            
            data.append({
                'id_medidor': id_medidor,
                'timestamp': ts,
                'tensao_v': tensao,
                'potencia_kw': potencia,
                'fator_potencia': fator_pot,
                'energia_kwh': potencia * 0.25,
                'alimentador': location_data['alimentador'],
                'regiao': location_name,
                'lat': location_data['lat'] + lat_variation,
                'lon': location_data['lon'] + lon_variation,
                'hora': hora,
            })
    
    return pd.DataFrame(data)

@st.cache_data
def detect_events_with_location(df):
    """Detecção de eventos com localização"""
    events = []
    event_id = 1
    
    for _, row in df.iterrows():
        if row['tensao_v'] < 117:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'lat': row['lat'],
                'lon': row['lon'],
                'tipo': 'SUBTENSÃO',
                'severidade': 'CRÍTICA' if row['tensao_v'] < 110 else 'ALTA',
                'valor': f"{row['tensao_v']:.1f}V",
                'descricao': f"Tensão {row['tensao_v']:.1f}V abaixo do adequado",
                'destino': 'Operação',
            })
            event_id += 1
        
        if row['potencia_kw'] < 0.08:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'lat': row['lat'],
                'lon': row['lon'],
                'tipo': 'INTERRUPÇÃO',
                'severidade': 'CRÍTICA',
                'valor': f"{row['potencia_kw']:.3f}kW",
                'descricao': 'Possível interrupção',
                'destino': 'Operação',
            })
            event_id += 1
    
    return pd.DataFrame(events) if events else pd.DataFrame()

# Header
st.markdown("""
<div class="main-header">
    <h1>🔷 CPFL LABS | TEMA 3</h1>
    <p>Smart Meter Insights Platform - Sistema Avançado de Análise e Gestão de Dados</p>
    <span class="location">📍 Natal, Parnamirim e Rio Grande do Norte</span>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### MÓDULOS DO PIPELINE")
    
    page = st.radio(
        "",
        [
            "🗺️ Mapa Interativo RN",
            "📊 Visão Operacional",
            "⚡ Motor de Eventos"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### CONFIGURAÇÕES")
    
    num_meters = st.slider("📡 Medidores", 20, 100, 50, 10)
    num_days = st.slider("📅 Dias", 1, 30, 7)
    
    if st.button("🔄 ATUALIZAR"):
        st.cache_data.clear()
        st.rerun()

# Carregar dados
with st.spinner("⚙️ Carregando dados georreferenciados..."):
    df = generate_smart_meter_data_with_location(num_meters, num_days)
    events_df = detect_events_with_location(df)

# PÁGINA: Mapa Interativo
if page == "🗺️ Mapa Interativo RN":
    st.markdown('<div class="section-title">🗺️ Mapa Geográfico Interativo - Rio Grande do Norte</div>', unsafe_allow_html=True)
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    eventos_criticos = len(events_df[events_df['severidade'] == 'CRÍTICA']) if not events_df.empty else 0
    
    col1.metric("Medidores Ativos", num_meters)
    col2.metric("Regiões Cobertas", df['regiao'].nunique())
    col3.metric("Eventos no Mapa", len(events_df) if not events_df.empty else 0)
    col4.metric("Alertas Críticos", eventos_criticos)
    
    st.markdown("---")
    
    # Mapa principal com Plotly (estilo profissional)
    # Dados dos medidores (últimas leituras)
    latest_readings = df.groupby('id_medidor').last().reset_index()
    
    # Classificar status
    def classify_status(row):
        if row['tensao_v'] < 117 or row['potencia_kw'] < 0.1:
            return 'Crítico'
        elif row['tensao_v'] < 120 or row['fator_potencia'] < 0.75:
            return 'Alerta'
        else:
            return 'Normal'
    
    latest_readings['status'] = latest_readings.apply(classify_status, axis=1)
    
    # Criar mapa com scatter_mapbox (Plotly)
    fig = go.Figure()
    
    # Adicionar medidores normais
    normal = latest_readings[latest_readings['status'] == 'Normal']
    if not normal.empty:
        fig.add_trace(go.Scattermapbox(
            lat=normal['lat'],
            lon=normal['lon'],
            mode='markers',
            marker=dict(size=12, color='#4CAF50', opacity=0.7),
            text=normal.apply(lambda r: f"<b>{r['id_medidor']}</b><br>{r['regiao']}<br>Tensão: {r['tensao_v']:.1f}V<br>Potência: {r['potencia_kw']:.2f}kW", axis=1),
            hoverinfo='text',
            name='Normal'
        ))
    
    # Adicionar medidores com alerta
    alerta = latest_readings[latest_readings['status'] == 'Alerta']
    if not alerta.empty:
        fig.add_trace(go.Scattermapbox(
            lat=alerta['lat'],
            lon=alerta['lon'],
            mode='markers',
            marker=dict(size=14, color='#FF9800', opacity=0.8),
            text=alerta.apply(lambda r: f"<b>{r['id_medidor']}</b><br>{r['regiao']}<br>⚠️ ALERTA<br>Tensão: {r['tensao_v']:.1f}V<br>Potência: {r['potencia_kw']:.2f}kW", axis=1),
            hoverinfo='text',
            name='Alerta'
        ))
    
    # Adicionar medidores críticos
    critico = latest_readings[latest_readings['status'] == 'Crítico']
    if not critico.empty:
        fig.add_trace(go.Scattermapbox(
            lat=critico['lat'],
            lon=critico['lon'],
            mode='markers',
            marker=dict(size=18, color='#F44336', opacity=0.9, symbol='circle'),
            text=critico.apply(lambda r: f"<b>{r['id_medidor']}</b><br>{r['regiao']}<br>🚨 CRÍTICO<br>Tensão: {r['tensao_v']:.1f}V<br>Potência: {r['potencia_kw']:.2f}kW", axis=1),
            hoverinfo='text',
            name='Crítico'
        ))
    
    # Configurar mapa
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=-5.85, lon=-35.22),  # Centro em Natal
            zoom=10
        ),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#003D5C",
            borderwidth=2
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legenda e informações
    st.markdown("""
    <div class="section-card">
    <h4>📍 Legenda do Mapa</h4>
    <div style='display: flex; gap: 2rem; margin-top: 1rem;'>
        <div><span style='color: #4CAF50; font-size: 1.5rem;'>●</span> <strong>Normal</strong> - Sistema operando adequadamente</div>
        <div><span style='color: #FF9800; font-size: 1.5rem;'>●</span> <strong>Alerta</strong> - Atenção necessária</div>
        <div><span style='color: #F44336; font-size: 1.5rem;'>●</span> <strong>Crítico</strong> - Ação imediata requerida</div>
    </div>
    <p style='margin-top: 1rem; color: #546E7A; font-size: 0.9rem;'>
    <strong>Dica:</strong> Clique nos marcadores para ver detalhes do medidor. Use os controles do mapa para zoom e navegação.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas por região
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Estatísticas por Região</div>', unsafe_allow_html=True)
    
    region_stats = latest_readings.groupby('regiao').agg({
        'id_medidor': 'count',
        'tensao_v': 'mean',
        'potencia_kw': 'mean',
        'status': lambda x: (x == 'Crítico').sum()
    }).reset_index()
    
    region_stats.columns = ['Região', 'Medidores', 'Tensão Média (V)', 'Potência Média (kW)', 'Críticos']
    
    st.dataframe(region_stats, use_container_width=True, hide_index=True)

# PÁGINA: Visão Operacional
elif page == "📊 Visão Operacional":
    st.markdown('<div class="section-title">📊 Visão Operacional da Rede</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    tensao_media = df['tensao_v'].mean()
    eventos_criticos = len(events_df[events_df['severidade'] == 'CRÍTICA']) if not events_df.empty else 0
    carga_total = df['potencia_kw'].sum() / 1000
    
    col1.metric("Tensão Média", f"{tensao_media:.1f} V")
    col2.metric("Eventos Críticos", eventos_criticos)
    col3.metric("Carga Total", f"{carga_total:.2f} MW")
    col4.metric("Alimentadores", df['alimentador'].nunique())
    
    st.markdown("---")
    
    # Gráfico de consumo por região
    region_consumption = df.groupby('regiao')['energia_kwh'].sum().reset_index()
    region_consumption = region_consumption.sort_values('energia_kwh', ascending=False)
    
    fig = px.bar(region_consumption, x='regiao', y='energia_kwh',
                 title='Consumo Energético por Região',
                 labels={'energia_kwh': 'Energia (kWh)', 'regiao': 'Região'},
                 color='energia_kwh',
                 color_continuous_scale='Blues')
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# PÁGINA: Motor de Eventos
else:
    st.markdown('<div class="section-title">⚡ Motor de Eventos</div>', unsafe_allow_html=True)
    
    if not events_df.empty:
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Total Eventos", len(events_df))
        col2.metric("Críticos", len(events_df[events_df['severidade']=='CRÍTICA']))
        col3.metric("Altos", len(events_df[events_df['severidade']=='ALTA']))
        
        st.markdown("---")
        
        # Tabela de eventos
        st.dataframe(
            events_df[['id_evento', 'id_medidor', 'regiao', 'tipo', 'severidade', 'valor', 'descricao']],
            use_container_width=True,
            height=400
        )
    else:
        st.success("✅ Nenhum evento detectado")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 1rem; background: #F5F7FA; border-radius: 10px;'>
<strong>🔷 CPFL LABS</strong> | P&D ANEEL Tema 3 | 
Localização: Natal, Parnamirim e RN | 
Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
</div>
""", unsafe_allow_html=True)
