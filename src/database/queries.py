"""
Queries e Funções de Carregamento de Dados
"""

import streamlit as st
import pandas as pd
from sqlalchemy import text
from typing import Optional, List, Dict, Any

from ..config.settings import TABLES, CACHE_CONFIG
from .connection import get_engine


@st.cache_data(ttl=CACHE_CONFIG['ttl_long'], show_spinner="⏳ Carregando dados principais...")
def load_main_data(_engine) -> pd.DataFrame:
    """
    Carrega dados principais da tabela dimp_score_final.

    Args:
        _engine: SQLAlchemy engine

    Returns:
        pd.DataFrame: Dados principais
    """
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


@st.cache_data(ttl=CACHE_CONFIG['ttl_medium'], show_spinner="⏳ Carregando sócios...")
def load_socios_data(_engine, cnpj: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega dados de sócios.

    Args:
        _engine: SQLAlchemy engine
        cnpj: CNPJ específico (opcional)

    Returns:
        pd.DataFrame: Dados de sócios
    """
    try:
        query = f"SELECT * FROM {TABLES['socios']}"

        if cnpj:
            query += f" WHERE cnpj = '{cnpj}'"

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        return df

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar sócios: {str(e)[:100]}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_CONFIG['ttl_medium'], show_spinner="⏳ Carregando pagamentos...")
def load_pagamentos_cpf(_engine, cnpj: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega pagamentos recebidos via CPF.

    Args:
        _engine: SQLAlchemy engine
        cnpj: CNPJ específico (opcional)

    Returns:
        pd.DataFrame: Dados de pagamentos CPF
    """
    try:
        query = f"SELECT * FROM {TABLES['pagamentos_cpf']}"

        if cnpj:
            query += f" WHERE cnpj = '{cnpj}'"

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        # Converter colunas de valor para numérico
        valor_cols = [col for col in df.columns if col.startswith('vl_')]
        for col in valor_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar pagamentos CPF: {str(e)[:100]}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_CONFIG['ttl_medium'], show_spinner="⏳ Carregando pagamentos CNPJ...")
def load_pagamentos_cnpj(_engine, cnpj: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega pagamentos recebidos via CNPJ.

    Args:
        _engine: SQLAlchemy engine
        cnpj: CNPJ específico (opcional)

    Returns:
        pd.DataFrame: Dados de pagamentos CNPJ
    """
    try:
        query = f"SELECT * FROM {TABLES['pagamentos_cnpj']}"

        if cnpj:
            query += f" WHERE cnpj = '{cnpj}'"

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        # Converter colunas de valor para numérico
        valor_cols = [col for col in df.columns if col.startswith('vl_')]
        for col in valor_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar pagamentos CNPJ: {str(e)[:100]}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_CONFIG['ttl_long'], show_spinner="⏳ Carregando sócios múltiplos...")
def load_socios_multiplos(_engine) -> pd.DataFrame:
    """
    Carrega dados de sócios com participação em múltiplas empresas.

    Args:
        _engine: SQLAlchemy engine

    Returns:
        pd.DataFrame: Dados de sócios múltiplos
    """
    try:
        query = f"""
            SELECT *
            FROM {TABLES['socios_multiplos']}
            ORDER BY qtd_empresas DESC, total_recebido DESC
        """

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        return df

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar sócios múltiplos: {str(e)[:100]}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_CONFIG['ttl_medium'], show_spinner="⏳ Carregando operações suspeitas...")
def load_operacoes_suspeitas(_engine, limit: int = 1000) -> pd.DataFrame:
    """
    Carrega operações suspeitas detalhadas.

    Args:
        _engine: SQLAlchemy engine
        limit: Limite de registros

    Returns:
        pd.DataFrame: Operações suspeitas
    """
    try:
        query = f"""
            SELECT *
            FROM {TABLES['operacoes_suspeitas']}
            ORDER BY score_risco_final DESC, vl_total DESC
            LIMIT {limit}
        """

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        return df

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar operações suspeitas: {str(e)[:100]}")
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
    """
    Aplica filtros ao DataFrame.

    Args:
        df: DataFrame a filtrar
        classificacao: Lista de classificações de risco
        regime: Lista de regimes tributários
        municipio: Lista de municípios
        uf: Lista de UFs
        score_min: Score mínimo
        score_max: Score máximo
        perc_cpf_min: Percentual CPF mínimo
        valor_min: Valor mínimo total

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
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
    """
    Busca empresa por CNPJ ou razão social.

    Args:
        df: DataFrame com dados
        search_term: Termo de busca

    Returns:
        pd.DataFrame: Resultados da busca
    """
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


def get_empresa_details(df: pd.DataFrame, cnpj: str) -> Optional[Dict[str, Any]]:
    """
    Obtém detalhes de uma empresa específica.

    Args:
        df: DataFrame com dados
        cnpj: CNPJ da empresa

    Returns:
        dict ou None: Dicionário com dados da empresa
    """
    empresa = df[df['cnpj'] == cnpj]

    if empresa.empty:
        return None

    return empresa.iloc[0].to_dict()


@st.cache_data(ttl=CACHE_CONFIG['ttl_long'])
def get_unique_values(_engine, table: str, column: str) -> List[Any]:
    """
    Obtém valores únicos de uma coluna.

    Args:
        _engine: SQLAlchemy engine
        table: Nome da tabela
        column: Nome da coluna

    Returns:
        list: Lista de valores únicos
    """
    try:
        query = f"""
            SELECT DISTINCT {column}
            FROM {table}
            WHERE {column} IS NOT NULL
            ORDER BY {column}
        """

        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        return df[column].tolist() if not df.empty else []

    except Exception as e:
        st.warning(f"⚠️ Erro ao obter valores únicos: {str(e)[:100]}")
        return []


@st.cache_data(ttl=CACHE_CONFIG['ttl_short'])
def execute_custom_query(_engine, query: str) -> pd.DataFrame:
    """
    Executa query customizada.

    Args:
        _engine: SQLAlchemy engine
        query: Query SQL

    Returns:
        pd.DataFrame: Resultado da query
    """
    try:
        with _engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao executar query: {str(e)}")
        return pd.DataFrame()
