"""
Análises Comparativas
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


def compare_empresas(df: pd.DataFrame, cnpjs: List[str]) -> pd.DataFrame:
    """
    Compara múltiplas empresas lado a lado.

    Args:
        df: DataFrame com dados
        cnpjs: Lista de CNPJs para comparar

    Returns:
        pd.DataFrame: Comparação das empresas
    """
    if df.empty or not cnpjs:
        return pd.DataFrame()

    empresas = df[df['cnpj'].isin(cnpjs)].copy()

    if empresas.empty:
        return pd.DataFrame()

    # Selecionar colunas relevantes
    cols_comparacao = [
        'cnpj', 'nm_razao_social', 'classificacao_risco', 'score_risco_final',
        'total_geral', 'total_recebido_cpf', 'total_recebido_cnpj',
        'perc_recebido_cpf', 'qtd_socios_recebendo', 'regime_tributario',
        'municipio', 'uf'
    ]

    cols_existentes = [col for col in cols_comparacao if col in empresas.columns]

    return empresas[cols_existentes]


def compare_with_sector(df: pd.DataFrame, cnpj: str, sector_column: str = 'nm_cnae1') -> Dict[str, Any]:
    """
    Compara empresa com a média do seu setor.

    Args:
        df: DataFrame
        cnpj: CNPJ da empresa
        sector_column: Coluna do setor

    Returns:
        dict: Comparação com setor
    """
    if df.empty or cnpj not in df['cnpj'].values:
        return {}

    empresa = df[df['cnpj'] == cnpj].iloc[0]
    setor_value = empresa.get(sector_column)

    if pd.isna(setor_value):
        return {}

    setor_df = df[df[sector_column] == setor_value]

    if len(setor_df) < 2:
        return {}

    comparison = {
        'empresa': {
            'cnpj': cnpj,
            'razao_social': empresa.get('nm_razao_social', 'N/A'),
            'setor': setor_value
        },
        'metricas_empresa': {},
        'metricas_setor': {},
        'diferencas': {},
        'posicao_ranking': {}
    }

    # Métricas para comparar
    metricas = ['score_risco_final', 'total_geral', 'perc_recebido_cpf',
                'total_recebido_cpf', 'qtd_socios_recebendo']

    for metrica in metricas:
        if metrica not in df.columns:
            continue

        valor_empresa = empresa.get(metrica, 0)
        media_setor = setor_df[metrica].mean()
        mediana_setor = setor_df[metrica].median()

        comparison['metricas_empresa'][metrica] = valor_empresa
        comparison['metricas_setor'][f'{metrica}_media'] = media_setor
        comparison['metricas_setor'][f'{metrica}_mediana'] = mediana_setor

        # Diferença percentual em relação à média
        if media_setor != 0:
            diff_pct = ((valor_empresa - media_setor) / media_setor) * 100
            comparison['diferencas'][metrica] = diff_pct

        # Posição no ranking do setor
        setor_sorted = setor_df.sort_values(metrica, ascending=False)
        posicao = list(setor_sorted['cnpj']).index(cnpj) + 1
        total_setor = len(setor_df)
        comparison['posicao_ranking'][metrica] = {
            'posicao': posicao,
            'total': total_setor,
            'percentil': (total_setor - posicao) / total_setor * 100
        }

    return comparison


def compare_with_regime(df: pd.DataFrame, cnpj: str) -> Dict[str, Any]:
    """
    Compara empresa com a média do seu regime tributário.

    Args:
        df: DataFrame
        cnpj: CNPJ da empresa

    Returns:
        dict: Comparação com regime
    """
    if df.empty or cnpj not in df['cnpj'].values or 'regime_tributario' not in df.columns:
        return {}

    empresa = df[df['cnpj'] == cnpj].iloc[0]
    regime = empresa.get('regime_tributario')

    if pd.isna(regime):
        return {}

    regime_df = df[df['regime_tributario'] == regime]

    comparison = {
        'regime': regime,
        'qtd_empresas_regime': len(regime_df),
        'metricas': {}
    }

    metricas = ['score_risco_final', 'total_geral', 'perc_recebido_cpf']

    for metrica in metricas:
        if metrica not in df.columns:
            continue

        valor_empresa = empresa.get(metrica, 0)
        media_regime = regime_df[metrica].mean()
        std_regime = regime_df[metrica].std()

        comparison['metricas'][metrica] = {
            'valor_empresa': valor_empresa,
            'media_regime': media_regime,
            'desvio_padrao': std_regime,
            'z_score': (valor_empresa - media_regime) / std_regime if std_regime > 0 else 0
        }

    return comparison


def benchmark_analysis(df: pd.DataFrame, cnpj: str) -> Dict[str, Any]:
    """
    Análise de benchmark completa de uma empresa.

    Args:
        df: DataFrame
        cnpj: CNPJ da empresa

    Returns:
        dict: Análise de benchmark
    """
    if df.empty or cnpj not in df['cnpj'].values:
        return {}

    empresa = df[df['cnpj'] == cnpj].iloc[0]

    benchmark = {
        'empresa': {
            'cnpj': cnpj,
            'razao_social': empresa.get('nm_razao_social', 'N/A')
        },
        'comparacao_geral': {},
        'comparacao_setor': {},
        'comparacao_regime': {},
        'percentis': {}
    }

    metricas = ['score_risco_final', 'total_geral', 'perc_recebido_cpf']

    # Comparação geral
    for metrica in metricas:
        if metrica not in df.columns:
            continue

        valor = empresa.get(metrica, 0)
        serie = df[metrica]

        benchmark['comparacao_geral'][metrica] = {
            'valor': valor,
            'media_geral': serie.mean(),
            'mediana_geral': serie.median(),
            'min_geral': serie.min(),
            'max_geral': serie.max()
        }

        # Calcular percentil
        percentil = (serie < valor).sum() / len(serie) * 100
        benchmark['percentis'][metrica] = percentil

    # Comparações específicas
    if 'nm_cnae1' in df.columns:
        benchmark['comparacao_setor'] = compare_with_sector(df, cnpj)

    if 'regime_tributario' in df.columns:
        benchmark['comparacao_regime'] = compare_with_regime(df, cnpj)

    return benchmark


def identify_similar_companies(df: pd.DataFrame, cnpj: str, n: int = 10,
                               similarity_features: List[str] = None) -> pd.DataFrame:
    """
    Identifica empresas similares com base em features.

    Args:
        df: DataFrame
        cnpj: CNPJ de referência
        n: Número de empresas similares
        similarity_features: Features para comparação

    Returns:
        pd.DataFrame: Empresas similares
    """
    if df.empty or cnpj not in df['cnpj'].values:
        return pd.DataFrame()

    if similarity_features is None:
        similarity_features = ['score_risco_final', 'perc_recebido_cpf',
                              'total_geral', 'qtd_socios_recebendo']

    # Filtrar features existentes
    features = [f for f in similarity_features if f in df.columns]

    if not features:
        return pd.DataFrame()

    empresa_ref = df[df['cnpj'] == cnpj][features].iloc[0]

    # Calcular distância euclidiana normalizada
    df_features = df[df['cnpj'] != cnpj][features].copy()

    # Normalizar features
    for feature in features:
        mean = df_features[feature].mean()
        std = df_features[feature].std()
        if std > 0:
            df_features[feature] = (df_features[feature] - mean) / std
            empresa_ref[feature] = (empresa_ref[feature] - mean) / std

    # Calcular distâncias
    distances = np.sqrt(((df_features - empresa_ref.values) ** 2).sum(axis=1))

    df_copy = df[df['cnpj'] != cnpj].copy()
    df_copy['similarity_distance'] = distances
    df_copy = df_copy.sort_values('similarity_distance').head(n)

    return df_copy


def compare_periods(df: pd.DataFrame, period_column: str,
                   period1: Any, period2: Any) -> Dict[str, Any]:
    """
    Compara métricas entre dois períodos.

    Args:
        df: DataFrame
        period_column: Coluna de período
        period1: Período 1
        period2: Período 2

    Returns:
        dict: Comparação entre períodos
    """
    if df.empty or period_column not in df.columns:
        return {}

    df1 = df[df[period_column] == period1]
    df2 = df[df[period_column] == period2]

    if df1.empty or df2.empty:
        return {}

    comparison = {
        'period1': period1,
        'period2': period2,
        'metricas': {}
    }

    metricas = ['total_geral', 'total_recebido_cpf', 'score_risco_final']

    for metrica in metricas:
        if metrica not in df.columns:
            continue

        valor1 = df1[metrica].sum() if metrica.startswith('total') else df1[metrica].mean()
        valor2 = df2[metrica].sum() if metrica.startswith('total') else df2[metrica].mean()

        variacao = valor2 - valor1
        variacao_pct = (variacao / valor1 * 100) if valor1 != 0 else 0

        comparison['metricas'][metrica] = {
            'valor_period1': valor1,
            'valor_period2': valor2,
            'variacao_absoluta': variacao,
            'variacao_percentual': variacao_pct
        }

    return comparison
