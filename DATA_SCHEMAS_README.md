# Gerador de Data Schemas - Projeto DIMP

Scripts para gerar automaticamente os schemas de todas as tabelas do projeto DIMP.

## 📋 O que é gerado

Para cada uma das **13 tabelas** do projeto, o script gera:

1. **DESCRIBE FORMATTED** - Estrutura completa da tabela (colunas, tipos, metadados)
2. **SELECT * LIMIT 10** - Amostra de 10 registros para visualizar os dados

## 📂 Tabelas Processadas

### Tabelas Originais (4)
- `teste.dimp_cnpj_base` - Base cadastral de empresas
- `teste.dimp_socios` - Informações de sócios
- `teste.dimp_pagamentos_cnpj` - Pagamentos via CNPJ (com NF)
- `teste.dimp_pagamentos_cpf` - Pagamentos via CPF (sem NF)

### Tabelas Intermediárias (9)
- `teste.dimp_score_final` ⭐ - Scores de risco (tabela principal)
- `teste.dimp_operacoes_suspeitas` - Operações suspeitas
- `teste.dimp_socios_multiplas_empresas` - Sócios em múltiplas empresas
- `teste.dimp_comparacao_cnpj_cpf` - Comparação CNPJ vs CPF
- `teste.dimp_func_score_final` - Scores de funcionários
- `teste.dimp_funcionarios_agregado` - Agregação de funcionários
- `teste.dimp_func_rede_multiplas` - Funcionários em múltiplas empresas
- `teste.dimp_func_top_suspeitos` - Top funcionários suspeitos
- `usr_sat_ods.vw_ods_contrib` - View externa de cadastro ODS

## 🚀 Como Usar

### Opção 1: Jupyter Notebook (Recomendado)

1. Abra o notebook:
   ```bash
   jupyter notebook generate_data_schemas.ipynb
   ```

2. Execute todas as células em sequência (Cell > Run All)

3. Acompanhe o progresso em tempo real

### Opção 2: Script Python

1. Execute o script:
   ```bash
   python generate_data_schemas.py
   ```

2. Aguarde a conclusão (pode levar alguns minutos)

## 📁 Estrutura de Saída

Os schemas serão salvos na pasta `data-schemas/`:

```
data-schemas/
├── RESUMO.txt                                    # Resumo geral da execução
├── originais/                                    # 4 tabelas originais
│   ├── teste_dimp_cnpj_base.txt
│   ├── teste_dimp_socios.txt
│   ├── teste_dimp_pagamentos_cnpj.txt
│   └── teste_dimp_pagamentos_cpf.txt
└── intermediarias/                               # 9 tabelas intermediárias
    ├── teste_dimp_score_final.txt
    ├── teste_dimp_operacoes_suspeitas.txt
    ├── teste_dimp_socios_multiplas_empresas.txt
    ├── teste_dimp_comparacao_cnpj_cpf.txt
    ├── teste_dimp_func_score_final.txt
    ├── teste_dimp_funcionarios_agregado.txt
    ├── teste_dimp_func_rede_multiplas.txt
    ├── teste_dimp_func_top_suspeitos.txt
    └── usr_sat_ods_vw_ods_contrib.txt
```

## 📄 Formato dos Arquivos

Cada arquivo `.txt` contém:

```
-- DESCRIBE FORMATTED teste.dimp_score_final
-- Gerado em: 2025-11-17 14:30:00

col_name                            data_type
--------------------------------------------------------------------------------
cnpj                                string
nm_razao_social                     string
score_risco_final                   double
...


-- SELECT * FROM teste.dimp_score_final LIMIT 10
-- Gerado em: 2025-11-17 14:30:05

cnpj | nm_razao_social | score_risco_final | ...
--------------------------------------------------------
12345678000190 | EMPRESA EXEMPLO LTDA | 85.5 | ...
...
```

## ⚙️ Requisitos

- Acesso ao banco de dados Spark
- Biblioteca `utils.spark_utils_session` configurada
- Permissões de leitura nas tabelas do schema `teste`
- Permissões de leitura na view `usr_sat_ods.vw_ods_contrib`

## 🔧 Customização

### Alterar limite de registros

No código, altere a linha:
```python
df = spark.sql(f"SELECT * FROM {tabela} LIMIT 10")
```

Para:
```python
df = spark.sql(f"SELECT * FROM {tabela} LIMIT 50")  # 50 registros
```

### Adicionar/Remover tabelas

Edite o dicionário `TABELAS` no início do script:

```python
TABELAS = {
    'originais': [
        'teste.dimp_cnpj_base',
        'teste.sua_nova_tabela',  # Adicione aqui
    ],
    'intermediarias': [
        'teste.dimp_score_final',
        # ...
    ]
}
```

## 📊 Informações Adicionais

### Tempo de Execução
- **Estimado**: 2-5 minutos (depende do tamanho das tabelas)
- Cada tabela leva ~10-30 segundos

### Tratamento de Erros
- Se uma tabela falhar, o script continua processando as demais
- Erros são registrados nos arquivos `.txt` correspondentes
- Um resumo final indica quantas tabelas foram processadas com sucesso

### Logs
O script exibe logs detalhados:
```
======================================================================
Processando: teste.dimp_score_final
======================================================================
  → DESCRIBE FORMATTED teste.dimp_score_final
  → SELECT * FROM teste.dimp_score_final LIMIT 10
✓ Salvo em: data-schemas/intermediarias/teste_dimp_score_final.txt
```

## 🆘 Solução de Problemas

### Erro: "Table not found"
- Verifique se você tem acesso ao schema `teste`
- Confirme se a tabela existe no banco

### Erro ao inicializar Spark
- Verifique suas credenciais de acesso
- Confirme se o módulo `utils.spark_utils_session` está disponível

### Pasta não criada
- Verifique permissões de escrita no diretório atual
- Execute com `sudo` se necessário (não recomendado)

## 📝 Próximos Passos

Após gerar os schemas:

1. Revise os arquivos gerados em `data-schemas/`
2. Verifique se todas as 13 tabelas foram processadas
3. Use esses schemas para:
   - Documentação do projeto
   - Análise de estrutura de dados
   - Onboarding de novos desenvolvedores
   - Versionamento de schemas

## 📞 Suporte

Em caso de dúvidas ou problemas:
1. Verifique o arquivo `data-schemas/RESUMO.txt`
2. Revise os logs de execução
3. Consulte a documentação do PySpark

---

**Gerado por**: Claude Code
**Data**: 2025-11-17
**Versão**: 1.0
