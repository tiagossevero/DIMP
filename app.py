"""
DIMP - Dashboard de Inteligência de Meios de Pagamento
Versão 2.0 - Refatorada e Otimizada
Receita Estadual de Santa Catarina
Desenvolvido por: Auditor Fiscal Tiago Severo
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Imports dos módulos
from config.settings import PAGE_CONFIG, SYSTEM_INFO
from config.constants import CSS_STYLES, PAGES, ICONS, MESSAGES
from utils.auth import check_password
from utils.formatters import (
    format_currency, format_percentage, format_number,
    get_risk_color, get_risk_emoji, create_download_button
)
from database.connection import get_engine, test_connection
from database.queries import load_main_data, filter_data, search_empresa
from analytics.kpis import (
    calculate_kpis, calculate_kpis_by_classification,
    calculate_kpis_by_municipio, get_top_empresas
)
from analytics.statistics import calculate_descriptive_stats, calculate_correlation_matrix
from visualizations.charts import (
    create_risk_distribution_pie, create_top_empresas_bar,
    create_scatter_cpf_vs_total, create_histogram,
    create_correlation_heatmap, create_box_plot
)
from ml.models import train_random_forest, detect_anomalies, get_ml_insights

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================

st.set_page_config(**PAGE_CONFIG)

# Aplicar CSS customizado
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Autenticação
check_password()

# =============================================================================
# SIDEBAR - NAVEGAÇÃO E FILTROS
# =============================================================================

with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #1565c0; margin: 0;'>💳 DIMP</h1>
            <p style='color: #666; font-size: 0.9rem; margin: 5px 0;'>
                Dashboard de Inteligência<br>de Meios de Pagamento
            </p>
            <hr style='margin: 15px 0;'>
        </div>
    """, unsafe_allow_html=True)

    # Seleção de página
    st.markdown("### 📑 Navegação")
    page_names = [p['name'] for p in PAGES]
    selected_page = st.radio(
        "Selecione a página:",
        page_names,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Informações do sistema
    with st.expander("ℹ️ Informações do Sistema"):
        st.markdown(f"""
            **Versão:** {SYSTEM_INFO['version']}
            **Autor:** {SYSTEM_INFO['author']}
            **Organização:** {SYSTEM_INFO['organization']}
        """)

# =============================================================================
# CARREGAMENTO DE DADOS
# =============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_all_data():
    """Carrega todos os dados necessários"""
    engine = get_engine()
    if engine is None:
        return None

    with st.spinner(MESSAGES['loading']['data']):
        df = load_main_data(engine)

    return df

# Carregar dados
df_main = load_all_data()

if df_main is None or df_main.empty:
    st.error(MESSAGES['error']['no_data'])
    st.stop()

# =============================================================================
# PÁGINA: DASHBOARD EXECUTIVO
# =============================================================================

def page_dashboard_executivo():
    st.markdown("<h1 class='main-header'>📊 Dashboard Executivo</h1>", unsafe_allow_html=True)

    # Filtros
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            classificacoes = st.multiselect(
                "Classificação de Risco",
                options=['ALTO', 'MÉDIO-ALTO', 'MÉDIO', 'BAIXO'],
                default=['ALTO', 'MÉDIO-ALTO']
            )

        with col2:
            score_min = st.slider("Score Mínimo", 0, 100, 0)

        with col3:
            perc_cpf_min = st.slider("% CPF Mínimo", 0, 100, 0)

    # Aplicar filtros
    df_filtered = filter_data(
        df_main,
        classificacao=classificacoes if classificacoes else None,
        score_min=score_min,
        perc_cpf_min=perc_cpf_min
    )

    # KPIs Principais
    kpis = calculate_kpis(df_filtered)

    st.markdown("### 📊 Indicadores Principais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total de Empresas",
            format_number(kpis['total_empresas']),
            help="Total de empresas analisadas"
        )

    with col2:
        st.metric(
            "Volume Total",
            format_currency(kpis['volume_total']),
            help="Soma de todos os pagamentos"
        )

    with col3:
        st.metric(
            "Volume via CPF",
            format_currency(kpis['volume_cpf']),
            delta=format_percentage(kpis['perc_total_cpf']),
            help="Total recebido via CPF de sócios"
        )

    with col4:
        st.metric(
            "Score Médio",
            f"{kpis['media_score_risco']:.2f}",
            help="Score médio de risco"
        )

    st.markdown("---")

    # Segunda linha de KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            f"{get_risk_emoji('ALTO')} Risco Alto",
            format_number(kpis['empresas_alto_risco']),
            delta=format_percentage(kpis['perc_alto_risco']),
            help="Empresas com risco alto"
        )

    with col2:
        st.metric(
            f"{get_risk_emoji('MÉDIO-ALTO')} Médio-Alto",
            format_number(kpis['empresas_medio_alto']),
            delta=format_percentage(kpis['perc_medio_alto']),
            help="Empresas com risco médio-alto"
        )

    with col3:
        st.metric(
            "Alertas Críticos",
            format_number(kpis['empresas_alerta_critico']),
            help="Empresas com score ≥ 90"
        )

    with col4:
        st.metric(
            ">50% via CPF",
            format_number(kpis['empresas_acima_50pct_cpf']),
            help="Empresas que recebem mais de 50% via CPF"
        )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_risk_distribution_pie(df_filtered),
            use_container_width=True,
            key="risk_pie"
        )

    with col2:
        st.plotly_chart(
            create_top_empresas_bar(df_filtered, 10),
            use_container_width=True,
            key="top_empresas"
        )

    # Scatter plot
    st.plotly_chart(
        create_scatter_cpf_vs_total(df_filtered),
        use_container_width=True,
        key="scatter"
    )

    # Top Municípios
    st.markdown("### 🏙️ Top Municípios por Volume")
    kpis_mun = calculate_kpis_by_municipio(df_filtered, 15)

    if not kpis_mun.empty:
        st.dataframe(
            kpis_mun.style.format({
                'volume_total': lambda x: format_currency(x),
                'volume_cpf': lambda x: format_currency(x),
                'score_medio': '{:.2f}'
            }),
            use_container_width=True
        )

