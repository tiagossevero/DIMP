"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    DIMP v2.0 - VERSÃO MONOLÍTICA                            ║
║          Dashboard de Inteligência de Meios de Pagamento                    ║
║                                                                              ║
║  Receita Estadual de Santa Catarina                                         ║
║  Desenvolvido por: Auditor Fiscal Tiago Severo                              ║
║  Versão: 2.0.0 Monolithic                                                   ║
║  Data: 2025-01-17                                                           ║
║                                                                              ║
║  ARQUIVO ÚNICO - PRONTO PARA DEPLOY                                         ║
║  Execute: streamlit run DIMP_v2_monolithic.py                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# =============================================================================
# IMPORTAÇÕES
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from typing import Dict, Any, List, Optional, Tuple, Union
import warnings
import ssl
import hashlib
import os
from io import BytesIO

# Machine Learning
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from scipy import stats

# Configuração SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURAÇÕES DA PÁGINA
# =============================================================================

PAGE_CONFIG = {
    "page_title": "DIMP - Análise de Meios de Pagamento",
    "page_icon": "💳",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

st.set_page_config(**PAGE_CONFIG)

# =============================================================================
# CONSTANTES E CONFIGURAÇÕES GLOBAIS
# =============================================================================

# Informações do Sistema
SYSTEM_INFO = {
    'name': 'DIMP - Dashboard de Inteligência de Meios de Pagamento',
    'version': '2.0.0 Monolithic',
    'author': 'Auditor Fiscal Tiago Severo',
    'organization': 'Receita Estadual de Santa Catarina',
    'release_date': '2025-01-17',
}

# Senha de Acesso (TROCAR EM PRODUÇÃO!)
DEFAULT_PASSWORD = "tsevero963"

def get_password():
    """Obtém senha de autenticação."""
    if hasattr(st, 'secrets') and 'auth' in st.secrets:
        return st.secrets['auth']['password']
    return os.getenv('DIMP_PASSWORD', DEFAULT_PASSWORD)

PASSWORD = get_password()

# Configurações Impala
IMPALA_CONFIG = {
    'host': 'bdaworkernode02.sef.sc.gov.br',
    'port': 21050,
    'database': 'teste',
    'auth_mechanism': 'LDAP',
    'use_ssl': True
}

# Credenciais Impala
def get_impala_credentials():
    """Obtém credenciais do Impala."""
    if hasattr(st, 'secrets') and 'impala_credentials' in st.secrets:
        return {
            'user': st.secrets['impala_credentials'].get('user', 'tsevero'),
            'password': st.secrets['impala_credentials'].get('password', '')
        }
    return {
        'user': os.getenv('IMPALA_USER', 'tsevero'),
        'password': os.getenv('IMPALA_PASSWORD', '')
    }

IMPALA_CREDENTIALS = get_impala_credentials()

# Tabelas do Sistema
TABLES = {
    'main': 'teste.dimp_score_final',
    'base': 'teste.dimp_cnpj_base',
    'socios': 'teste.dimp_socios',
    'pagamentos_cnpj': 'teste.dimp_pagamentos_cnpj',
    'pagamentos_cpf': 'teste.dimp_pagamentos_cpf',
    'operacoes_suspeitas': 'teste.dimp_operacoes_suspeitas',
    'socios_multiplos': 'teste.dimp_socios_multiplas_empresas'
}

# Cache TTL
CACHE_TTL = {
    'short': 600,
    'medium': 1800,
    'long': 3600,
    'extra_long': 7200
}

# Cores e Temas
COLOR_SCHEME = {
    'risco': {
        'ALTO': '#d32f2f',
        'MÉDIO-ALTO': '#f57c00',
        'MÉDIO': '#fbc02d',
        'BAIXO': '#388e3c'
    },
    'primary': '#1565c0',
    'secondary': '#2196f3',
}

# Configurações de ML
ML_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42,
        'class_weight': 'balanced',
        'min_samples_split': 5,
        'min_samples_leaf': 2
    },
    'isolation_forest': {
        'contamination': 0.1,
        'random_state': 42,
        'n_estimators': 100,
    },
    'test_size': 0.3,
    'features': ['perc_recebido_cpf', 'total_geral', 'qtd_socios_recebendo', 'score_risco_final'],
    'target': 'classificacao_risco'
}

# Ícones
ICONS = {
    'dashboard': '📊',
    'ranking': '🏆',
    'ml': '🤖',
    'stats': '📈',
    'diagnostico': '🔧',
}

