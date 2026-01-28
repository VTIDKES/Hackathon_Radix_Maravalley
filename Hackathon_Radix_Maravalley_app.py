"""
CPFL LABS | TEMA 3
Smart Meter Insights Platform (Python Prototype)
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
    
    [data-testid="stSidebar"] h3 {
        color: #003D5C;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00A9CE;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 600;
        color: #2C5F7A;
        font-size: 0.95rem;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.2s;
        background: transparent;
        margin: 0.2rem 0;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(0,169,206,0.08);
        transform: translateX(3px);
    }
    
    /* Métricas profissionais */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #003D5C;
        letter-spacing: -0.5px;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 600;
        color: #546E7A;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Cards de seção com sombra */
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 5px solid #00A9CE;
        transition: all 0.3s;
    }
    
    .section-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #003D5C;
        margin-bottom: 1.2rem;
        letter-spacing: -0.3px;
    }
    
    .section-subtitle {
        font-size: 0.95rem;
        color: #546E7A;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Status badges profissionais */
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
        box-shadow: 0 2px 4px rgba(46,125,50,0.2);
    }
    
    .badge-alerta { 
        background: linear-gradient(135deg, #FFE082 0%, #FFD54F 100%);
        color: #F57C00;
        box-shadow: 0 2px 4px rgba(245,124,0,0.2);
    }
    
    .badge-critico { 
        background: linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%);
        color: #C62828;
        box-shadow: 0 2px 4px rgba(198,40,40,0.2);
    }
    
    .badge-media {
        background: linear-gradient(135deg, #BBDEFB 0%, #90CAF9 100%);
        color: #1565C0;
        box-shadow: 0 2px 4px rgba(21,101,192,0.2);
    }
    
    /* Botões premium */
    .stButton > button {
        background: linear-gradient(135deg, #00A9CE 0%, #0088AA 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2.5rem;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,169,206,0.3);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0088AA 0%, #006688 100%);
        box-shadow: 0 6px 20px rgba(0,169,206,0.4);
        transform: translateY(-2px);
    }
    
    /* Info box premium */
    .info-box {
        background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%);
        border-left: 5px solid #00A9CE;
        padding: 1.3rem;
        margin: 1.2rem 0;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,169,206,0.1);
    }
    
    .info-box strong {
        color: #003D5C;
        font-weight: 700;
    }
    
    /* Terminal profissional */
    .terminal-output {
        background: linear-gradient(135deg, #1A1A1D 0%, #2D2D30 100%);
        color: #E0E0E0;
        font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        padding: 1.5rem;
        border-radius: 10px;
        font-size: 0.85rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        border: 1px solid #3D3D40;
        line-height: 1.6;
    }
    
    .terminal-output .info {
        color: #4FC3F7;
    }
    
    .terminal-output .success {
        color: #81C784;
    }
    
    .terminal-output .warning {
        color: #FFB74D;
    }
    
    /* Tabela profissional */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Status footer premium */
    .status-footer {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8EDF2 100%);
        padding: 1.2rem 2rem;
        margin-top: 3rem;
        border-top: 3px solid #00A9CE;
        font-size: 0.85rem;
        color: #546E7A;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
    }
    
    .status-footer strong {
        color: #003D5C;
        font-weight: 700;
    }
    
    /* Indicadores de status */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    
    .status-online { background: #4CAF50; }
    .status-warning { background: #FF9800; }
    .status-offline { background: #F44336; }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Divisores elegantes */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00A9CE 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Tabs profissionais */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F5F7FA;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        background: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00A9CE 0%, #0088AA 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Funções de geração de dados - NATAL/PARNAMIRIM/RN
@st.cache_data
def generate_smart_meter_data(num_meters=50, days=7):
    """Gera dados sintéticos de smart meters para região Natal/Parnamirim/RN"""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='15min')
    
    # Alimentadores da região Natal/Parnamirim
    alimentadores = [
        'AL-NAT-04 (Ponta Negra)',
        'AL-NAT-07 (Capim Macio)', 
        'AL-PAR-02 (Parnamirim Centro)',
        'AL-PAR-05 (Nova Parnamirim)'
    ]
    
    regioes = [
        'Zona Sul - Natal',
        'Zona Leste - Natal',
        'Centro - Parnamirim',
        'Cotovelo - Parnamirim'
    ]
    
    data = []
    
    for meter_id in range(1, num_meters + 1):
        id_medidor = f"RN-{39200 + meter_id:05d}"
        alimentador = np.random.choice(alimentadores)
        regiao = np.random.choice(regioes)
        consumo_base = np.random.uniform(2.0, 4.5)  # kW - perfil residencial RN
        
        for ts in timestamps:
            hora = ts.hour
            # Padrão de consumo adaptado ao clima do RN (uso de AC)
            if 12 <= hora <= 15:  # Pico de calor - uso intenso de AC
                fator = 3.2
            elif 18 <= hora <= 22:  # Noite - ainda quente
                fator = 2.8
            elif 6 <= hora <= 8:  # Manhã
                fator = 1.8
            elif 0 <= hora <= 5:  # Madrugada
                fator = 0.5
            else:
                fator = 1.2
            
            potencia = consumo_base * fator * np.random.uniform(0.88, 1.12)
            
            # Anomalias ocasionais
            if np.random.random() < 0.015:
                anomaly_type = np.random.choice(['pico_ac', 'queda', 'oscilacao'])
                if anomaly_type == 'pico_ac':
                    potencia = potencia * 4.5  # Múltiplos ACs ligados
                elif anomaly_type == 'queda':
                    potencia = 0.02
                else:
                    potencia = potencia * 0.3
            
            # Tensão (127V nominal no RN)
            tensao = 127 + np.random.normal(0, 2.5)
            
            # Subtensões mais frequentes em horário de pico
            if np.random.random() < 0.012 and 12 <= hora <= 15:
                tensao = np.random.uniform(108, 117)
            
            # Fator de potência
            fator_pot = np.random.uniform(0.87, 0.97)
            if np.random.random() < 0.025:  # FP baixo por equipamentos
                fator_pot = np.random.uniform(0.62, 0.75)
            
            data.append({
                'id_medidor': id_medidor,
                'timestamp': ts,
                'tensao_v': tensao,
                'potencia_kw': potencia,
                'fator_potencia': fator_pot,
                'energia_kwh': potencia * 0.25,
                'alimentador': alimentador,
                'regiao': regiao,
                'hora': hora,
                'temperatura_estimada': 26 + np.random.uniform(-2, 8) if 10 <= hora <= 16 else 24 + np.random.uniform(-2, 4)
            })
    
    return pd.DataFrame(data)

@st.cache_data
def detect_events_advanced(df):
    """Detecção avançada de eventos - adaptado para RN"""
    events = []
    event_id = 1
    
    for _, row in df.iterrows():
        # Subtensão (127V nominal)
        if row['tensao_v'] < 117:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'tipo': 'SUBTENSÃO',
                'severidade': 'CRÍTICA' if row['tensao_v'] < 110 else 'ALTA',
                'valor': f"{row['tensao_v']:.1f}V",
                'descricao': f"Tensão {row['tensao_v']:.1f}V abaixo do limite adequado (117V)",
                'acao_sugerida': 'Verificar transformador e rede MT - possível sobrecarga por AC',
                'destino': 'Operação',
                'impacto': 'ALTO'
            })
            event_id += 1
        
        # Sobretensão
        if row['tensao_v'] > 133:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'tipo': 'SOBRETENSÃO',
                'severidade': 'ALTA',
                'valor': f"{row['tensao_v']:.1f}V",
                'descricao': f"Tensão {row['tensao_v']:.1f}V acima do limite adequado (133V)",
                'acao_sugerida': 'Verificar regulador de tensão',
                'destino': 'Operação',
                'impacto': 'MÉDIO'
            })
            event_id += 1
        
        # Queda de energia
        if row['potencia_kw'] < 0.08:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'tipo': 'INTERRUPÇÃO',
                'severidade': 'CRÍTICA',
                'valor': f"{row['potencia_kw']:.3f}kW",
                'descricao': 'Possível interrupção no fornecimento de energia',
                'acao_sugerida': 'Despachar equipe emergencial - verificar alimentador',
                'destino': 'Operação',
                'impacto': 'CRÍTICO'
            })
            event_id += 1
        
        # Consumo anormal (pico de AC)
        if row['potencia_kw'] > 15:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'tipo': 'CONSUMO ELEVADO',
                'severidade': 'MÉDIA',
                'valor': f"{row['potencia_kw']:.2f}kW",
                'descricao': f"Consumo atípico detectado ({row['potencia_kw']:.2f}kW) - possível uso excessivo de climatização",
                'acao_sugerida': 'Análise comercial - orientar cliente sobre eficiência energética',
                'destino': 'Comercial',
                'impacto': 'BAIXO'
            })
            event_id += 1
        
        # Fator de potência baixo
        if row['fator_potencia'] < 0.75:
            events.append({
                'id_evento': f"EVT-RN-{event_id:06d}",
                'id_medidor': row['id_medidor'],
                'timestamp': row['timestamp'],
                'alimentador': row['alimentador'],
                'regiao': row['regiao'],
                'tipo': 'FP INADEQUADO',
                'severidade': 'MÉDIA',
                'valor': f"{row['fator_potencia']:.3f}",
                'descricao': f"Fator de potência {row['fator_potencia']:.3f} abaixo do regulamentado (0.92)",
                'acao_sugerida': 'Notificar cliente - sugerir correção com banco de capacitores',
                'destino': 'Cliente',
                'impacto': 'MÉDIO'
            })
            event_id += 1
    
    return pd.DataFrame(events) if events else pd.DataFrame()

# Header principal
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
            "📊 Ingestão & Qualidade",
            "📈 Visão Operacional",
            "🔍 Análise Avançada",
            "⚡ Motor de Eventos",
            "🔧 Integrações Corporativas"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### CONFIGURAÇÕES")
    
    num_meters = st.slider("📡 Medidores Ativos", 10, 100, 50, 10)
    num_days = st.slider("📅 Histórico (dias)", 1, 30, 7)
    
    if st.button("🔄 ATUALIZAR DADOS"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### STATUS DO SISTEMA")
    
    st.markdown("""
    <div style='font-size: 0.85rem; line-height: 1.8;'>
    <p><span class='status-indicator status-online'></span><strong>Ambiente:</strong> Laboratório (Sandbox)</p>
    <p><span class='status-indicator status-online'></span><strong>Dados:</strong> Sintéticos - RN</p>
    <p><span class='status-indicator status-online'></span><strong>Atualização:</strong> Tempo Real</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### STACK TECNOLÓGICO")
    
    st.markdown("""
    <div style='font-size: 0.8rem; color: #546E7A; line-height: 1.7;'>
    <strong>🟢 KERNEL:</strong> Python 3.10.12<br>
    <strong>🟢 PANDAS:</strong> 2.0.3<br>
    <strong>🟢 NUMPY:</strong> 1.24.3<br>
    <strong>🟢 PLOTLY:</strong> 5.17.0<br>
    <strong>🟢 STREAMLIT:</strong> 1.29.0
    </div>
    """, unsafe_allow_html=True)

