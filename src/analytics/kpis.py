"""
Cálculo de KPIs e Indicadores
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula KPIs principais do dashboard.

    Args:
        df: DataFrame com dados principais

    Returns:
        dict: Dicionário com KPIs calculados
    """
    if df.empty:
        return get_empty_kpis()

    kpis = {
        # KPIs Básicos
        'total_empresas': len(df),
        'total_empresas_ativas': len(df),  # Assumindo que todas são ativas

        # KPIs Financeiros
        'volume_total': df['total_geral'].sum() if 'total_geral' in df.columns else 0,
        'volume_cpf': df['total_recebido_cpf'].sum() if 'total_recebido_cpf' in df.columns else 0,
        'volume_cnpj': df['total_recebido_cnpj'].sum() if 'total_recebido_cnpj' in df.columns else 0,

        # Médias
        'media_score_risco': df['score_risco_final'].mean() if 'score_risco_final' in df.columns else 0,
        'media_perc_cpf': df['perc_recebido_cpf'].mean() if 'perc_recebido_cpf' in df.columns else 0,
        'media_volume': df['total_geral'].mean() if 'total_geral' in df.columns else 0,

        # Distribuição de Risco
        'empresas_alto_risco': len(df[df['classificacao_risco'] == 'ALTO']) if 'classificacao_risco' in df.columns else 0,
        'empresas_medio_alto': len(df[df['classificacao_risco'] == 'MÉDIO-ALTO']) if 'classificacao_risco' in df.columns else 0,
        'empresas_medio': len(df[df['classificacao_risco'] == 'MÉDIO']) if 'classificacao_risco' in df.columns else 0,
        'empresas_baixo': len(df[df['classificacao_risco'] == 'BAIXO']) if 'classificacao_risco' in df.columns else 0,

        # Percentuais de Risco
        'perc_alto_risco': (len(df[df['classificacao_risco'] == 'ALTO']) / len(df) * 100) if len(df) > 0 and 'classificacao_risco' in df.columns else 0,
        'perc_medio_alto': (len(df[df['classificacao_risco'] == 'MÉDIO-ALTO']) / len(df) * 100) if len(df) > 0 and 'classificacao_risco' in df.columns else 0,

        # Sócios
        'total_socios_recebendo': df['qtd_socios_recebendo'].sum() if 'qtd_socios_recebendo' in df.columns else 0,
        'media_socios_por_empresa': df['qtd_socios_recebendo'].mean() if 'qtd_socios_recebendo' in df.columns else 0,

        # Alertas
        'empresas_alerta_critico': len(df[
            (df['score_risco_final'] >= 90) if 'score_risco_final' in df.columns else False
        ]),
        'empresas_acima_50pct_cpf': len(df[
            (df['perc_recebido_cpf'] > 50) if 'perc_recebido_cpf' in df.columns else False
        ]),
    }

    # Percentual CPF do total
    if kpis['volume_total'] > 0:
        kpis['perc_total_cpf'] = (kpis['volume_cpf'] / kpis['volume_total']) * 100
    else:
        kpis['perc_total_cpf'] = 0

    return kpis


def get_empty_kpis() -> Dict[str, Any]:
    """Retorna estrutura de KPIs vazia."""
    return {
        'total_empresas': 0,
        'total_empresas_ativas': 0,
        'volume_total': 0,
        'volume_cpf': 0,
        'volume_cnpj': 0,
        'media_score_risco': 0,
        'media_perc_cpf': 0,
        'media_volume': 0,
        'empresas_alto_risco': 0,
        'empresas_medio_alto': 0,
        'empresas_medio': 0,
        'empresas_baixo': 0,
        'perc_alto_risco': 0,
        'perc_medio_alto': 0,
        'total_socios_recebendo': 0,
        'media_socios_por_empresa': 0,
        'empresas_alerta_critico': 0,
        'empresas_acima_50pct_cpf': 0,
        'perc_total_cpf': 0
    }


