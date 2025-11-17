TABELAS ORIGINAIS (Fonte de Dados)
==================================

Esta pasta contém os schemas das tabelas originais que alimentam o sistema DIMP.

Tabelas (4):
-----------
1. teste_dimp_cnpj_base.txt          - Base cadastral de empresas
2. teste_dimp_socios.txt             - Informações de sócios das empresas
3. teste_dimp_pagamentos_cnpj.txt    - Pagamentos recebidos via CNPJ (com nota fiscal)
4. teste_dimp_pagamentos_cpf.txt     - Pagamentos recebidos via CPF de sócios (sem NF)

Cada arquivo contém:
-------------------
- DESCRIBE FORMATTED: estrutura completa da tabela
- SELECT * LIMIT 10: amostra de 10 registros

Para gerar os schemas, execute:
------------------------------
python generate_data_schemas.py

ou

jupyter notebook generate_data_schemas.ipynb
