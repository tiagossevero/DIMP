"""
Análises Estatísticas Avançadas
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, Tuple, List


def calculate_descriptive_stats(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Calcula estatísticas descritivas para múltiplas colunas.

    Args:
        df: DataFrame
        columns: Lista de colunas numéricas

    Returns:
        pd.DataFrame: Estatísticas descritivas
    """
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
            'q99': series.quantile(0.99),
            'skewness': series.skew(),
            'kurtosis': series.kurtosis()
        }

    return pd.DataFrame(stats_dict).T


def calculate_correlation_matrix(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Calcula matriz de correlação.

    Args:
        df: DataFrame
        columns: Colunas para correlação

    Returns:
        pd.DataFrame: Matriz de correlação
    """
    if df.empty:
        return pd.DataFrame()

    valid_cols = [col for col in columns if col in df.columns]

    if not valid_cols:
        return pd.DataFrame()

    return df[valid_cols].corr()


def perform_normality_test(series: pd.Series) -> Dict[str, Any]:
    """
    Realiza teste de normalidade (Shapiro-Wilk).

    Args:
        series: Série de dados

    Returns:
        dict: Resultados do teste
    """
    series_clean = series.dropna()

    if len(series_clean) < 3:
        return {'error': 'Dados insuficientes'}

    try:
        statistic, p_value = stats.shapiro(series_clean)
        return {
            'test': 'Shapiro-Wilk',
            'statistic': statistic,
            'p_value': p_value,
            'is_normal': p_value > 0.05,
            'interpretation': 'Normal' if p_value > 0.05 else 'Não-normal'
        }
    except Exception as e:
        return {'error': str(e)}


def calculate_percentiles(df: pd.DataFrame, column: str,
                         percentiles: List[float] = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]) -> Dict[str, float]:
    """
    Calcula percentis para uma coluna.

    Args:
        df: DataFrame
        column: Nome da coluna
        percentiles: Lista de percentis

    Returns:
        dict: Percentis calculados
    """
    if df.empty or column not in df.columns:
        return {}

    series = df[column].dropna()

    return {f'p{int(p*100)}': series.quantile(p) for p in percentiles}


def detect_anomalies_statistical(df: pd.DataFrame, column: str,
                                method: str = 'zscore', threshold: float = 3) -> pd.DataFrame:
    """
    Detecta anomalias usando métodos estatísticos.

    Args:
        df: DataFrame
        column: Coluna para análise
        method: Método ('zscore', 'iqr', 'modified_zscore')
        threshold: Limiar para detecção

    Returns:
        pd.DataFrame: Dados com flag de anomalia
    """
    if df.empty or column not in df.columns:
        return df

    df_copy = df.copy()
    series = df[column]

    if method == 'zscore':
        z_scores = np.abs((series - series.mean()) / series.std())
        df_copy['is_anomaly'] = z_scores > threshold
        df_copy['anomaly_score'] = z_scores

    elif method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        df_copy['is_anomaly'] = (series < lower_bound) | (series > upper_bound)
        df_copy['anomaly_score'] = np.abs((series - series.median()) / IQR)

    elif method == 'modified_zscore':
        median = series.median()
        mad = np.median(np.abs(series - median))
        modified_z = 0.6745 * (series - median) / mad
        df_copy['is_anomaly'] = np.abs(modified_z) > threshold
        df_copy['anomaly_score'] = np.abs(modified_z)

    return df_copy


def calculate_concentration_index(df: pd.DataFrame, value_column: str,
                                  group_column: str = None) -> Dict[str, float]:
    """
    Calcula índice de concentração (Gini, HHI).

    Args:
        df: DataFrame
        value_column: Coluna de valores
        group_column: Coluna de agrupamento (opcional)

    Returns:
        dict: Índices de concentração
    """
    if df.empty or value_column not in df.columns:
        return {}

    values = df[value_column].dropna().sort_values()

    # Índice de Gini
    n = len(values)
    if n == 0:
        return {}

    cumsum = values.cumsum()
    gini = (2 * (cumsum * np.arange(1, n + 1)).sum() / (n * cumsum.iloc[-1])) - (n + 1) / n

    # HHI (Herfindahl-Hirschman Index)
    total = values.sum()
    if total > 0:
        market_shares = (values / total) ** 2
        hhi = market_shares.sum() * 10000  # Multiplicar por 10000 para escala tradicional
    else:
        hhi = 0

    # CR4 (Concentration Ratio dos top 4)
    top4_sum = values.nlargest(4).sum()
    cr4 = (top4_sum / total * 100) if total > 0 else 0

    return {
        'gini_index': gini,
        'hhi': hhi,
        'cr4': cr4,
        'total_value': total,
        'count': n
    }


def perform_hypothesis_test(group1: pd.Series, group2: pd.Series,
                           test_type: str = 'ttest') -> Dict[str, Any]:
    """
    Realiza teste de hipótese entre dois grupos.

    Args:
        group1: Série do grupo 1
        group2: Série do grupo 2
        test_type: Tipo de teste ('ttest', 'mannwhitneyu')

    Returns:
        dict: Resultados do teste
    """
    g1 = group1.dropna()
    g2 = group2.dropna()

    if len(g1) < 2 or len(g2) < 2:
        return {'error': 'Dados insuficientes'}

    try:
        if test_type == 'ttest':
            statistic, p_value = stats.ttest_ind(g1, g2)
            test_name = 'T-Test'
        elif test_type == 'mannwhitneyu':
            statistic, p_value = stats.mannwhitneyu(g1, g2)
            test_name = 'Mann-Whitney U'
        else:
            return {'error': 'Tipo de teste inválido'}

        return {
            'test': test_name,
            'statistic': statistic,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'interpretation': 'Diferença significativa' if p_value < 0.05 else 'Sem diferença significativa'
        }
    except Exception as e:
        return {'error': str(e)}


def calculate_growth_rate(df: pd.DataFrame, value_column: str,
                         time_column: str, method: str = 'simple') -> pd.DataFrame:
    """
    Calcula taxa de crescimento.

    Args:
        df: DataFrame
        value_column: Coluna de valores
        time_column: Coluna de tempo
        method: Método ('simple', 'compound', 'log')

    Returns:
        pd.DataFrame: Dados com taxa de crescimento
    """
    if df.empty or value_column not in df.columns or time_column not in df.columns:
        return df

    df_sorted = df.sort_values(time_column).copy()

    if method == 'simple':
        df_sorted['growth_rate'] = df_sorted[value_column].pct_change() * 100

    elif method == 'compound':
        df_sorted['growth_rate'] = ((df_sorted[value_column] / df_sorted[value_column].shift(1)) - 1) * 100

    elif method == 'log':
        df_sorted['growth_rate'] = np.log(df_sorted[value_column] / df_sorted[value_column].shift(1)) * 100

    return df_sorted


def calculate_moving_statistics(df: pd.DataFrame, column: str,
                               window: int = 3) -> pd.DataFrame:
    """
    Calcula estatísticas móveis.

    Args:
        df: DataFrame
        column: Coluna para cálculo
        window: Janela de tempo

    Returns:
        pd.DataFrame: DataFrame com estatísticas móveis
    """
    if df.empty or column not in df.columns:
        return df

    df_copy = df.copy()

    df_copy[f'{column}_ma'] = df[column].rolling(window=window).mean()
    df_copy[f'{column}_std'] = df[column].rolling(window=window).std()
    df_copy[f'{column}_min'] = df[column].rolling(window=window).min()
    df_copy[f'{column}_max'] = df[column].rolling(window=window).max()

    return df_copy