# =============================================================================
# PÁGINA: RANKING DE EMPRESAS
# =============================================================================

def page_ranking_empresas():
    st.markdown("<h1 class='main-header'>🏆 Ranking de Empresas</h1>", unsafe_allow_html=True)

    # Busca
    col1, col2 = st.columns([3, 1])

    with col1:
        search_term = st.text_input(
            "🔍 Buscar por CNPJ ou Razão Social",
            placeholder="Digite para buscar..."
        )

    with col2:
        order_by = st.selectbox(
            "Ordenar por",
            ["Score de Risco", "Volume Total", "% CPF"]
        )

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        risk_filter = st.multiselect(
            "Classificação",
            ['ALTO', 'MÉDIO-ALTO', 'MÉDIO', 'BAIXO'],
            default=['ALTO', 'MÉDIO-ALTO']
        )

    with col2:
        if 'regime_tributario' in df_main.columns:
            regimes = df_main['regime_tributario'].dropna().unique().tolist()
            regime_filter = st.multiselect("Regime Tributário", regimes)
        else:
            regime_filter = None

    with col3:
        limit = st.number_input("Mostrar top", 10, 100, 50)

    # Aplicar filtros
    df_filtered = filter_data(
        df_main,
        classificacao=risk_filter if risk_filter else None,
        regime=regime_filter if regime_filter else None
    )

    # Aplicar busca
    if search_term:
        df_filtered = search_empresa(df_filtered, search_term)

    # Ordenar
    if order_by == "Score de Risco":
        df_display = df_filtered.nlargest(limit, 'score_risco_final')
    elif order_by == "Volume Total":
        df_display = df_filtered.nlargest(limit, 'total_geral')
    else:
        df_display = df_filtered.nlargest(limit, 'perc_recebido_cpf')

    # Exibir resultados
    st.markdown(f"### 📋 Resultados: {len(df_display)} empresas")

    if not df_display.empty:
        # Preparar colunas para exibição
        cols_display = [
            'cnpj', 'nm_razao_social', 'classificacao_risco',
            'score_risco_final', 'total_geral', 'perc_recebido_cpf',
            'qtd_socios_recebendo', 'municipio'
        ]

        cols_exist = [c for c in cols_display if c in df_display.columns]

        st.dataframe(
            df_display[cols_exist].style.format({
                'score_risco_final': '{:.2f}',
                'total_geral': lambda x: format_currency(x),
                'perc_recebido_cpf': '{:.2f}%'
            }),
            use_container_width=True,
            height=600
        )

        # Botão de download
        create_download_button(df_display[cols_exist], "📥 Baixar Ranking", "ranking_empresas.csv")
    else:
        st.info(MESSAGES['info']['no_results'])

# =============================================================================
# PÁGINA: MACHINE LEARNING
# =============================================================================

def page_machine_learning():
    st.markdown("<h1 class='main-header'>🤖 Machine Learning</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Modelo de Classificação", "⚠️ Detecção de Anomalias"])

    with tab1:
        st.markdown("### 🌲 Random Forest - Classificação de Risco")

        if st.button("🚀 Treinar Modelo", type="primary"):
            with st.spinner(MESSAGES['loading']['ml']):
                results = train_random_forest(df_main)

            if 'error' in results:
                st.error(f"Erro: {results['error']}")
            else:
                st.success(f"✅ Modelo treinado! Acurácia: {results['accuracy']*100:.2f}%")

                # Exibir métricas
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 📊 Importância das Features")
                    st.dataframe(
                        results['feature_importance'].style.format({'importance': '{:.4f}'}),
                        use_container_width=True
                    )

                with col2:
                    st.markdown("#### 📈 Matriz de Confusão")
                    st.write(results['confusion_matrix'])

                # Classification Report
                st.markdown("#### 📋 Relatório de Classificação")
                report_df = pd.DataFrame(results['classification_report']).T
                st.dataframe(report_df.style.format('{:.3f}'), use_container_width=True)

    with tab2:
        st.markdown("### 🔍 Isolation Forest - Detecção de Anomalias")

        if st.button("🎯 Detectar Anomalias", type="primary"):
            with st.spinner("Detectando anomalias..."):
                df_anomalies = detect_anomalies(df_main)

            anomalies = df_anomalies[df_anomalies['is_anomaly'] == True]

            st.success(f"✅ {len(anomalies)} anomalias detectadas!")

            if not anomalies.empty:
                cols = ['cnpj', 'nm_razao_social', 'score_risco_final',
                       'total_geral', 'perc_recebido_cpf', 'anomaly_score']

                cols_exist = [c for c in cols if c in anomalies.columns]

                st.dataframe(
                    anomalies[cols_exist].nlargest(50, 'score_risco_final'),
                    use_container_width=True,
                    height=500
                )

                create_download_button(anomalies[cols_exist], "📥 Baixar Anomalias", "anomalias.csv")

