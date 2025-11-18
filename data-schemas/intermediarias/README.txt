TABELAS INTERMEDIÁRIAS/PROCESSADAS
===================================

Esta pasta contém os schemas das tabelas intermediárias geradas a partir do processamento das tabelas originais.

Tabelas (9):
-----------
1. teste_dimp_score_final.txt                    - ⭐ Scores de risco calculados (PRINCIPAL)
2. teste_dimp_operacoes_suspeitas.txt            - Operações financeiras suspeitas identificadas
3. teste_dimp_socios_multiplas_empresas.txt      - Sócios com participação em múltiplas empresas
4. teste_dimp_comparacao_cnpj_cpf.txt            - Comparação entre pagamentos via CNPJ vs CPF
5. teste_dimp_func_score_final.txt               - Análise de funcionários com scores de risco
6. teste_dimp_funcionarios_agregado.txt          - Dados agregados de funcionários por empresa
7. teste_dimp_func_rede_multiplas.txt            - Funcionários vinculados a múltiplas empresas
8. teste_dimp_func_top_suspeitos.txt             - Top funcionários com comportamento suspeito
9. usr_sat_ods_vw_ods_contrib.txt                - View externa de dados cadastrais ODS

Cada arquivo contém:
-------------------
- DESCRIBE FORMATTED: estrutura completa da tabela
- SELECT * LIMIT 10: amostra de 10 registros

Para gerar os schemas, execute:
------------------------------
python generate_data_schemas.py

ou

jupyter notebook generate_data_schemas.ipynb