# Carregar dados
with st.spinner("⚙️ Processando dados da rede elétrica..."):
    df = generate_smart_meter_data(num_meters, num_days)
    events_df = detect_events_advanced(df)

# PÁGINA 1: Ingestão & Qualidade
if page == "📊 Ingestão & Qualidade":
    st.markdown('<div class="section-title">Pipeline de Ingestão de Dados (MDC/MDM)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Simulação da leitura de arquivos brutos do sistema de medição centralizada, processamento ETL, validação de qualidade e cálculo de score de confiabilidade conforme PRODIST Módulo 8.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("▶️ EXECUTAR PIPELINE ETL", use_container_width=True):
            with st.spinner("Processando..."):
                st.markdown(f"""
                <div class="terminal-output">
                <span style='color: #81C784;'>user@cpfl-labs-natal:~$</span> python run_pipeline.py --source mdm --region RN --validate<br><br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Inicializando Ingestão de Dados MDM - Região RN...<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Conectando ao Data Lake AWS S3 (cosanpa-smartmeter-rn)... <span class='success'>✓ OK</span><br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Lendo arquivo: raw/mdm_export_natal_parnamirim_2026.csv...<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Schema detectado: [meter_id, timestamp, v_a, i_a, kw_tot, kvar_tot, fp, temp]<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Validando {len(df):,} registros (região Natal/Parnamirim)...<br>
                <span class='warning'>[{datetime.now().strftime('%H:%M:%S')}] WARN:</span> Detectados {int(len(df) * 0.002)} registros com gaps de timestamp (interpolação aplicada)<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Calculando estatísticas básicas por alimentador...<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Verificando conformidade PRODIST Módulo 8 (tensão 127V ±10%)...<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Gerando features avançadas: [peak_demand, voltage_quality_index, consumption_pattern]<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Aplicando detecção de anomalias (Isolation Forest + Statistical Z-Score)...<br>
                <span class='info'>[{datetime.now().strftime('%H:%M:%S')}] INFO:</span> Persistindo dados processados: data/refined/smart_meter_rn.parquet<br>
                <span class='success'>[{datetime.now().strftime('%H:%M:%S')}] SUCCESS:</span> Ingestão concluída. Tempo total: 1.4s | Taxa de processamento: {int(len(df)/1.4):,} registros/s
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <strong>📁 Fonte de Dados</strong><br>
        Origem: /data/raw/mdm_export_natal_parnamirim_2026.csv<br><br>
        <strong>🗓️ Período</strong><br>
        """ + f"{df['timestamp'].min().strftime('%d/%m/%Y %H:%M')}" + """<br>
        até """ + f"{df['timestamp'].max().strftime('%d/%m/%Y %H:%M')}" + """<br><br>
        <strong>📊 Volume</strong><br>
        """ + f"{len(df):,} leituras" + """<br>
        """ + f"{num_meters} medidores" + """
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Métricas de qualidade
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.metric("REGISTROS PROCESSADOS", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        missing = int(len(df) * 0.002)
        st.metric("DADOS CORRIGIDOS", missing, delta="-99.8%", delta_color="normal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.metric("SCORE DE CONFIABILIDADE", "99.6%", delta="+0.2%", delta_color="normal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        conformidade = ((df['tensao_v'] >= 117) & (df['tensao_v'] <= 133)).sum() / len(df) * 100
        st.metric("CONFORMIDADE PRODIST", f"{conformidade:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

# PÁGINA 2: Visão Operacional
elif page == "📈 Visão Operacional":
    st.markdown('<div class="section-title">Monitoramento Operacional da Rede Elétrica</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Visão em tempo real dos alimentadores de Natal e Parnamirim - Rio Grande do Norte</div>', unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        tensao_media = df['tensao_v'].mean()
        delta_tensao = tensao_media - 127
        st.metric("TENSÃO MÉDIA DA REDE", f"{tensao_media:.1f} V", 
                 delta=f"{delta_tensao:+.1f}V em relação ao nominal",
                 delta_color="inverse" if abs(delta_tensao) > 3 else "off")
    
    with col2:
        eventos_criticos = len(events_df[events_df['severidade'] == 'CRÍTICA']) if not events_df.empty else 0
        st.metric("EVENTOS CRÍTICOS", eventos_criticos,
                 delta=f"{eventos_criticos} requerem ação imediata" if eventos_criticos > 0 else "Sistema estável",
                 delta_color="inverse" if eventos_criticos > 0 else "normal")
    
    with col3:
        carga_total = df['potencia_kw'].sum() / 1000
        st.metric("CARGA TOTAL INSTANTÂNEA", f"{carga_total:.2f} MW")
    
    with col4:
        temp_media = df['temperatura_estimada'].mean()
        st.metric("TEMPERATURA ESTIMADA", f"{temp_media:.1f}°C",
                 delta="Alta demanda por refrigeração" if temp_media > 30 else "Normal")
    
    st.markdown("---")
    
    # Mapa e Eventos
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-title">🗺️ Geolocalização de Ativos - Região Metropolitana de Natal</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 2.5rem; border-radius: 12px; text-align: center; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #90CAF9;'>
        <h3 style='color: #003D5C; margin-bottom: 1rem;'>🛰️ Sistema GIS Integrado</h3>
        <p style='font-size: 1.1rem; color: #0277BD; font-weight: 600;'>Alimentadores Monitorados: Natal & Parnamirim</p>
        <div style='margin-top: 1.5rem; display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='margin: 0.5rem;'>
                <div style='font-size: 2rem; font-weight: 700; color: #2E7D32;'>{num_meters - eventos_criticos}</div>
                <div style='font-size: 0.9rem; color: #546E7A;'>🟢 Medidores Normais</div>
            </div>
            <div style='margin: 0.5rem;'>
                <div style='font-size: 2rem; font-weight: 700; color: #F57C00;'>{len(events_df[events_df['severidade']=='ALTA']) if not events_df.empty else 0}</div>
                <div style='font-size: 0.9rem; color: #546E7A;'>🟡 Com Alerta</div>
            </div>
            <div style='margin: 0.5rem;'>
                <div style='font-size: 2rem; font-weight: 700; color: #C62828;'>{eventos_criticos}</div>
                <div style='font-size: 0.9rem; color: #546E7A;'>🔴 Críticos</div>
            </div>
        </div>
        <p style='margin-top: 1.5rem; font-size: 0.85rem; color: #546E7A;'>
        Cobertura: Zona Sul, Zona Leste (Natal) | Centro, Nova Parnamirim (Parnamirim)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚨 EVENTOS PRIORITÁRIOS")
        
        if not events_df.empty:
            priority_events = events_df[events_df['severidade'].isin(['CRÍTICA', 'ALTA'])].head(5)
            
            for _, evt in priority_events.iterrows():
                if evt['severidade'] == 'CRÍTICA':
                    badge_class = "badge-critico"
                elif evt['severidade'] == 'ALTA':
                    badge_class = "badge-alerta"
                else:
                    badge_class = "badge-media"
                
                st.markdown(f"""
                <div class="section-card" style="margin-bottom: 1rem;">
                    <span class="status-badge {badge_class}">{evt['severidade']}</span>
                    <h4 style='color: #003D5C; margin: 0.5rem 0;'>{evt['tipo']}</h4>
                    <p style='margin: 0.3rem 0; font-size: 0.9rem;'><strong>ID:</strong> {evt['id_medidor']}</p>
                    <p style='margin: 0.3rem 0; font-size: 0.85rem; color: #546E7A;'>{evt['regiao']}</p>
                    <p style='margin: 0.5rem 0; font-size: 0.9rem;'>{evt['descricao']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Sistema operando em condições normais - Nenhum evento prioritário")
    
    st.markdown("---")
    
    # Balanço Energético
    st.markdown('<div class="section-title">⚡ Balanço Energético por Alimentador (Últimas 24h)</div>', unsafe_allow_html=True)
    
    last_24h = df[df['timestamp'] >= (datetime.now() - timedelta(hours=24))]
    
    # Gráfico por alimentador
    alim_energy = last_24h.groupby(['alimentador', last_24h['timestamp'].dt.hour]).agg({
        'energia_kwh': 'sum'
    }).reset_index()
    
    fig = px.bar(alim_energy, x='timestamp', y='energia_kwh', color='alimentador',
                 labels={'timestamp': 'Hora do Dia', 'energia_kwh': 'Energia (kWh)', 'alimentador': 'Alimentador'},
                 title='Consumo Energético Horário por Alimentador',
                 color_discrete_sequence=['#00A9CE', '#0088AA', '#006688', '#004466'])
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# PÁGINA 3: Análise Avançada
elif page == "🔍 Análise Avançada":
    st.markdown('<div class="section-title">Análise Detalhada de Medidor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Análise técnica individual com indicadores de qualidade PRODIST Módulo 8</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("#### 🔍 SELEÇÃO")
        selected_meter = st.selectbox("Medidor", sorted(df['id_medidor'].unique()), label_visibility="collapsed")
        
        period = st.selectbox("Período de Análise", 
                             ["Últimas 24 Horas", "Últimos 7 Dias", "Últimos 30 Dias"],
                             label_visibility="collapsed")
        
        if st.button("🔄 ATUALIZAR ANÁLISE", use_container_width=True):
            st.rerun()
        
        meter_data = df[df['id_medidor'] == selected_meter]
        
        if not meter_data.empty:
            st.markdown("---")
            st.markdown("#### 📊 RESUMO")
            st.markdown(f"""
            <div style='font-size: 0.85rem; line-height: 1.8;'>
            <strong>Alimentador:</strong><br>{meter_data['alimentador'].iloc[0]}<br><br>
            <strong>Região:</strong><br>{meter_data['regiao'].iloc[0]}<br><br>
            <strong>Leituras:</strong><br>{len(meter_data):,}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if not meter_data.empty:
            st.markdown(f"#### 📡 MEDIDOR: {selected_meter}")
            
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Consumo Médio", f"{meter_data['energia_kwh'].mean():.2f} kWh/15min")
            col_b.metric("Fator de Potência", f"{meter_data['fator_potencia'].mean():.3f}")
            col_c.metric("Tensão Média", f"{meter_data['tensao_v'].mean():.1f} V")
            col_d.metric("Temp. Estimada", f"{meter_data['temperatura_estimada'].mean():.1f}°C")
    
    st.markdown("---")
    
    # Gráficos técnicos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">📊 Perfil de Tensão (PRODIST Módulo 8)</div>', unsafe_allow_html=True)
        st.caption("Tensão nominal 127V | Faixa adequada: 117V - 133V | Precário: 110-117V / 133-135V")
        
        meter_sorted = meter_data.sort_values('timestamp').tail(200)
        
        fig = go.Figure()
        
        # Linha de tensão
        fig.add_trace(go.Scatter(
            x=meter_sorted['timestamp'],
            y=meter_sorted['tensao_v'],
            mode='lines',
            name='Tensão Medida',
            line=dict(color='#00A9CE', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(0,169,206,0.1)'
        ))
        
        # Limites PRODIST
        fig.add_hline(y=133, line_dash="dash", line_color="#F57C00", 
                     annotation_text="Limite Superior Adequado (133V)",
                     annotation_position="right")
        fig.add_hline(y=127, line_dash="dot", line_color="#4CAF50",
                     annotation_text="Tensão Nominal (127V)",
                     annotation_position="right")
        fig.add_hline(y=117, line_dash="dash", line_color="#F57C00",
                     annotation_text="Limite Inferior Adequado (117V)",
                     annotation_position="right")
        
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="",
            yaxis_title="Tensão (V)",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-title">⚡ Curva de Carga Diária</div>', unsafe_allow_html=True)
        st.caption("Padrão de consumo por hora do dia - Identificação de picos de demanda")
        
        hourly_profile = meter_data.groupby('hora').agg({
            'potencia_kw': ['mean', 'max'],
            'energia_kwh': 'sum'
        }).reset_index()
        hourly_profile.columns = ['hora', 'potencia_media', 'potencia_max', 'energia_total']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=hourly_profile['hora'],
            y=hourly_profile['potencia_media'],
            name='Potência Média',
            marker_color='#FFB300',
            marker_line_color='#FF8F00',
            marker_line_width=1.5
        ))
        
        fig.add_trace(go.Scatter(
            x=hourly_profile['hora'],
            y=hourly_profile['potencia_max'],
            name='Pico de Demanda',
            line=dict(color='#C62828', width=3),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Hora do Dia",
            yaxis_title="Potência (kW)",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# PÁGINA 4: Motor de Eventos
elif page == "⚡ Motor de Eventos":
    st.markdown('<div class="section-title">⚡ Motor de Regras e Detecção de Eventos</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Sistema inteligente de detecção baseado em regras determinísticas e algoritmos de análise para geração automática de insights operacionais e comerciais</div>', unsafe_allow_html=True)
    
    if not events_df.empty:
        # Filtros avançados
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            tipo_filter = st.multiselect("🏷️ Tipo de Evento", events_df['tipo'].unique())
        with col2:
            sev_filter = st.multiselect("⚠️ Severidade", events_df['severidade'].unique())
        with col3:
            dest_filter = st.multiselect("📍 Destino", events_df['destino'].unique())
        with col4:
            alim_filter = st.multiselect("🔌 Alimentador", events_df['alimentador'].unique())
        
        # Aplicar filtros
        filtered = events_df.copy()
        if tipo_filter:
            filtered = filtered[filtered['tipo'].isin(tipo_filter)]
        if sev_filter:
            filtered = filtered[filtered['severidade'].isin(sev_filter)]
        if dest_filter:
            filtered = filtered[filtered['destino'].isin(dest_filter)]
        if alim_filter:
            filtered = filtered[filtered['alimentador'].isin(alim_filter)]
        
        st.markdown("---")
        
        # Métricas de eventos
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Eventos", len(filtered))
        col2.metric("Críticos", len(filtered[filtered['severidade']=='CRÍTICA']))
        col3.metric("Altos", len(filtered[filtered['severidade']=='ALTA']))
        col4.metric("Médios", len(filtered[filtered['severidade']=='MÉDIA']))
        
        st.markdown("---")
        
        # Tabela de eventos
        st.dataframe(
            filtered[['id_evento', 'id_medidor', 'alimentador', 'tipo', 'severidade', 
                     'valor', 'acao_sugerida', 'destino', 'impacto']],
            use_container_width=True,
            height=450
        )
        
        # Botão de exportação
        csv = filtered.to_csv(index=False)
        st.download_button(
            label="📥 EXPORTAR EVENTOS (CSV)",
            data=csv,
            file_name=f"eventos_rn_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=False
        )
        
    else:
        st.success("✅ Sistema operando normalmente - Nenhum evento detectado no período selecionado")

# PÁGINA 5: Integrações
else:
    st.markdown('<div class="section-title">🔧 Integrações Corporativas</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Interfaces de integração com sistemas GIS, ADMS e SAP para automação de processos operacionais</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🗺️ GIS - Sistema de Informações Geográficas", 
                                 "⚡ ADMS - Gestão Avançada de Distribuição", 
                                 "💼 SAP - Ordens de Serviço"])
    
    with tab1:
        st.markdown("### 🗺️ Sistema de Informações Geográficas (GIS)")
        st.markdown("Integração com base cartográfica e cadastro de ativos da rede de distribuição")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 ALIMENTADORES MONITORADOS")
            
            for alim in df['alimentador'].unique():
                alim_data = df[df['alimentador'] == alim]
                carga = alim_data['potencia_kw'].sum() / 1000
                medidores = alim_data['id_medidor'].nunique()
                
                st.markdown(f"""
                <div style='margin: 1rem 0; padding: 1rem; background: #F5F7FA; border-radius: 8px;'>
                <strong style='color: #003D5C;'>{alim}</strong><br>
                <span style='font-size: 0.9rem; color: #546E7A;'>
                Carga: {carga:.2f} MW | Medidores: {medidores}
                </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 📡 STATUS DE COMUNICAÇÃO")
            
            taxa_comunicacao = np.random.uniform(98.5, 99.8)
            medidores_offline = int(num_meters * (1 - taxa_comunicacao/100))
            
            st.markdown(f"""
            <div style='margin: 1rem 0;'>
            <div style='margin: 0.8rem 0;'>
            <strong>Medidores Online:</strong> {num_meters - medidores_offline} / {num_meters}<br>
            <strong>Taxa de Comunicação:</strong> {taxa_comunicacao:.1f}%<br>
            <strong>Última Atualização:</strong> {datetime.now().strftime('%H:%M:%S')}
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(taxa_comunicacao/100)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### ⚡ Advanced Distribution Management System (ADMS)")
        st.markdown("Correlação de eventos, detecção de interrupções e suporte à tomada de decisão operacional")
        
        if not events_df.empty:
            criticos = events_df[events_df['severidade'] == 'CRÍTICA']
            
            if not criticos.empty:
                st.warning(f"⚠️ **ALERTA:** {len(criticos)} eventos críticos detectados - possível interrupção ou degradação do fornecimento")
                
                st.markdown("#### 🚨 EVENTOS CRÍTICOS ATIVOS")
                
                for i, (_, evt) in enumerate(criticos.head(5).iterrows(), 1):
                    st.markdown(f"""
                    <div class="section-card" style="border-left-color: #C62828;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #C62828;">{evt['tipo']}</h4>
                                <p style="margin: 0.3rem 0;"><strong>{evt['id_medidor']}</strong> | {evt['alimentador']}</p>
                                <p style="margin: 0.3rem 0; font-size: 0.9rem; color: #546E7A;">{evt['regiao']}</p>
                            </div>
                            <div>
                                <span class="status-badge badge-critico">{evt['severidade']}</span>
                            </div>
                        </div>
                        <p style="margin: 0.8rem 0 0.3rem 0;"><strong>Descrição:</strong> {evt['descricao']}</p>
                        <p style="margin: 0.3rem 0;"><strong>Ação Sugerida:</strong> {evt['acao_sugerida']}</p>
                        <p style="margin: 0.3rem 0; font-size: 0.85rem; color: #546E7A;">
                        <strong>Timestamp:</strong> {evt['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ **SISTEMA NORMAL:** Rede operando em condições adequadas")
        else:
            st.success("✅ **SISTEMA NORMAL:** Nenhum evento detectado")
    
    with tab3:
        st.markdown("### 💼 Sistema SAP - Geração Automática de Ordens de Serviço")
        st.markdown("Integração com ERP para criação automatizada de OS a partir de eventos críticos e de alta prioridade")
        
        if not events_df.empty:
            os_events = events_df[events_df['severidade'].isin(['CRÍTICA', 'ALTA'])]
            
            if not os_events.empty:
                col1, col2, col3, col4 = st.columns(4)
                
                num_os = len(os_events)
                custo_medio = 1200 if 'CRÍTICA' in os_events['severidade'].values else 800
                custo_total = num_os * custo_medio
                equipes = max(1, num_os // 4)
                
                col1.metric("OS GERADAS", num_os)
                col2.metric("CUSTO ESTIMADO", f"R$ {custo_total:,.2f}")
                col3.metric("EQUIPES NECESSÁRIAS", equipes)
                col4.metric("PRAZO MÉDIO", "4-6h" if 'CRÍTICA' in os_events['severidade'].values else "24-48h")
                
                st.markdown("---")
                st.markdown("#### 📋 ORDENS DE SERVIÇO CRIADAS")
                
                for i, (_, evt) in enumerate(os_events.head(8).iterrows(), 1):
                    os_id = f"OS-RN-{202501000 + i}"
                    tipo_os = "EMERGENCIAL" if evt['severidade'] == 'CRÍTICA' else "CORRETIVA"
                    
                    st.markdown(f"""
                    <div class="section-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                            <h4 style="margin: 0; color: #003D5C;">{os_id}</h4>
                            <span class="status-badge {'badge-critico' if evt['severidade']=='CRÍTICA' else 'badge-alerta'}">{tipo_os}</span>
                        </div>
                        <p style="margin: 0.3rem 0;"><strong>Tipo de Serviço:</strong> {evt['tipo']}</p>
                        <p style="margin: 0.3rem 0;"><strong>Medidor:</strong> {evt['id_medidor']}</p>
                        <p style="margin: 0.3rem 0;"><strong>Local:</strong> {evt['regiao']}</p>
                        <p style="margin: 0.3rem 0;"><strong>Alimentador:</strong> {evt['alimentador']}</p>
                        <p style="margin: 0.3rem 0;"><strong>Prioridade:</strong> {evt['severidade']}</p>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #546E7A;">
                        <strong>Ação:</strong> {evt['acao_sugerida']}
                        </p>
                        <p style="margin: 0.3rem 0; font-size: 0.85rem; color: #546E7A;">
                        <strong>Custo Estimado:</strong> R$ {custo_medio:,.2f} | 
                        <strong>Criado em:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nenhuma ordem de serviço gerada automaticamente no período atual")
        else:
            st.info("ℹ️ Sistema sem eventos que requeiram abertura de OS")

# Footer profissional
st.markdown("---")
st.markdown(f"""
<div class="status-footer">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <strong>🔷 CPFL LABS</strong> | Projeto P&D ANEEL | 
            <strong>Tema 3:</strong> Aplicações e Gestão de Dados de Smart Meters
        </div>
        <div style="text-align: right;">
            <strong>Localização:</strong> Natal, Parnamirim e Rio Grande do Norte | 
            <strong>Atualizado:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    </div>
    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #D5DDE5; font-size: 0.8rem;">
        <strong>Stack Tecnológico:</strong> Python 3.10.12 | Pandas 2.0.3 | NumPy 1.24.3 | Plotly 5.17.0 | Streamlit 1.29.0 | 
        <strong>Ambiente:</strong> Laboratório (Sandbox) com dados sintéticos
    </div>
</div>
""", unsafe_allow_html=True)