# Mensagens
MESSAGES = {
    'loading': {
        'data': '⏳ Carregando dados do banco...',
        'ml': '🤖 Treinando modelos de Machine Learning...',
    },
    'error': {
        'no_data': '⚠️ Nenhum dado encontrado',
        'connection': '❌ Erro de conexão com o banco de dados',
    },
    'info': {
        'no_results': 'ℹ️ Nenhum resultado encontrado com os filtros aplicados',
    }
}

# =============================================================================
# ESTILOS CSS
# =============================================================================

CSS_STYLES = """
<style>
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

    .alert-critico {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 6px solid #c62828;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(198, 40, 40, 0.2);
    }

    .alert-alto {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 6px solid #ef6c00;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(239, 108, 0, 0.2);
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

    .stDataFrame {
        font-size: 0.9rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

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

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 2px solid #e0e0e0;
    }

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

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }

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
</style>
"""

st.markdown(CSS_STYLES, unsafe_allow_html=True)

# =============================================================================
# FUNÇÕES DE FORMATAÇÃO
# =============================================================================

def format_currency(value: Union[int, float], prefix: str = 'R$ ') -> str:
    """Formata valor como moeda brasileira."""
    if pd.isna(value):
        return 'R$ 0,00'
    return f"{prefix}{value:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

def format_percentage(value: Union[int, float], decimals: int = 2) -> str:
    """Formata valor como percentual."""
    if pd.isna(value):
        return '0,00%'
    return f"{value:.{decimals}f}%".replace('.', ',')

def format_number(value: Union[int, float], decimals: int = 0) -> str:
    """Formata número com separador de milhares."""
    if pd.isna(value):
        return '0'
    if decimals == 0:
        return f"{int(value):,}".replace(',', '.')
    return f"{value:,.{decimals}f}".replace(',', '_').replace('.', ',').replace('_', '.')

def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ com máscara."""
    cnpj_str = str(cnpj).zfill(14)
    return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:]}"

def get_risk_color(classificacao: str) -> str:
    """Retorna cor baseada na classificação de risco."""
    return COLOR_SCHEME['risco'].get(classificacao, '#757575')

def get_risk_emoji(classificacao: str) -> str:
    """Retorna emoji baseado na classificação de risco."""
    emojis = {
        'ALTO': '🔴',
        'MÉDIO-ALTO': '🟠',
        'MÉDIO': '🟡',
        'BAIXO': '🟢'
    }
    return emojis.get(classificacao, '⚪')

def export_to_csv(df: pd.DataFrame) -> bytes:
    """Exporta DataFrame para CSV."""
    return df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

def export_to_excel(df: pd.DataFrame) -> bytes:
    """Exporta DataFrame para Excel."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    return output.getvalue()

def create_download_button(df: pd.DataFrame, label: str = "📥 Baixar Dados",
                          filename: str = "dados.csv", file_format: str = 'csv') -> None:
    """Cria botão de download de dados."""
    if file_format == 'csv':
        data = export_to_csv(df)
        mime = 'text/csv'
    elif file_format == 'excel':
        data = export_to_excel(df)
        filename = filename.replace('.csv', '.xlsx')
        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        st.error("Formato não suportado")
        return

    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime
    )

# =============================================================================
# AUTENTICAÇÃO
# =============================================================================

