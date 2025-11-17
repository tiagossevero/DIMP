"""
Constantes do Sistema DIMP
"""

# =============================================================================
# ESTILOS CSS
# =============================================================================

CSS_STYLES = """
<style>
    /* ======== HEADER PRINCIPAL ======== */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1565c0;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ======== MÉTRICAS/KPIs ======== */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #2c3e50;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }

    div[data-testid="stMetric"] > label {
        font-weight: 600;
        color: #2c3e50;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1565c0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* ======== CARDS CUSTOMIZADOS ======== */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 10px 0;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }

    .metric-card h3 {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
        opacity: 0.9;
    }

    .metric-card .value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 10px 0;
    }

    /* ======== ALERTAS ======== */
    .alert-critico {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 6px solid #c62828;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(198, 40, 40, 0.2);
        animation: pulse-red 2s infinite;
    }

    .alert-alto {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 6px solid #ef6c00;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(239, 108, 0, 0.2);
    }

    .alert-medio {
        background: linear-gradient(135deg, #fffde7 0%, #fff9c4 100%);
        border-left: 6px solid #f57f17;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(245, 127, 23, 0.2);
    }

    .alert-positivo {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 6px solid #2e7d32;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(46, 125, 50, 0.2);
    }

    .alert-info {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 6px solid #1976d2;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.2);
    }

    /* ======== INFO BOXES ======== */
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #f57c00;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #388e3c;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* ======== TABELAS ======== */
    .stDataFrame {
        font-size: 0.9rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .stDataFrame thead tr th {
        background-color: #1565c0 !important;
        color: white !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }

    .stDataFrame tbody tr:hover {
        background-color: #f5f5f5;
        transition: background-color 0.3s ease;
    }

    /* ======== BOTÕES ======== */
    .stButton > button {
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* ======== SIDEBAR ======== */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 2px solid #e0e0e0;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* ======== TABS ======== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e0e0;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }

    /* ======== EXPANDERS ======== */
    .streamlit-expanderHeader {
        background-color: #f5f5f5;
        border-radius: 8px;
        font-weight: 600;
        color: #2c3e50;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background-color: #e0e0e0;
    }

    /* ======== ANIMAÇÕES ======== */
    @keyframes pulse-red {
        0%, 100% {
            box-shadow: 0 4px 8px rgba(198, 40, 40, 0.2);
        }
        50% {
            box-shadow: 0 4px 16px rgba(198, 40, 40, 0.4);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }

    /* ======== SCROLLBAR ======== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* ======== CONTAINERS ======== */
    .stContainer {
        border-radius: 10px;
        padding: 20px;
    }

    .plot-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 15px 0;
    }

    /* ======== RESPONSIVIDADE ======== */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }

        .metric-card .value {
            font-size: 2rem;
        }
    }
</style>
"""

# =============================================================================
# MENSAGENS E TEXTOS
# =============================================================================

MESSAGES = {
    'loading': {
        'data': '⏳ Carregando dados do banco...',
        'analysis': '📊 Executando análises...',
        'ml': '🤖 Treinando modelos de Machine Learning...',
        'viz': '📈 Gerando visualizações...'
    },
    'success': {
        'data_loaded': '✅ Dados carregados com sucesso!',
        'analysis_complete': '✅ Análise concluída!',
        'export_complete': '✅ Exportação realizada com sucesso!'
    },
    'error': {
        'connection': '❌ Erro de conexão com o banco de dados',
        'no_data': '⚠️ Nenhum dado encontrado',
        'invalid_filter': '⚠️ Filtros inválidos'
    },
    'info': {
        'select_empresa': 'ℹ️ Selecione uma empresa para ver detalhes',
        'no_results': 'ℹ️ Nenhum resultado encontrado com os filtros aplicados',
        'loading_first_time': 'ℹ️ Primeira carga pode levar alguns minutos...'
    }
}

# =============================================================================
# ÍCONES
# =============================================================================

