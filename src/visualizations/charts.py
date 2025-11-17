"""Gráficos e Visualizações com Plotly"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional
from ..config.settings import COLOR_SCHEME


def create_risk_distribution_pie(df: pd.DataFrame) -> go.Figure:
    """Gráfico de pizza - distribuição de risco"""
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
    """Gráfico de barras - top empresas"""
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
    """Gráfico de dispersão - CPF vs Total"""
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


def create_geographic_map(df: pd.DataFrame) -> go.Figure:
    """Mapa geográfico por UF"""
    if df.empty or 'uf' not in df.columns:
        return go.Figure()

    uf_data = df.groupby('uf').agg({
        'cnpj': 'count',
        'total_geral': 'sum',
        'score_risco_final': 'mean'
    }).reset_index()

    fig = px.choropleth(
        uf_data,
        locations='uf',
        locationmode='USA-states',
        color='score_risco_final',
        hover_data=['cnpj', 'total_geral'],
        color_continuous_scale='Reds',
        title='Distribuição Geográfica - Score Médio de Risco por UF'
    )

    fig.update_geos(scope='south america')
    fig.update_layout(height=500)

    return fig


def create_histogram(df: pd.DataFrame, column: str, title: str = None) -> go.Figure:
    """Histograma de distribuição"""
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
    """Mapa de calor de correlação"""
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


def create_sunburst(df: pd.DataFrame) -> go.Figure:
    """Gráfico sunburst hierárquico"""
    if df.empty:
        return go.Figure()

    # Criar hierarquia: UF -> Município -> Classificação
    hierarchy = df.groupby(['uf', 'municipio', 'classificacao_risco']).agg({
        'total_geral': 'sum'
    }).reset_index()

    fig = px.sunburst(
        hierarchy,
        path=['uf', 'municipio', 'classificacao_risco'],
        values='total_geral',
        color='classificacao_risco',
        color_discrete_map=COLOR_SCHEME['risco'],
        title='Distribuição Hierárquica: UF → Município → Risco'
    )

    fig.update_layout(height=600)

    return fig


def create_box_plot(df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """Box plot para comparação"""
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


def create_timeline(df: pd.DataFrame, date_col: str, value_col: str) -> go.Figure:
    """Gráfico de linha temporal"""
    if df.empty or date_col not in df.columns:
        return go.Figure()

    df_sorted = df.sort_values(date_col)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted[date_col],
        y=df_sorted[value_col],
        mode='lines+markers',
        name=value_col,
        line=dict(color='#1976d2', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title='Evolução Temporal',
        xaxis_title='Data',
        yaxis_title=value_col,
        height=400,
        hovermode='x unified'
    )

    return fig