def check_password() -> bool:
    """Sistema de autenticação com senha."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h1>🔐 Acesso Restrito - Sistema DIMP</h1>
                <p style='color: #666; margin-top: 20px;'>
                    Dashboard de Inteligência de Meios de Pagamento<br>
                    Receita Estadual de Santa Catarina
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            senha_input = st.text_input(
                "Digite a senha:",
                type="password",
                key="pwd_input",
                placeholder="Senha de acesso"
            )

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                if st.button("🔓 Entrar", use_container_width=True, type="primary"):
                    if senha_input == PASSWORD:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta")

            with col_btn2:
                if st.button("ℹ️ Ajuda", use_container_width=True):
                    st.info("Entre em contato com o administrador do sistema.")

        st.markdown(f"""
            <div style='text-align: center; margin-top: 50px; color: #999; font-size: 0.9rem;'>
                <p>{SYSTEM_INFO['author']}</p>
                <p>Versão {SYSTEM_INFO['version']} | © 2025 Receita Estadual SC</p>
            </div>
        """, unsafe_allow_html=True)

        st.stop()

    return True

# =============================================================================
# CONEXÃO COM BANCO DE DADOS
# =============================================================================

@st.cache_resource(show_spinner=False)
def get_engine():
    """Cria e retorna engine de conexão com Impala."""
    try:
        connection_string = (
            f"impala://{IMPALA_CONFIG['host']}:{IMPALA_CONFIG['port']}/"
            f"{IMPALA_CONFIG['database']}"
        )

        connect_args = {
            'user': IMPALA_CREDENTIALS['user'],
            'password': IMPALA_CREDENTIALS['password'],
            'auth_mechanism': IMPALA_CONFIG['auth_mechanism'],
        }

        if IMPALA_CONFIG.get('use_ssl'):
            connect_args['use_ssl'] = True

        engine = create_engine(
            connection_string,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

        return engine

    except Exception as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
        return None

def test_connection() -> dict:
    """Testa a conexão com o banco de dados."""
    result = {'success': False, 'message': '', 'details': {}}

    try:
        engine = get_engine()
        if engine is None:
            result['message'] = 'Engine não foi criado'
            return result

        with engine.connect() as conn:
            test_query = text("SELECT 1 as test")
            df = pd.read_sql(test_query, conn)

            if not df.empty and df.iloc[0]['test'] == 1:
                result['success'] = True
                result['message'] = 'Conexão estabelecida com sucesso'
                result['details'] = {
                    'host': IMPALA_CONFIG['host'],
                    'port': IMPALA_CONFIG['port'],
                    'database': IMPALA_CONFIG['database'],
                    'user': IMPALA_CREDENTIALS['user']
                }

    except Exception as e:
        result['message'] = f'Erro ao testar conexão: {str(e)}'

    return result

# =============================================================================
# FUNÇÕES DE CARREGAMENTO DE DADOS
# =============================================================================

@st.cache_data(ttl=CACHE_TTL['long'], show_spinner=False)
def load_main_data(_engine) -> pd.DataFrame:
    """Carrega dados principais da tabela dimp_score_final."""
    try:
        query = f"""
            SELECT *
            FROM {TABLES['main']}
            WHERE score_risco_final IS NOT NULL
                AND total_geral > 0
        """

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        # Conversões de tipos
        numeric_cols = [
            'score_risco_final', 'total_geral', 'total_recebido_cpf',
            'total_recebido_cnpj', 'perc_recebido_cpf', 'perc_recebido_cnpj',
            'qtd_socios_recebendo', 'score_proporcao', 'score_volume_cpf',
            'score_qtd_socios', 'score_desvio_regime', 'score_consistencia'
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados principais: {str(e)}")
        return pd.DataFrame()

def filter_data(
    df: pd.DataFrame,
    classificacao: Optional[List[str]] = None,
    regime: Optional[List[str]] = None,
    municipio: Optional[List[str]] = None,
    uf: Optional[List[str]] = None,
    score_min: Optional[float] = None,
    score_max: Optional[float] = None,
    perc_cpf_min: Optional[float] = None,
    valor_min: Optional[float] = None
) -> pd.DataFrame:
    """Aplica filtros ao DataFrame."""
    df_filtered = df.copy()

    if classificacao and 'classificacao_risco' in df.columns:
        df_filtered = df_filtered[df_filtered['classificacao_risco'].isin(classificacao)]

    if regime and 'regime_tributario' in df.columns:
        df_filtered = df_filtered[df_filtered['regime_tributario'].isin(regime)]

    if municipio and 'municipio' in df.columns:
        df_filtered = df_filtered[df_filtered['municipio'].isin(municipio)]

    if uf and 'uf' in df.columns:
        df_filtered = df_filtered[df_filtered['uf'].isin(uf)]

    if score_min is not None and 'score_risco_final' in df.columns:
        df_filtered = df_filtered[df_filtered['score_risco_final'] >= score_min]

    if score_max is not None and 'score_risco_final' in df.columns:
        df_filtered = df_filtered[df_filtered['score_risco_final'] <= score_max]

    if perc_cpf_min is not None and 'perc_recebido_cpf' in df.columns:
        df_filtered = df_filtered[df_filtered['perc_recebido_cpf'] >= perc_cpf_min]

    if valor_min is not None and 'total_geral' in df.columns:
        df_filtered = df_filtered[df_filtered['total_geral'] >= valor_min]

    return df_filtered

def search_empresa(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Busca empresa por CNPJ ou razão social."""
    if not search_term:
        return df

    search_term = search_term.upper().strip()
    mask = pd.Series([False] * len(df), index=df.index)

    if 'cnpj' in df.columns:
        mask |= df['cnpj'].astype(str).str.contains(search_term, na=False, regex=False)

    if 'nm_razao_social' in df.columns:
        mask |= df['nm_razao_social'].astype(str).str.upper().str.contains(
            search_term, na=False, regex=False
        )

    return df[mask]

