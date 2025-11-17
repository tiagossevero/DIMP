"""
Gerenciamento de Conexões com Banco de Dados
"""

import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import ssl
from typing import Optional
import warnings

from ..config.settings import IMPALA_CONFIG, IMPALA_CREDENTIALS, TABLES

warnings.filterwarnings('ignore')

# Configuração SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


@st.cache_resource(show_spinner=False)
def get_engine():
    """
    Cria e retorna engine de conexão com Impala.
    Usa cache para evitar múltiplas conexões.

    Returns:
        SQLAlchemy Engine ou None em caso de erro
    """
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
            pool_pre_ping=True,  # Verifica conexões antes de usar
            pool_recycle=3600,   # Recicla conexões após 1 hora
        )

        return engine

    except Exception as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
        return None


def test_connection() -> dict:
    """
    Testa a conexão com o banco de dados.

    Returns:
        dict: Dicionário com status e informações da conexão
    """
    result = {
        'success': False,
        'message': '',
        'details': {}
    }

    try:
        engine = get_engine()

        if engine is None:
            result['message'] = 'Engine não foi criado'
            return result

        # Testa query simples
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
        result['details'] = {'error': str(e)}

    return result


def verify_tables() -> dict:
    """
    Verifica a existência das tabelas necessárias.

    Returns:
        dict: Dicionário com status de cada tabela
    """
    engine = get_engine()
    if engine is None:
        return {}

    tables_status = {}

    for table_name, table_full_name in TABLES.items():
        try:
            query = f"SELECT COUNT(*) as cnt FROM {table_full_name} LIMIT 1"
            with engine.connect() as conn:
                df = pd.read_sql(text(query), conn)
                tables_status[table_name] = {
                    'exists': True,
                    'accessible': True,
                    'full_name': table_full_name
                }
        except Exception as e:
            tables_status[table_name] = {
                'exists': False,
                'accessible': False,
                'error': str(e)[:100],
                'full_name': table_full_name
            }

    return tables_status


@st.cache_data(ttl=3600, show_spinner=False)
def get_table_columns(_engine, table_name: str) -> list:
    """
    Obtém lista de colunas de uma tabela.

    Args:
        _engine: SQLAlchemy engine
        table_name: Nome completo da tabela

    Returns:
        list: Lista de nomes de colunas
    """
    try:
        query = f"DESCRIBE {table_name}"
        df = pd.read_sql(text(query), _engine)
        return df.iloc[:, 0].tolist() if not df.empty else []
    except Exception as e:
        st.warning(f"Erro ao obter colunas de {table_name}: {str(e)[:50]}")
        return []


@st.cache_data(ttl=7200, show_spinner=False)
def get_table_stats(_engine, table_name: str) -> dict:
    """
    Obtém estatísticas básicas de uma tabela.

    Args:
        _engine: SQLAlchemy engine
        table_name: Nome completo da tabela

    Returns:
        dict: Estatísticas da tabela
    """
    stats = {
        'total_rows': 0,
        'sample_data': None,
        'columns': []
    }

    try:
        # Total de linhas
        count_query = f"SELECT COUNT(*) as total FROM {table_name}"
        with _engine.connect() as conn:
            df_count = pd.read_sql(text(count_query), conn)
            stats['total_rows'] = int(df_count.iloc[0]['total']) if not df_count.empty else 0

        # Colunas
        stats['columns'] = get_table_columns(_engine, table_name)

        # Amostra de dados
        sample_query = f"SELECT * FROM {table_name} LIMIT 5"
        with _engine.connect() as conn:
            stats['sample_data'] = pd.read_sql(text(sample_query), conn)

    except Exception as e:
        st.warning(f"Erro ao obter estatísticas: {str(e)[:100]}")

    return stats
