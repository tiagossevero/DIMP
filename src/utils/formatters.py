"""
Funções de Formatação e Utilidades
"""

import pandas as pd
import streamlit as st
from typing import Any, Union


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


def format_cpf(cpf: str) -> str:
    """Formata CPF com máscara."""
    cpf_str = str(cpf).zfill(11)
    return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"


def get_risk_color(classificacao: str) -> str:
    """Retorna cor baseada na classificação de risco."""
    colors = {
        'ALTO': '#d32f2f',
        'MÉDIO-ALTO': '#f57c00',
        'MÉDIO': '#fbc02d',
        'BAIXO': '#388e3c'
    }
    return colors.get(classificacao, '#757575')


def get_risk_emoji(classificacao: str) -> str:
    """Retorna emoji baseado na classificação de risco."""
    emojis = {
        'ALTO': '🔴',
        'MÉDIO-ALTO': '🟠',
        'MÉDIO': '🟡',
        'BAIXO': '🟢'
    }
    return emojis.get(classificacao, '⚪')


def create_metric_card(label: str, value: Any, delta: Any = None,
                      help_text: str = None, format_type: str = 'number') -> None:
    """Cria card de métrica formatado."""
    if format_type == 'currency':
        formatted_value = format_currency(value)
    elif format_type == 'percentage':
        formatted_value = format_percentage(value)
    elif format_type == 'number':
        formatted_value = format_number(value)
    else:
        formatted_value = str(value)

    if delta is not None:
        if format_type == 'percentage':
            formatted_delta = format_percentage(delta)
        else:
            formatted_delta = str(delta)
        st.metric(label=label, value=formatted_value, delta=formatted_delta, help=help_text)
    else:
        st.metric(label=label, value=formatted_value, help=help_text)


def export_to_csv(df: pd.DataFrame, filename: str = 'export.csv') -> bytes:
    """Exporta DataFrame para CSV."""
    return df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')


def export_to_excel(df: pd.DataFrame) -> bytes:
    """Exporta DataFrame para Excel."""
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    return output.getvalue()


def create_download_button(df: pd.DataFrame, label: str = "📥 Baixar Dados",
                          filename: str = "dados.csv", file_format: str = 'csv') -> None:
    """Cria botão de download de dados."""
    if file_format == 'csv':
        data = export_to_csv(df, filename)
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


def display_dataframe_with_formatting(df: pd.DataFrame,
                                     currency_cols: list = None,
                                     percentage_cols: list = None,
                                     number_cols: list = None) -> None:
    """Exibe DataFrame com formatação customizada."""
    df_display = df.copy()

    if currency_cols:
        for col in currency_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_currency)

    if percentage_cols:
        for col in percentage_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_percentage)

    if number_cols:
        for col in number_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_number)

    st.dataframe(df_display, use_container_width=True)