# =============================================================================
# FUNÇÕES DE ANÁLISE E KPIs
# =============================================================================

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula KPIs principais do dashboard."""
    if df.empty:
        return {k: 0 for k in [
            'total_empresas', 'volume_total', 'volume_cpf', 'volume_cnpj',
            'media_score_risco', 'media_perc_cpf', 'empresas_alto_risco',
            'empresas_medio_alto', 'perc_alto_risco', 'perc_medio_alto',
            'empresas_alerta_critico', 'empresas_acima_50pct_cpf', 'perc_total_cpf'
        ]}

    kpis = {
        'total_empresas': len(df),
        'volume_total': df['total_geral'].sum() if 'total_geral' in df.columns else 0,
        'volume_cpf': df['total_recebido_cpf'].sum() if 'total_recebido_cpf' in df.columns else 0,
        'volume_cnpj': df['total_recebido_cnpj'].sum() if 'total_recebido_cnpj' in df.columns else 0,
        'media_score_risco': df['score_risco_final'].mean() if 'score_risco_final' in df.columns else 0,
        'media_perc_cpf': df['perc_recebido_cpf'].mean() if 'perc_recebido_cpf' in df.columns else 0,
        'empresas_alto_risco': len(df[df['classificacao_risco'] == 'ALTO']) if 'classificacao_risco' in df.columns else 0,
        'empresas_medio_alto': len(df[df['classificacao_risco'] == 'MÉDIO-ALTO']) if 'classificacao_risco' in df.columns else 0,
    }

    if len(df) > 0:
        kpis['perc_alto_risco'] = (kpis['empresas_alto_risco'] / len(df) * 100) if 'classificacao_risco' in df.columns else 0
        kpis['perc_medio_alto'] = (kpis['empresas_medio_alto'] / len(df) * 100) if 'classificacao_risco' in df.columns else 0

    kpis['empresas_alerta_critico'] = len(df[(df['score_risco_final'] >= 90)]) if 'score_risco_final' in df.columns else 0
    kpis['empresas_acima_50pct_cpf'] = len(df[(df['perc_recebido_cpf'] > 50)]) if 'perc_recebido_cpf' in df.columns else 0

    if kpis['volume_total'] > 0:
        kpis['perc_total_cpf'] = (kpis['volume_cpf'] / kpis['volume_total']) * 100
    else:
        kpis['perc_total_cpf'] = 0

    return kpis

def calculate_kpis_by_municipio(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Calcula KPIs agrupados por município."""
    if df.empty or 'municipio' not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby('municipio').agg({
        'cnpj': 'count',
        'total_geral': 'sum',
        'total_recebido_cpf': 'sum',
        'score_risco_final': 'mean'
    }).reset_index()

    grouped.columns = ['municipio', 'qtd_empresas', 'volume_total', 'volume_cpf', 'score_medio']
    grouped = grouped.sort_values('volume_total', ascending=False).head(top_n)

    return grouped

