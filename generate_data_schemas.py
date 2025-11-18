"""
Script para gerar data schemas de todas as tabelas do projeto DIMP
Executa DESCRIBE FORMATTED e SELECT * LIMIT 10 para cada tabela
"""

import os
from datetime import datetime
from pathlib import Path

# Importar utilitários Spark (seguindo padrão do notebook)
from utils import spark_utils_session as utils


# Lista completa de tabelas do projeto DIMP
TABELAS = {
    # Tabelas Originais (Fonte de Dados)
    'originais': [
        'teste.dimp_cnpj_base',
        'teste.dimp_socios',
        'teste.dimp_pagamentos_cnpj',
        'teste.dimp_pagamentos_cpf',
    ],

    # Tabelas Intermediárias/Processadas
    'intermediarias': [
        'teste.dimp_score_final',
        'teste.dimp_operacoes_suspeitas',
        'teste.dimp_socios_multiplas_empresas',
        'teste.dimp_comparacao_cnpj_cpf',
        'teste.dimp_func_score_final',
        'teste.dimp_funcionarios_agregado',
        'teste.dimp_func_rede_multiplas',
        'teste.dimp_func_top_suspeitos',
        'usr_sat_ods.vw_ods_contrib',
    ]
}


def get_session(profile: str = 'default', dynamic_allocation_enabled: bool = True):
    """Cria sessão Spark (adaptado do notebook DIMP-Exemplo.ipynb)."""
    spark_builder = (utils.DBASparkAppSession
                     .builder
                     .appName('DIMP_Data_Schema_Generator')
                     .language(utils.AvailableLanguages.PYTHON)
                     .profileName(profile))

    if dynamic_allocation_enabled:
        spark_builder.autoResourceManagement()

    return spark_builder.build()


def criar_estrutura_pastas():
    """Cria estrutura de pastas para armazenar os schemas."""
    base_path = Path('data-schemas')

    # Criar diretórios
    dirs = [
        base_path / 'originais',
        base_path / 'intermediarias',
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    print(f"✓ Estrutura de pastas criada em: {base_path.absolute()}")
    return base_path


def executar_describe_formatted(spark, tabela: str) -> str:
    """Executa DESCRIBE FORMATTED e retorna resultado como string."""
    try:
        print(f"  → Executando DESCRIBE FORMATTED {tabela}...")
        df = spark.sql(f"DESCRIBE FORMATTED {tabela}")

        # Converter para string formatada
        resultado = f"-- DESCRIBE FORMATTED {tabela}\n"
        resultado += f"-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Coletar dados e formatar
        rows = df.collect()
        for row in rows:
            resultado += f"{row[0]:<35} {row[1]:<40} {row[2] if len(row) > 2 else ''}\n"

        return resultado
    except Exception as e:
        error_msg = f"-- ERRO ao executar DESCRIBE FORMATTED {tabela}\n-- {str(e)}\n"
        print(f"  ✗ Erro: {str(e)}")
        return error_msg


def executar_select_sample(spark, tabela: str) -> str:
    """Executa SELECT * LIMIT 10 e retorna resultado como string."""
    try:
        print(f"  → Executando SELECT * FROM {tabela} LIMIT 10...")
        df = spark.sql(f"SELECT * FROM {tabela} LIMIT 10")

        # Converter para string formatada
        resultado = f"\n\n-- SELECT * FROM {tabela} LIMIT 10\n"
        resultado += f"-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Obter nomes das colunas
        colunas = df.columns

        # Coletar dados
        rows = df.collect()

        if not rows:
            resultado += "-- Tabela vazia (sem dados)\n"
            return resultado

        # Formatar como tabela
        resultado += " | ".join(colunas) + "\n"
        resultado += "-" * (len(" | ".join(colunas))) + "\n"

        for row in rows:
            valores = [str(row[col]) if row[col] is not None else 'NULL' for col in colunas]
            resultado += " | ".join(valores) + "\n"

        return resultado
    except Exception as e:
        error_msg = f"\n\n-- ERRO ao executar SELECT FROM {tabela}\n-- {str(e)}\n"
        print(f"  ✗ Erro: {str(e)}")
        return error_msg


def gerar_schema_tabela(spark, tabela: str, tipo: str, base_path: Path):
    """Gera schema completo para uma tabela (DESCRIBE + SELECT)."""
    print(f"\n{'='*70}")
    print(f"Processando: {tabela}")
    print(f"{'='*70}")

    # Executar comandos
    describe_result = executar_describe_formatted(spark, tabela)
    select_result = executar_select_sample(spark, tabela)

    # Combinar resultados
    conteudo_completo = describe_result + select_result

    # Definir nome do arquivo
    nome_limpo = tabela.replace('.', '_')
    arquivo = base_path / tipo / f"{nome_limpo}.txt"

    # Salvar arquivo
    arquivo.write_text(conteudo_completo, encoding='utf-8')
    print(f"✓ Schema salvo em: {arquivo}")

    return arquivo


def main():
    """Função principal."""
    print("="*70)
    print("GERADOR DE DATA SCHEMAS - PROJETO DIMP")
    print("="*70)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Criar estrutura de pastas
    base_path = criar_estrutura_pastas()

    # Inicializar sessão Spark
    print("\n→ Inicializando sessão Spark...")
    try:
        session = get_session()
        spark = session.sparkSession
        print("✓ Sessão Spark iniciada com sucesso\n")
    except Exception as e:
        print(f"✗ Erro ao inicializar Spark: {e}")
        return

    # Contador de tabelas processadas
    total_tabelas = sum(len(tabelas) for tabelas in TABELAS.values())
    processadas = 0
    com_erro = 0

    # Processar cada categoria de tabelas
    for tipo, lista_tabelas in TABELAS.items():
        print(f"\n{'#'*70}")
        print(f"# CATEGORIA: {tipo.upper()}")
        print(f"# Total de tabelas: {len(lista_tabelas)}")
        print(f"{'#'*70}")

        for tabela in lista_tabelas:
            try:
                gerar_schema_tabela(spark, tabela, tipo, base_path)
                processadas += 1
            except Exception as e:
                print(f"✗ Erro ao processar {tabela}: {e}")
                com_erro += 1

    # Gerar arquivo de resumo
    resumo_path = base_path / 'RESUMO.txt'
    resumo = f"""
RESUMO DA GERAÇÃO DE DATA SCHEMAS
{'='*70}

Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de tabelas: {total_tabelas}
Processadas com sucesso: {processadas}
Com erro: {com_erro}

TABELAS ORIGINAIS ({len(TABELAS['originais'])}):
{chr(10).join(f'  - {t}' for t in TABELAS['originais'])}

TABELAS INTERMEDIÁRIAS ({len(TABELAS['intermediarias'])}):
{chr(10).join(f'  - {t}' for t in TABELAS['intermediarias'])}

{'='*70}
Arquivos salvos em: {base_path.absolute()}
"""

    resumo_path.write_text(resumo, encoding='utf-8')
    print(resumo)

    # Finalizar sessão Spark
    print("\n→ Finalizando sessão Spark...")
    session.stop()
    print("✓ Sessão finalizada")

    print(f"\n{'='*70}")
    print("CONCLUÍDO!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
