"""
Configurações Globais do Sistema DIMP
Dashboard de Inteligência de Meios de Pagamento
Receita Estadual de Santa Catarina
"""

import streamlit as st
from typing import Dict, Any
import os

# =============================================================================
# CONFIGURAÇÕES DE PÁGINA
# =============================================================================

PAGE_CONFIG = {
    "page_title": "DIMP - Análise de Meios de Pagamento",
    "page_icon": "💳",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://www.sef.sc.gov.br',
        'Report a bug': None,
        'About': "# DIMP - Dashboard de Inteligência de Meios de Pagamento\nReceita Estadual de Santa Catarina\nVersão 2.0"
    }
}

# =============================================================================
# AUTENTICAÇÃO
# =============================================================================

# Senha padrão (TROCAR EM PRODUÇÃO!)
DEFAULT_PASSWORD = "tsevero963"

# Obter senha de variável de ambiente ou secrets
def get_password():
    """Obtém senha de autenticação."""
    if hasattr(st, 'secrets') and 'auth' in st.secrets:
        return st.secrets['auth']['password']
    return os.getenv('DIMP_PASSWORD', DEFAULT_PASSWORD)

PASSWORD = get_password()

# =============================================================================
# BANCO DE DADOS - IMPALA
# =============================================================================

# Configurações de conexão Impala
IMPALA_CONFIG = {
    'host': 'bdaworkernode02.sef.sc.gov.br',
    'port': 21050,
    'database': 'teste',
    'auth_mechanism': 'LDAP',
    'use_ssl': True
}

# Credenciais (priorizar secrets do Streamlit)
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

# Tabelas do sistema
TABLES = {
    'main': 'teste.dimp_score_final',
    'base': 'teste.dimp_cnpj_base',
    'socios': 'teste.dimp_socios',
    'pagamentos_cnpj': 'teste.dimp_pagamentos_cnpj',
    'pagamentos_cpf': 'teste.dimp_pagamentos_cpf',
    'operacoes_suspeitas': 'teste.dimp_operacoes_suspeitas',
    'socios_multiplos': 'teste.dimp_socios_multiplas_empresas'
}

# =============================================================================
# CACHE E PERFORMANCE
# =============================================================================

CACHE_CONFIG = {
    'ttl_short': 600,      # 10 minutos
    'ttl_medium': 1800,    # 30 minutos
    'ttl_long': 3600,      # 1 hora
    'ttl_extra_long': 7200 # 2 horas
}

# =============================================================================
# FILTROS E LIMITES
# =============================================================================

FILTERS_CONFIG = {
    'classificacao_risco': ['ALTO', 'MÉDIO-ALTO', 'MÉDIO', 'BAIXO'],
    'max_empresas_display': 1000,
    'min_score_risco': 0,
    'max_score_risco': 100
}

# =============================================================================
# CORES E TEMAS
# =============================================================================

COLOR_SCHEME = {
    'primary': '#1565c0',
    'secondary': '#2196f3',
    'success': '#4caf50',
    'warning': '#ff9800',
    'danger': '#f44336',
    'info': '#00bcd4',
    'dark': '#263238',
    'light': '#eceff1',

    # Cores por classificação de risco
    'risco': {
        'ALTO': '#d32f2f',
        'MÉDIO-ALTO': '#f57c00',
        'MÉDIO': '#fbc02d',
        'BAIXO': '#388e3c'
    },

    # Paleta para gráficos
    'chart_palette': [
        '#1976d2', '#388e3c', '#f57c00', '#d32f2f',
        '#7b1fa2', '#0097a7', '#c2185b', '#5d4037'
    ]
}

# =============================================================================
# MACHINE LEARNING
# =============================================================================

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
        'max_samples': 'auto'
    },
    'test_size': 0.3,
    'features': [
        'perc_recebido_cpf',
        'total_geral',
        'qtd_socios_recebendo',
        'score_risco_final'
    ],
    'target': 'classificacao_risco'
}

# =============================================================================
# FORMATAÇÃO
# =============================================================================

FORMAT_CONFIG = {
    'moeda': {
        'prefix': 'R$ ',
        'decimal_sep': ',',
        'thousands_sep': '.',
        'decimals': 2
    },
    'percentual': {
        'suffix': '%',
        'decimals': 2
    },
    'numero': {
        'thousands_sep': '.',
        'decimals': 0
    }
}

# =============================================================================
# ANÁLISES AVANÇADAS
# =============================================================================

ANALYTICS_CONFIG = {
    'percentis': [0.25, 0.50, 0.75, 0.90, 0.95, 0.99],
    'correlacao_min': 0.3,
    'outlier_threshold': 3,  # Desvios padrão
    'min_empresas_setor': 3,
    'min_transacoes_temporal': 3
}

# =============================================================================
# EXPORTAÇÃO
# =============================================================================

EXPORT_CONFIG = {
    'formatos': ['CSV', 'Excel', 'JSON'],
    'max_rows_export': 100000,
    'encoding': 'utf-8-sig'
}

# =============================================================================
# VERSÃO DO SISTEMA
# =============================================================================

SYSTEM_INFO = {
    'name': 'DIMP - Dashboard de Inteligência de Meios de Pagamento',
    'version': '2.0.0',
    'author': 'Auditor Fiscal Tiago Severo',
    'organization': 'Receita Estadual de Santa Catarina',
    'release_date': '2025-01-17',
    'description': 'Sistema avançado de análise fiscal para detecção de irregularidades em meios de pagamento'
}