def calculate_descriptive_stats(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Calcula estatísticas descritivas para múltiplas colunas."""
    if df.empty:
        return pd.DataFrame()

    stats_dict = {}

    for col in columns:
        if col not in df.columns:
            continue

        series = df[col].dropna()
        if len(series) == 0:
            continue

        stats_dict[col] = {
            'count': len(series),
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max(),
            'q25': series.quantile(0.25),
            'q75': series.quantile(0.75),
            'q90': series.quantile(0.90),
            'q95': series.quantile(0.95),
        }

    return pd.DataFrame(stats_dict).T

def calculate_correlation_matrix(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Calcula matriz de correlação."""
    if df.empty:
        return pd.DataFrame()

    valid_cols = [col for col in columns if col in df.columns]
    if not valid_cols:
        return pd.DataFrame()

    return df[valid_cols].corr()

# =============================================================================
# FUNÇÕES DE MACHINE LEARNING
# =============================================================================

def prepare_ml_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepara dados para ML."""
    if df.empty:
        return pd.DataFrame(), pd.Series()

    features = [f for f in ML_CONFIG['features'] if f in df.columns]
    target = ML_CONFIG['target']

    if not features or target not in df.columns:
        return pd.DataFrame(), pd.Series()

    df_clean = df[features + [target]].dropna()
    X = df_clean[features]
    y = df_clean[target]

    return X, y

def train_random_forest(df: pd.DataFrame) -> Dict[str, Any]:
    """Treina modelo Random Forest."""
    X, y = prepare_ml_data(df)

    if X.empty or y.empty:
        return {'error': 'Dados insuficientes'}

    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Split dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=ML_CONFIG['test_size'],
        random_state=ML_CONFIG['random_forest']['random_state'],
        stratify=y_encoded
    )

    # Treinar modelo
    rf = RandomForestClassifier(**ML_CONFIG['random_forest'])
    rf.fit(X_train, y_train)

    # Predições
    y_pred = rf.predict(X_test)

    # Métricas
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(
        y_test, y_pred,
        target_names=le.classes_,
        output_dict=True
    )

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'model': rf,
        'label_encoder': le,
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix,
        'classification_report': class_report,
        'feature_importance': feature_importance,
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_pred
    }

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Detecta anomalias com Isolation Forest."""
    features = [f for f in ML_CONFIG['features'][:-1] if f in df.columns]

    if not features:
        return df

    df_clean = df[features].dropna()
    if df_clean.empty:
        return df

    # Normalizar dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)

    # Treinar Isolation Forest
    iso_forest = IsolationForest(**ML_CONFIG['isolation_forest'])
    predictions = iso_forest.fit_predict(X_scaled)
    scores = iso_forest.score_samples(X_scaled)

    # Adicionar resultados
    df_result = df.copy()
    df_result['anomaly'] = 0
    df_result['anomaly_score'] = 0.0
    df_result.loc[df_clean.index, 'anomaly'] = predictions
    df_result.loc[df_clean.index, 'anomaly_score'] = scores
    df_result['is_anomaly'] = df_result['anomaly'] == -1

    return df_result

# =============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# =============================================================================

def create_risk_distribution_pie(df: pd.DataFrame) -> go.Figure:
    """Gráfico de pizza - distribuição de risco."""
    if df.empty or 'classificacao_risco' not in df.columns:
        return go.Figure()

    dist = df['classificacao_risco'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=dist.index,
        values=dist.values,
        hole=0.4,
        marker=dict(colors=[COLOR_SCHEME['risco'].get(x, '#999') for x in dist.index]),
        textinfo='label+percent',
        textfont=dict(size=14)
    )])

    fig.update_layout(
        title='Distribuição de Risco',
        height=400,
        showlegend=True
    )

    return fig

def create_top_empresas_bar(df: pd.DataFrame, n: int = 10) -> go.Figure:
    """Gráfico de barras - top empresas."""
    if df.empty:
        return go.Figure()

    top = df.nlargest(n, 'score_risco_final')

    fig = go.Figure(data=[
        go.Bar(
            x=top['score_risco_final'],
            y=top['nm_razao_social'] if 'nm_razao_social' in top.columns else top['cnpj'],
            orientation='h',
            marker=dict(
                color=top['score_risco_final'],
                colorscale='Reds',
                showscale=True
            ),
            text=top['score_risco_final'].round(2),
            textposition='auto'
        )
    ])

    fig.update_layout(
        title=f'Top {n} Empresas por Score de Risco',
        xaxis_title='Score de Risco',
        yaxis_title='Empresa',
        height=500,
        showlegend=False
    )

    return fig

def create_scatter_cpf_vs_total(df: pd.DataFrame) -> go.Figure:
    """Gráfico de dispersão - CPF vs Total."""
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x='total_geral',
        y='perc_recebido_cpf',
        color='classificacao_risco',
        size='score_risco_final',
        hover_data=['nm_razao_social', 'cnpj'] if 'nm_razao_social' in df.columns else ['cnpj'],
        color_discrete_map=COLOR_SCHEME['risco'],
        title='Relação entre Volume Total e % Recebido via CPF'
    )

    fig.update_layout(height=500)
    return fig

def create_histogram(df: pd.DataFrame, column: str, title: str = None) -> go.Figure:
    """Histograma de distribuição."""
    if df.empty or column not in df.columns:
        return go.Figure()

    fig = go.Figure(data=[
        go.Histogram(
            x=df[column],
            nbinsx=50,
            marker=dict(color='#1976d2'),
            opacity=0.75
        )
    ])

    fig.update_layout(
        title=title or f'Distribuição de {column}',
        xaxis_title=column,
        yaxis_title='Frequência',
        height=400
    )

    return fig