ICONS = {
    'dashboard': '📊',
    'ranking': '🏆',
    'empresa': '🏢',
    'ml': '🤖',
    'setor': '🏭',
    'funcionarios': '👥',
    'socios': '🔗',
    'temporal': '📈',
    'suspeitos': '⚠️',
    'geo': '🗺️',
    'comparacao': '⚖️',
    'rede': '🕸️',
    'diagnostico': '🔧',
    'sobre': 'ℹ️',
    'filtro': '🔍',
    'export': '📥',
    'alert': '🚨',
    'check': '✅',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
    'money': '💰',
    'percent': '📊',
    'trend_up': '📈',
    'trend_down': '📉',
    'target': '🎯'
}

# =============================================================================
# PÁGINAS DO DASHBOARD
# =============================================================================

PAGES = [
    {
        'id': 'dashboard',
        'name': '📊 Dashboard Executivo',
        'description': 'Visão geral e KPIs principais'
    },
    {
        'id': 'ranking',
        'name': '🏆 Ranking de Empresas',
        'description': 'Top empresas por risco'
    },
    {
        'id': 'drill_down',
        'name': '🏢 Análise Detalhada',
        'description': 'Drill-down por empresa'
    },
    {
        'id': 'comparacao',
        'name': '⚖️ Comparação Avançada',
        'description': 'Compare empresas e setores'
    },
    {
        'id': 'geografica',
        'name': '🗺️ Análise Geográfica',
        'description': 'Mapas e distribuição regional'
    },
    {
        'id': 'setorial',
        'name': '🏭 Análise Setorial',
        'description': 'Análise por CNAE e atividade'
    },
    {
        'id': 'temporal',
        'name': '📈 Análise Temporal',
        'description': 'Evolução e tendências'
    },
    {
        'id': 'rede',
        'name': '🕸️ Rede de Relacionamentos',
        'description': 'Sócios e grupos empresariais'
    },
    {
        'id': 'funcionarios',
        'name': '👥 Análise de Funcionários',
        'description': 'Pagamentos a funcionários'
    },
    {
        'id': 'ml',
        'name': '🤖 Machine Learning',
        'description': 'Modelos preditivos e anomalias'
    },
    {
        'id': 'padroes',
        'name': '⚠️ Padrões Suspeitos',
        'description': 'Detecção de irregularidades'
    },
    {
        'id': 'estatisticas',
        'name': '📊 Estatísticas Avançadas',
        'description': 'Análises estatísticas detalhadas'
    },
    {
        'id': 'diagnostico',
        'name': '🔧 Diagnóstico do Sistema',
        'description': 'Status e configurações'
    },
    {
        'id': 'sobre',
        'name': 'ℹ️ Sobre o Sistema',
        'description': 'Informações e documentação'
    }
]

# =============================================================================
# TOOLTIPS E AJUDA
# =============================================================================

TOOLTIPS = {
    'score_risco': 'Score de 0-100 calculado com base em múltiplos indicadores',
    'perc_cpf': 'Percentual do total recebido via CPF de sócios',
    'classificacao_risco': 'ALTO (≥80), MÉDIO-ALTO (60-79), MÉDIO (40-59), BAIXO (<40)',
    'qtd_socios': 'Quantidade de sócios que receberam pagamentos via CPF',
    'total_geral': 'Soma de todos os pagamentos (CNPJ + CPF)',
    'anomalia': 'Empresa com comportamento estatisticamente atípico'
}

# =============================================================================
# QUERIES SQL PREDEFINIDAS
# =============================================================================

SQL_QUERIES = {
    'top_empresas': """
        SELECT * FROM {table}
        WHERE score_risco_final IS NOT NULL
        ORDER BY score_risco_final DESC
        LIMIT {limit}
    """,
    'estatisticas_gerais': """
        SELECT
            COUNT(*) as total_empresas,
            AVG(score_risco_final) as media_score,
            SUM(total_geral) as volume_total
        FROM {table}
    """,
    'distribuicao_risco': """
        SELECT
            classificacao_risco,
            COUNT(*) as qtd,
            SUM(total_geral) as volume
        FROM {table}
        GROUP BY classificacao_risco
    """
}