def calculate_kpis_by_classification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula KPIs agrupados por classificação de risco.

    Args:
        df: DataFrame com dados

    Returns:
        pd.DataFrame: KPIs por classificação
    """
    if df.empty or 'classificacao_risco' not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby('classificacao_risco').agg({
        'cnpj': 'count',
        'total_geral': ['sum', 'mean', 'median'],
        'total_recebido_cpf': ['sum', 'mean'],
        'perc_recebido_cpf': 'mean',
        'score_risco_final': ['mean', 'min', 'max'],
        'qtd_socios_recebendo': ['sum', 'mean']
    }).reset_index()

    grouped.columns = ['_'.join(col).strip('_') for col in grouped.columns.values]

    return grouped


def calculate_kpis_by_regime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula KPIs agrupados por regime tributário.

    Args:
        df: DataFrame com dados

    Returns:
        pd.DataFrame: KPIs por regime
    """
    if df.empty or 'regime_tributario' not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby('regime_tributario').agg({
        'cnpj': 'count',
        'total_geral': ['sum', 'mean'],
        'total_recebido_cpf': 'sum',
        'perc_recebido_cpf': 'mean',
        'score_risco_final': 'mean'
    }).reset_index()

    grouped.columns = ['_'.join(col).strip('_') for col in grouped.columns.values]

    return grouped


def calculate_kpis_by_municipio(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Calcula KPIs agrupados por município.

    Args:
        df: DataFrame com dados
        top_n: Top N municípios

    Returns:
        pd.DataFrame: KPIs por município
    """
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


def calculate_kpis_by_uf(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula KPIs agrupados por UF.

    Args:
        df: DataFrame com dados

    Returns:
        pd.DataFrame: KPIs por UF
    """
    if df.empty or 'uf' not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby('uf').agg({
        'cnpj': 'count',
        'total_geral': 'sum',
        'total_recebido_cpf': 'sum',
        'score_risco_final': 'mean'
    }).reset_index()

    grouped.columns = ['uf', 'qtd_empresas', 'volume_total', 'volume_cpf', 'score_medio']

    return grouped


def calculate_kpis_by_setor(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Calcula KPIs agrupados por setor (CNAE).

    Args:
        df: DataFrame com dados
        top_n: Top N setores

    Returns:
        pd.DataFrame: KPIs por setor
    """
    if df.empty:
        return pd.DataFrame()

    cnae_col = 'nm_cnae1' if 'nm_cnae1' in df.columns else 'cd_cnae1'

    if cnae_col not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby(cnae_col).agg({
        'cnpj': 'count',
        'total_geral': 'sum',
        'total_recebido_cpf': 'sum',
        'perc_recebido_cpf': 'mean',
        'score_risco_final': 'mean'
    }).reset_index()

    grouped.columns = ['setor', 'qtd_empresas', 'volume_total', 'volume_cpf',
                       'perc_medio_cpf', 'score_medio']

    grouped = grouped.sort_values('volume_total', ascending=False).head(top_n)

    return grouped


def identify_outliers(df: pd.DataFrame, column: str, method: str = 'iqr',
                     threshold: float = 1.5) -> pd.DataFrame:
    """
    Identifica outliers em uma coluna.

    Args:
        df: DataFrame
        column: Nome da coluna
        method: Método ('iqr' ou 'zscore')
        threshold: Limiar (1.5 para IQR, 3 para Z-score)

    Returns:
        pd.DataFrame: DataFrame com outliers
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()

    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    elif method == 'zscore':
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        return df[z_scores > threshold]

    return pd.DataFrame()


def calculate_risk_distribution(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula distribuição detalhada de risco.

    Args:
        df: DataFrame com dados

    Returns:
        dict: Distribuição de risco
    """
    if df.empty or 'classificacao_risco' not in df.columns:
        return {}

    total = len(df)
    dist = df['classificacao_risco'].value_counts().to_dict()

    return {
        'counts': dist,
        'percentages': {k: (v / total * 100) for k, v in dist.items()},
        'total': total
    }


def calculate_temporal_metrics(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Calcula métricas temporais.

    Args:
        df: DataFrame com dados
        date_column: Nome da coluna de data

    Returns:
        pd.DataFrame: Métricas por período
    """
    if df.empty or date_column not in df.columns:
        return pd.DataFrame()

    df_copy = df.copy()
    df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='coerce')

    grouped = df_copy.groupby(pd.Grouper(key=date_column, freq='M')).agg({
        'cnpj': 'count',
        'total_geral': 'sum',
        'total_recebido_cpf': 'sum',
        'score_risco_final': 'mean'
    }).reset_index()

    return grouped


def get_top_empresas(df: pd.DataFrame, column: str = 'score_risco_final',
                    n: int = 10, ascending: bool = False) -> pd.DataFrame:
    """
    Obtém top N empresas por determinada coluna.

    Args:
        df: DataFrame
        column: Coluna para ordenação
        n: Número de empresas
        ascending: Ordenação crescente?

    Returns:
        pd.DataFrame: Top empresas
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()

    return df.nlargest(n, column) if not ascending else df.nsmallest(n, column)