def create_correlation_heatmap(df: pd.DataFrame, columns: list) -> go.Figure:
    """Mapa de calor de correlação."""
    if df.empty:
        return go.Figure()

    valid_cols = [col for col in columns if col in df.columns]
    if not valid_cols:
        return go.Figure()

    corr = df[valid_cols].corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr.values.round(2),
        texttemplate='%{text}',
        textfont=dict(size=10)
    ))

    fig.update_layout(
        title='Matriz de Correlação',
        height=600,
        width=700
    )

    return fig

def create_box_plot(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """Box plot para comparação."""
    if df.empty:
        return go.Figure()

    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        title=f'Distribuição de {y_col} por {x_col}'
    )

    fig.update_layout(height=500)
    return fig

# =============================================================================
# PÁGINAS DO DASHBOARD
# =============================================================================

def page_dashboard_executivo(df_main):
    """Página: Dashboard Executivo."""
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

def page_ranking_empresas(df_main):
    """Página: Ranking de Empresas."""
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

        create_download_button(df_display[cols_exist], "📥 Baixar Ranking", "ranking_empresas.csv")
    else:
        st.info(MESSAGES['info']['no_results'])

def page_machine_learning(df_main):
    """Página: Machine Learning."""
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

def page_estatisticas(df_main):
    """Página: Estatísticas Avançadas."""
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

        if 'classificacao_risco' in df_main.columns:
            st.markdown("### 📦 Box Plot por Classificação de Risco")
            st.plotly_chart(
                create_box_plot(df_main, 'classificacao_risco', 'score_risco_final'),
                use_container_width=True
            )

def page_diagnostico():
    """Página: Diagnóstico do Sistema."""
    st.markdown("<h1 class='main-header'>🔧 Diagnóstico do Sistema</h1>", unsafe_allow_html=True)

    st.markdown("### 🔌 Status da Conexão")

    if st.button("🔄 Testar Conexão"):
        result = test_connection()

        if result['success']:
            st.success(f"✅ {result['message']}")
            st.json(result['details'])
        else:
            st.error(f"❌ {result['message']}")

    st.markdown("---")

    st.markdown("### 📊 Estatísticas dos Dados Carregados")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Registros", format_number(len(df_main)))

    with col2:
        st.metric("Total de Colunas", len(df_main.columns))

    with col3:
        st.metric("Memória Utilizada", f"{df_main.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

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
# APLICAÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal da aplicação."""

    # Autenticação
    check_password()

    # Sidebar
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
        pages = {
            f"{ICONS['dashboard']} Dashboard Executivo": "dashboard",
            f"{ICONS['ranking']} Ranking de Empresas": "ranking",
            f"{ICONS['ml']} Machine Learning": "ml",
            f"{ICONS['stats']} Estatísticas Avançadas": "stats",
            f"{ICONS['diagnostico']} Diagnóstico": "diagnostico",
        }

        selected_page_name = st.radio(
            "Selecione a página:",
            list(pages.keys()),
            label_visibility="collapsed"
        )

        selected_page = pages[selected_page_name]

        st.markdown("---")

        # Informações do sistema
        with st.expander("ℹ️ Informações do Sistema"):
            st.markdown(f"""
                **Versão:** {SYSTEM_INFO['version']}
                **Autor:** {SYSTEM_INFO['author']}
                **Organização:** {SYSTEM_INFO['organization']}
            """)

    # Carregamento de dados
    @st.cache_data(ttl=CACHE_TTL['long'], show_spinner=False)
    def load_all_data():
        engine = get_engine()
        if engine is None:
            return None
        with st.spinner(MESSAGES['loading']['data']):
            df = load_main_data(engine)
        return df

    df_main = load_all_data()

    if df_main is None or df_main.empty:
        st.error(MESSAGES['error']['no_data'])
        st.stop()

    # Roteamento de páginas
    if selected_page == "dashboard":
        page_dashboard_executivo(df_main)
    elif selected_page == "ranking":
        page_ranking_empresas(df_main)
    elif selected_page == "ml":
        page_machine_learning(df_main)
    elif selected_page == "stats":
        page_estatisticas(df_main)
    elif selected_page == "diagnostico":
        page_diagnostico()

    # Rodapé
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

# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()