# =============================================================================
# PÁGINA: ESTATÍSTICAS AVANÇADAS
# =============================================================================

def page_estatisticas():
    st.markdown("<h1 class='main-header'>📊 Estatísticas Avançadas</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📈 Estatísticas Descritivas", "🔗 Correlações"])

    with tab1:
        st.markdown("### 📊 Estatísticas Descritivas")

        numeric_cols = ['score_risco_final', 'total_geral', 'perc_recebido_cpf',
                       'total_recebido_cpf', 'qtd_socios_recebendo']

        stats = calculate_descriptive_stats(df_main, numeric_cols)

        if not stats.empty:
            st.dataframe(
                stats.style.format('{:.2f}'),
                use_container_width=True
            )

        # Histogramas
        st.markdown("### 📊 Distribuições")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_histogram(df_main, 'score_risco_final', 'Distribuição de Score de Risco'),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                create_histogram(df_main, 'perc_recebido_cpf', 'Distribuição de % Recebido via CPF'),
                use_container_width=True
            )

    with tab2:
        st.markdown("### 🔗 Matriz de Correlação")

        corr_cols = ['score_risco_final', 'total_geral', 'perc_recebido_cpf',
                    'total_recebido_cpf', 'qtd_socios_recebendo',
                    'score_proporcao', 'score_volume_cpf']

        st.plotly_chart(
            create_correlation_heatmap(df_main, corr_cols),
            use_container_width=True
        )

        # Box plots por classificação
        if 'classificacao_risco' in df_main.columns:
            st.markdown("### 📦 Box Plot por Classificação de Risco")

            st.plotly_chart(
                create_box_plot(df_main, 'classificacao_risco', 'score_risco_final'),
                use_container_width=True
            )

# =============================================================================
# PÁGINA: DIAGNÓSTICO
# =============================================================================

def page_diagnostico():
    st.markdown("<h1 class='main-header'>🔧 Diagnóstico do Sistema</h1>", unsafe_allow_html=True)

    # Teste de conexão
    st.markdown("### 🔌 Status da Conexão")

    if st.button("🔄 Testar Conexão"):
        result = test_connection()

        if result['success']:
            st.success(f"✅ {result['message']}")
            st.json(result['details'])
        else:
            st.error(f"❌ {result['message']}")

    st.markdown("---")

    # Estatísticas dos dados
    st.markdown("### 📊 Estatísticas dos Dados Carregados")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Registros", format_number(len(df_main)))

    with col2:
        st.metric("Total de Colunas", len(df_main.columns))

    with col3:
        st.metric("Memória Utilizada", f"{df_main.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Informações das colunas
    st.markdown("### 📋 Informações das Colunas")

    col_info = pd.DataFrame({
        'Coluna': df_main.columns,
        'Tipo': df_main.dtypes.values,
        'Não-Nulos': df_main.count().values,
        '% Preenchimento': (df_main.count() / len(df_main) * 100).values
    })

    st.dataframe(
        col_info.style.format({'% Preenchimento': '{:.2f}%'}),
        use_container_width=True,
        height=400
    )

# =============================================================================
# ROTEAMENTO DE PÁGINAS
# =============================================================================

# Mapear páginas
pages_map = {
    f"{ICONS['dashboard']} Dashboard Executivo": page_dashboard_executivo,
    f"{ICONS['ranking']} Ranking de Empresas": page_ranking_empresas,
    f"{ICONS['ml']} Machine Learning": page_machine_learning,
    "📊 Estatísticas Avançadas": page_estatisticas,
    f"{ICONS['diagnostico']} Diagnóstico do Sistema": page_diagnostico,
}

# Executar página selecionada
if selected_page in pages_map:
    pages_map[selected_page]()
else:
    st.info("Página em desenvolvimento")

# =============================================================================
# RODAPÉ
# =============================================================================

st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: #999; padding: 20px;'>
        <p>
            <strong>{SYSTEM_INFO['name']}</strong><br>
            Versão {SYSTEM_INFO['version']} | {SYSTEM_INFO['organization']}<br>
            Desenvolvido por {SYSTEM_INFO['author']}
        </p>
    </div>
""", unsafe_allow_html=True)
