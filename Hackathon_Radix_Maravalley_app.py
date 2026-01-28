"""
Aplicação Web - LABS Plataforma de Insights do Smart Meter
Interface principal para visualização de dados, eventos e dashboards
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

from ingestion.data_ingestion import SmartMeterDataIngestion
from processing.data_quality import DataQualityProcessor
from analytics.feature_engineering import FeatureEngineering
from events.event_engine import EventEngine
from integration.corporate_integration import CorporateIntegration

# Configuração da página
st.set_page_config(
    page_title="Smart Meter Insights LABS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Funções auxiliares
@st.cache_data
def load_data():
    """Carrega dados do banco de dados"""
    ingestion = SmartMeterDataIngestion()
    df = ingestion.load_from_database()
    
    if df.empty:
        # Se não há dados, gerar sintéticos
        st.warning("Banco de dados vazio. Gerando dados sintéticos...")
        df = ingestion.generate_synthetic_data(num_meters=50, days=7)
        ingestion.save_to_database(df)
    
    return df


@st.cache_data
def process_data(df):
    """Processa dados com pipeline de qualidade"""
    processor = DataQualityProcessor()
    df_processed, log = processor.process_pipeline(df)
    return df_processed, log


@st.cache_data
def engineer_features(df):
    """Aplica feature engineering"""
    fe = FeatureEngineering()
    df = fe.create_time_features(df)
    df = fe.detect_consumption_steps(df)
    df = fe.calculate_statistical_features(df)
    
    patterns = fe.calculate_consumption_patterns(df)
    metrics = fe.calculate_power_quality_metrics(df)
    
    return df, patterns, metrics


@st.cache_data
def detect_events(df):
    """Detecta eventos"""
    engine = EventEngine()
    events_df, summary = engine.process_all_events(df)
    return events_df, summary


def main():
    # Header
    st.markdown('<p class="main-header">⚡ Smart Meter Insights LABS</p>', unsafe_allow_html=True)
    st.markdown("**Plataforma de Insights para Cliente e Operação - Protótipo P&D ANEEL**")
    
    # Sidebar
    st.sidebar.title("🎛️ Navegação")
    page = st.sidebar.radio(
        "Selecione a visualização:",
        ["📊 Visão Geral", "👤 Portal do Cliente", "🔧 Portal Operacional", 
         "📈 Análises Avançadas", "⚙️ Gerenciamento de Dados"]
    )
    
    # Carregar dados
    with st.spinner("Carregando dados..."):
        df_raw = load_data()
        df_processed, quality_log = process_data(df_raw)
        df_featured, patterns, metrics = engineer_features(df_processed)
        events_df, events_summary = detect_events(df_featured)
    
    # Processar integrações
    integration = CorporateIntegration()
    integration_results = integration.process_events_with_integration(events_df, df_featured)
    
    # Roteamento de páginas
    if page == "📊 Visão Geral":
        show_overview(df_featured, events_summary, quality_log, integration_results)
    elif page == "👤 Portal do Cliente":
        show_client_portal(df_featured, events_df, patterns)
    elif page == "🔧 Portal Operacional":
        show_operation_portal(df_featured, events_df, integration_results)
    elif page == "📈 Análises Avançadas":
        show_advanced_analytics(df_featured, patterns, metrics)
    elif page == "⚙️ Gerenciamento de Dados":
        show_data_management(df_raw, df_processed, quality_log)


def show_overview(df, events_summary, quality_log, integration_results):
    """Página de visão geral"""
    st.header("📊 Visão Geral do Sistema")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Medidores",
            df['id_medidor'].nunique(),
            help="Número total de smart meters monitorados"
        )
    
    with col2:
        st.metric(
            "Leituras Processadas",
            f"{len(df):,}",
            help="Total de leituras no período"
        )
    
    with col3:
        st.metric(
            "Eventos Detectados",
            events_summary.get('total_eventos', 0),
            delta=f"{events_summary.get('eventos_criticos', 0)} críticos",
            delta_color="inverse"
        )
    
    with col4:
        score_medio = quality_log.get('avg_confidence_score', 0)
        st.metric(
            "Score de Qualidade",
            f"{score_medio}%",
            help="Score médio de confiabilidade dos dados"
        )
    
    st.divider()
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição de Eventos por Severidade")
        if events_summary.get('por_severidade'):
            fig = px.pie(
                values=list(events_summary['por_severidade'].values()),
                names=list(events_summary['por_severidade'].keys()),
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum evento detectado")
    
    with col2:
        st.subheader("Carga por Alimentador")
        if 'feeder_load' in integration_results:
            feeder_load = integration_results['feeder_load']
            fig = px.bar(
                feeder_load,
                x='alimentador',
                y='carga_total_kw',
                color='carregamento_pct',
                text='carregamento_pct',
                labels={'carga_total_kw': 'Carga Total (kW)', 'carregamento_pct': 'Carregamento (%)'}
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    # Timeline de eventos
    st.subheader("Timeline de Consumo e Eventos")
    
    # Agregar consumo por hora
    df_hourly = df.groupby(df['timestamp'].dt.floor('H')).agg({
        'potencia_ativa_kw': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_hourly['timestamp'],
        y=df_hourly['potencia_ativa_kw'],
        mode='lines',
        name='Consumo Total',
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        xaxis_title="Data/Hora",
        yaxis_title="Potência Total (kW)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_client_portal(df, events_df, patterns):
    """Portal do cliente"""
    st.header("👤 Portal do Cliente")
    
    # Seletor de medidor
    meters = sorted(df['id_medidor'].unique())
    selected_meter = st.selectbox("Selecione seu medidor:", meters)
    
    # Filtrar dados do medidor
    df_meter = df[df['id_medidor'] == selected_meter].copy()
    events_meter = events_df[
        (events_df['id_medidor'] == selected_meter) & 
        (events_df['destino'] == 'cliente')
    ] if not events_df.empty else pd.DataFrame()
    
    # Padrão de consumo
    if not patterns.empty:
        meter_pattern = patterns[patterns['id_medidor'] == selected_meter]
        
        if not meter_pattern.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Consumo Médio Diário",
                    f"{meter_pattern['consumo_medio_diario'].values[0]:.2f} kWh"
                )
            
            with col2:
                st.metric(
                    "Perfil de Consumo",
                    meter_pattern['perfil_consumo'].values[0]
                )
            
            with col3:
                st.metric(
                    "Estabilidade",
                    meter_pattern['estabilidade'].values[0]
                )
    
    st.divider()
    
    # Alertas para o cliente
    if not events_meter.empty:
        st.subheader("🔔 Seus Alertas")
        
        for _, event in events_meter.head(5).iterrows():
            severity_class = f"alert-{event['severidade'].lower()}" if event['severidade'].lower() in ['critical', 'high', 'medium'] else 'alert-medium'
            
            st.markdown(f"""
            <div class="{severity_class}">
                <strong>{event['tipo_evento']}</strong> - {event['severidade']}<br>
                {event['descricao']}<br>
                <em>Sugestão: {event['acao_sugerida']}</em>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhum alerta no momento")
    
    # Histórico de consumo
    st.subheader("📊 Histórico de Consumo")
    
    tab1, tab2 = st.tabs(["Por Hora", "Por Dia"])
    
    with tab1:
        # Consumo por hora do dia
        hourly_avg = df_meter.groupby('hora')['potencia_ativa_kw'].mean().reset_index()
        
        fig = px.bar(
            hourly_avg,
            x='hora',
            y='potencia_ativa_kw',
            labels={'hora': 'Hora do Dia', 'potencia_ativa_kw': 'Consumo Médio (kW)'},
            title="Perfil de Consumo por Hora"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Consumo diário
        daily = df_meter.groupby(df_meter['timestamp'].dt.date).agg({
            'energia_q1_kwh': 'sum'
        }).reset_index()
        daily.columns = ['data', 'consumo_kwh']
        
        fig = px.line(
            daily,
            x='data',
            y='consumo_kwh',
            labels={'data': 'Data', 'consumo_kwh': 'Consumo Diário (kWh)'},
            title="Consumo Diário"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Fator de potência
    st.subheader("⚡ Qualidade de Energia")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fp_avg = df_meter['fator_potencia'].mean()
        st.metric(
            "Fator de Potência Médio",
            f"{fp_avg:.3f}",
            help="Ideal: acima de 0.92"
        )
        
        if fp_avg < 0.92:
            st.warning("⚠️ Seu fator de potência está abaixo do ideal. Considere instalar capacitores para correção.")
    
    with col2:
        tensao_avg = df_meter['tensao_v'].mean()
        st.metric(
            "Tensão Média",
            f"{tensao_avg:.1f} V"
        )


def show_operation_portal(df, events_df, integration_results):
    """Portal operacional"""
    st.header("🔧 Portal Operacional")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        alimentador_filter = st.multiselect(
            "Filtrar por Alimentador:",
            options=sorted(df['alimentador'].unique()),
            default=None
        )
    
    with col2:
        severidade_filter = st.selectbox(
            "Severidade Mínima:",
            options=['TODAS', 'CRITICA', 'ALTA', 'MEDIA', 'BAIXA'],
            index=0
        )
    
    with col3:
        periodo = st.selectbox(
            "Período:",
            options=['Últimas 24h', 'Últimos 7 dias', 'Últimos 30 dias', 'Tudo'],
            index=1
        )
    
    # Aplicar filtros
    df_filtered = df.copy()
    events_filtered = events_df.copy() if not events_df.empty else pd.DataFrame()
    
    if alimentador_filter:
        df_filtered = df_filtered[df_filtered['alimentador'].isin(alimentador_filter)]
        if not events_filtered.empty and 'alimentador' in events_filtered.columns:
            events_filtered = events_filtered[events_filtered['alimentador'].isin(alimentador_filter)]
    
    if severidade_filter != 'TODAS' and not events_filtered.empty:
        severity_map = {'CRITICA': 4, 'ALTA': 3, 'MEDIA': 2, 'BAIXA': 1}
        min_sev = severity_map[severidade_filter]
        events_filtered = events_filtered[
            events_filtered['severidade'].map(severity_map) >= min_sev
        ]
    
    st.divider()
    
    # Métricas operacionais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Eventos Operacionais", len(events_filtered))
    
    with col2:
        interrup = integration_results.get('outages', [])
        st.metric("Interrupções Detectadas", len(interrup))
    
    with col3:
        os_summary = integration_results.get('os_summary', {})
        st.metric("Ordens de Serviço", os_summary.get('total_os', 0))
    
    with col4:
        custo = os_summary.get('custo_total_estimado', 0)
        st.metric("Custo Estimado", f"R$ {custo:,.2f}")
    
    # Eventos priorizados
    st.subheader("🚨 Eventos Priorizados")
    
    if not events_filtered.empty:
        # Mostrar top 10 eventos
        display_cols = ['ranking', 'tipo_evento', 'severidade', 'id_medidor', 
                       'timestamp', 'descricao', 'acao_sugerida']
        
        available_cols = [col for col in display_cols if col in events_filtered.columns]
        
        st.dataframe(
            events_filtered[available_cols].head(10),
            use_container_width=True,
            hide_index=True
        )
        
        # Download
        csv = events_filtered.to_csv(index=False)
        st.download_button(
            "📥 Download Eventos (CSV)",
            csv,
            "eventos_operacionais.csv",
            "text/csv"
        )
    else:
        st.info("Nenhum evento operacional no período selecionado")
    
    # Interrupções
    if interrup:
        st.subheader("⚠️ Interrupções em Andamento")
        
        for outage in interrup:
            with st.expander(f"🔴 {outage['alimentador']} - {outage['medidores_afetados']} medidores afetados"):
                st.write(f"**ID:** {outage['id_interrupcao']}")
                st.write(f"**Início:** {outage['timestamp']}")
                st.write(f"**Medidores afetados:** {outage['medidores_afetados']}")
                st.write(f"**Causa provável:** {outage['causa_provavel']}")
                st.write(f"**Prioridade:** {outage['prioridade']}")
    
    # Ordens de serviço
    if integration_results.get('service_orders'):
        st.subheader("📋 Ordens de Serviço Geradas")
        
        df_os = pd.DataFrame(integration_results['service_orders'])
        
        st.dataframe(
            df_os[['id_os', 'tipo_os', 'prioridade', 'id_medidor', 'descricao', 'status', 'custo_estimado']].head(10),
            use_container_width=True,
            hide_index=True
        )


def show_advanced_analytics(df, patterns, metrics):
    """Análises avançadas"""
    st.header("📈 Análises Avançadas")
    
    tab1, tab2, tab3 = st.tabs(["Padrões de Consumo", "Qualidade de Energia", "Análise por Região"])
    
    with tab1:
        st.subheader("Padrões de Consumo")
        
        if not patterns.empty:
            # Distribuição de perfis
            perfil_dist = patterns['perfil_consumo'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    values=perfil_dist.values,
                    names=perfil_dist.index,
                    title="Distribuição de Perfis de Consumo"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(
                    patterns,
                    x='consumo_medio_diario',
                    y='cv_consumo',
                    color='perfil_consumo',
                    size='consumo_maximo',
                    hover_data=['id_medidor'],
                    title="Consumo vs. Variabilidade",
                    labels={
                        'consumo_medio_diario': 'Consumo Médio Diário (kWh)',
                        'cv_consumo': 'Coeficiente de Variação'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Métricas de Qualidade de Energia")
        
        if not metrics.empty:
            # Tensão
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    metrics,
                    x='tensao_media',
                    nbins=30,
                    title="Distribuição de Tensão Média",
                    labels={'tensao_media': 'Tensão Média (V)'}
                )
                fig.add_vline(x=220, line_dash="dash", line_color="green", annotation_text="Nominal")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(
                    metrics,
                    x='fp_medio',
                    nbins=30,
                    title="Distribuição de Fator de Potência",
                    labels={'fp_medio': 'Fator de Potência Médio'}
                )
                fig.add_vline(x=0.92, line_dash="dash", line_color="green", annotation_text="Ideal")
                st.plotly_chart(fig, use_container_width=True)
            
            # Problemas detectados
            st.subheader("Problemas de Qualidade Detectados")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Subtensões", metrics['subtensao_detectada'].sum())
            
            with col2:
                st.metric("Sobretensões", metrics['sobretensao_detectada'].sum())
            
            with col3:
                st.metric("FP Baixo", metrics['fp_baixo_detectado'].sum())
    
    with tab3:
        st.subheader("Análise por Região/Alimentador")
        
        # Agregação por alimentador
        agg_alim = df.groupby('alimentador').agg({
            'potencia_ativa_kw': ['mean', 'max'],
            'tensao_v': 'mean',
            'id_medidor': 'nunique'
        }).reset_index()
        
        agg_alim.columns = ['alimentador', 'demanda_media', 'demanda_maxima', 'tensao_media', 'num_medidores']
        
        st.dataframe(agg_alim, use_container_width=True, hide_index=True)
        
        # Mapa de calor de consumo por alimentador e hora
        heatmap_data = df.groupby(['alimentador', 'hora'])['potencia_ativa_kw'].mean().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='alimentador', columns='hora', values='potencia_ativa_kw')
        
        fig = px.imshow(
            heatmap_pivot,
            labels=dict(x="Hora do Dia", y="Alimentador", color="kW"),
            title="Mapa de Calor: Demanda por Alimentador e Hora",
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)


def show_data_management(df_raw, df_processed, quality_log):
    """Gerenciamento de dados"""
    st.header("⚙️ Gerenciamento de Dados")
    
    tab1, tab2, tab3 = st.tabs(["Pipeline de Qualidade", "Geração de Dados", "Exportação"])
    
    with tab1:
        st.subheader("Relatório de Qualidade")
        
        # Métricas de qualidade
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Registros Processados",
                f"{quality_log['output_records']:,}",
                delta=f"{quality_log['output_records'] - quality_log['input_records']}"
            )
        
        with col2:
            st.metric(
                "Score Médio",
                f"{quality_log['avg_confidence_score']}%"
            )
        
        with col3:
            duplicates = quality_log['duplicates']['duplicatas_removidas']
            st.metric("Duplicatas Removidas", duplicates)
        
        # Detalhes do pipeline
        with st.expander("📋 Detalhes do Pipeline de Qualidade"):
            st.json(quality_log)
    
    with tab2:
        st.subheader("Geração de Dados Sintéticos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num_meters = st.number_input("Número de Medidores", 10, 200, 50)
        
        with col2:
            num_days = st.number_input("Dias de Histórico", 1, 30, 7)
        
        with col3:
            interval = st.number_input("Intervalo (min)", 15, 60, 15)
        
        if st.button("🔄 Gerar Novos Dados"):
            with st.spinner("Gerando dados..."):
                ingestion = SmartMeterDataIngestion()
                new_df = ingestion.generate_synthetic_data(
                    num_meters=num_meters,
                    days=num_days,
                    interval_minutes=interval
                )
                ingestion.save_to_database(new_df)
                st.success(f"✅ {len(new_df)} registros gerados e salvos!")
                st.rerun()
    
    with tab3:
        st.subheader("Exportação de Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV
            csv = df_processed.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                "smart_meter_data.csv",
                "text/csv"
            )
        
        with col2:
            # Parquet
            if st.button("💾 Salvar em Parquet"):
                ingestion = SmartMeterDataIngestion()
                ingestion.save_to_parquet(df_processed, "processed_data")
                st.success("✅ Dados salvos em formato Parquet!")


if __name__ == "__main__":
    main()
