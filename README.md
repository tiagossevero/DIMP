# 💳 DIMP - Sistema de Análise de Meios de Pagamento

<div align="center">

**Sistema de Análise de Meios de Pagamento (CNPJ vs CPF de Sócios)**
Receita Estadual de Santa Catarina

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-Proprietário-yellow.svg)
![Status](https://img.shields.io/badge/Status-Ativo-success.svg)

**Versão 1.0** | Desenvolvido por **Auditor Fiscal Tiago Severo**

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Módulos e Páginas](#-módulos-e-páginas)
- [Análise de Machine Learning](#-análise-de-machine-learning)
- [Configuração do Banco de Dados](#-configuração-do-banco-de-dados)
- [Segurança](#-segurança)
- [Contribuição](#-contribuição)
- [Autor](#-autor)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **DIMP** (Dashboard de Inteligência de Meios de Pagamento) é um sistema avançado de análise fiscal desenvolvido para a **Receita Estadual de Santa Catarina**. O sistema realiza análise aprofundada de transações financeiras, identificando padrões suspeitos de pagamentos entre empresas (CNPJs) e seus sócios (CPFs).

### Objetivo Principal

Detectar possíveis irregularidades fiscais através da análise de:
- Volume de pagamentos recebidos via CPF vs CNPJ
- Padrões atípicos de transações
- Empresas com alto risco fiscal
- Relacionamentos entre sócios e múltiplas empresas
- Anomalias comportamentais através de Machine Learning

### Diferenciais

- ✅ **Dashboard Interativo**: Interface intuitiva desenvolvida em Streamlit
- ✅ **Machine Learning**: Modelos de classificação e detecção de anomalias
- ✅ **Análise em Tempo Real**: Consultas otimizadas com cache inteligente
- ✅ **Visualizações Avançadas**: Gráficos interativos com Plotly
- ✅ **Drill-down Completo**: Análise detalhada por empresa, setor e município
- ✅ **Segurança**: Sistema de autenticação para acesso restrito

---

## 🚀 Funcionalidades

### 1. 📊 Dashboard Executivo
- **KPIs Estratégicos**: Total de empresas, volume financeiro, médias de risco
- **Distribuição de Risco**: Classificação em Alto, Médio-Alto, Médio, Baixo
- **Análise Geográfica**: Top municípios e distribuição por UF
- **Gráficos Interativos**: Pizza, barras, mapas de calor

### 2. 🏆 Ranking de Empresas
- Listagem das empresas com maior score de risco
- Filtros por classificação de risco, regime tributário e localização
- Métricas de volume (CPF vs CNPJ) e percentuais
- Ordenação dinâmica por diferentes critérios

### 3. 🔍 Drill-down de Empresa
- Análise individual detalhada de cada empresa
- Informações cadastrais completas
- Histórico de transações
- Análise de sócios vinculados
- Indicadores de risco personalizados

### 4. 🤖 Machine Learning
- **Modelo de Classificação**: Random Forest para predição de risco
- **Detecção de Anomalias**: Isolation Forest para identificar outliers
- **Métricas de Performance**: Accuracy, Precision, Recall, F1-Score
- **Visualizações**: Confusion Matrix, Feature Importance
- **Score de Anomalia**: Identificação automática de comportamentos atípicos

### 5. 🏭 Análise Setorial
- Análise por CNAE (Classificação Nacional de Atividades Econômicas)
- Comparação entre setores econômicos
- Padrões de risco por atividade
- Ranking setorial

### 6. 👥 Análise de Funcionários
- Identificação de funcionários que recebem por CPF
- Análise agregada por empresa
- Detecção de padrões suspeitos em folha de pagamento
- Top funcionários com maiores volumes

### 7. 🔗 Análise de Sócios Múltiplos
- Identificação de sócios com participação em múltiplas empresas
- Análise de rede de relacionamentos
- Detecção de possíveis laranjas fiscais
- Mapeamento de grupos empresariais

### 8. 📈 Análise Temporal
- Evolução de transações ao longo do tempo
- Tendências e sazonalidade
- Comparação de períodos
- Projeções e forecasting

### 9. ⚠️ Padrões Suspeitos
- Detecção automática de padrões irregulares
- Alertas de risco configuráveis
- Casos prioritários para investigação
- Regras de negócio customizáveis

### 10. 🔧 Diagnóstico
- Status da conexão com banco de dados
- Verificação de colunas e tabelas
- Estatísticas do sistema
- Logs e monitoramento

### 11. ℹ️ Sobre
- Informações do sistema
- Documentação de uso
- Contatos e suporte

---

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+**: Linguagem principal
- **Streamlit**: Framework web para dashboards interativos
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica

### Visualização
- **Plotly**: Gráficos interativos
- **Plotly Express**: Visualizações rápidas
- **Plotly Graph Objects**: Gráficos customizados

### Machine Learning
- **Scikit-learn**: Biblioteca de ML
  - Random Forest Classifier
  - Isolation Forest
  - StandardScaler
  - Train/Test Split
  - Classification Metrics

### Banco de Dados
- **SQLAlchemy**: ORM e gerenciamento de conexões
- **Apache Impala**: Data warehouse (via Impala driver)
- **PyHive**: Conector Python para Hive/Impala

### Outras
- **SSL**: Segurança de conexões
- **Pickle**: Serialização de modelos
- **Hashlib**: Hash e criptografia
- **Datetime**: Manipulação de datas

---

## 📦 Requisitos

### Requisitos de Sistema
- Python 3.8 ou superior
- 4GB RAM mínimo (8GB recomendado)
- Conexão com banco de dados Impala/Hive

### Dependências Python

```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.14.0
sqlalchemy>=1.4.0
scikit-learn>=1.2.0
pyhive>=0.6.5
thrift>=0.16.0
thrift-sasl>=0.4.3
```

---

## 🔧 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/tiagossevero/DIMP.git
cd DIMP
```

### 2. Crie um Ambiente Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

Edite o arquivo `DIMP.py` e configure a conexão Impala na função `get_impala_engine()`:

```python
# AJUSTE AQUI: Configure o host e porta do seu Impala
impala_host = "seu-servidor-impala"
impala_port = 21050
database = "teste"
```

### 5. Configure a Senha de Acesso

Altere a senha no arquivo `DIMP.py`:

```python
SENHA = "sua-senha-segura"  # Linha 51
```

---

## 🎮 Uso

### Executar o Dashboard

```bash
streamlit run DIMP.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

### Primeiro Acesso

1. Insira a senha configurada
2. Aguarde o carregamento dos dados (primeira vez pode levar alguns minutos)
3. Navegue pelos módulos usando a barra lateral

### Jupyter Notebook (Exemplo)

Para exploração de dados e testes:

```bash
jupyter notebook DIMP-Exemplo.ipynb
```

---

## 📁 Estrutura do Projeto

```
DIMP/
│
├── DIMP.py                 # Aplicação principal Streamlit
├── DIMP.json              # Configurações e dados auxiliares
├── DIMP-Exemplo.ipynb     # Notebook de exemplos e testes
├── README.md              # Este arquivo
└── requirements.txt       # Dependências Python (criar conforme necessário)
```

### Organização do Código (DIMP.py)

```python
# 1. IMPORTS E CONFIGURAÇÕES INICIAIS
# 2. SISTEMA DE AUTENTICAÇÃO
# 3. ESTILOS CSS CUSTOMIZADOS
# 4. CONEXÃO COM BANCO DE DADOS
# 5. FUNÇÕES DE CARREGAMENTO DE DADOS
# 6. CÁLCULO DE KPIs
# 7. MODELOS DE MACHINE LEARNING
# 8. FILTROS DA SIDEBAR
# 9. PÁGINAS DO DASHBOARD
#    - Dashboard Executivo
#    - Ranking de Empresas
#    - Drill-down de Empresa
#    - Machine Learning
#    - Análise Setorial
#    - Análise de Funcionários
#    - Análise de Sócios Múltiplos
#    - Análise Temporal
#    - Padrões Suspeitos
#    - Diagnóstico
#    - Sobre
# 10. FUNÇÃO MAIN E EXECUÇÃO
```

---

## 📊 Módulos e Páginas

### Dashboard Executivo
**Arquivo**: `pagina_dashboard_executivo()` (linha 582)

Exibe visão geral do sistema com:
- Cards de KPIs principais
- Gráfico de distribuição de risco
- Top 10 empresas de maior risco
- Análise geográfica (municípios e UF)
- Gráficos de pizza e barras

### Ranking de Empresas
**Arquivo**: `pagina_ranking_empresas()` (linha 731)

Funcionalidades:
- Tabela ordenável com todas as empresas
- Filtros por risco, regime tributário, município
- Exportação de dados
- Busca por CNPJ/Razão Social

### Drill-down de Empresa
**Arquivo**: `pagina_drill_down_empresa()` (linha 810)

Análise individual:
- Seleção de empresa
- Dados cadastrais completos
- Indicadores de risco detalhados
- Análise de transações
- Lista de sócios

### Machine Learning
**Arquivo**: `pagina_machine_learning()` (linha 1072)

Modelos implementados:
- **Random Forest**: Classificação de risco
- **Isolation Forest**: Detecção de anomalias
- Métricas de avaliação
- Gráficos de performance

### Análise Setorial
**Arquivo**: `pagina_analise_setorial()` (linha 1259)

Análise por CNAE:
- Distribuição por setor
- Comparação de volumes
- Risco médio por atividade

### Análise de Funcionários
**Arquivo**: `pagina_analise_funcionarios()` (linha 1585)

Detecção de irregularidades:
- Funcionários recebendo por CPF
- Análise agregada por empresa
- Top suspeitos

### Sócios Múltiplos
**Arquivo**: `pagina_analise_socios_multiplos()` (linha 2040)

Identificação de:
- Sócios em múltiplas empresas
- Rede de relacionamentos
- Possíveis laranjas

### Análise Temporal
**Arquivo**: `pagina_analise_temporal()` (linha 2148)

Evolução temporal:
- Séries históricas
- Tendências
- Sazonalidade

### Padrões Suspeitos
**Arquivo**: `pagina_padroes_suspeitos()` (linha 2320)

Detecção automática:
- Regras de negócio
- Alertas configuráveis
- Casos prioritários

### Diagnóstico
**Arquivo**: `pagina_diagnostico()` (linha 2483)

Status do sistema:
- Conexão com BD
- Verificação de tabelas
- Estatísticas gerais

---

## 🤖 Análise de Machine Learning

### Modelo de Classificação (Random Forest)

**Função**: `treinar_modelo_ml()` (linha 443)

**Features utilizadas**:
- `perc_recebido_cpf`: Percentual recebido via CPF
- `total_geral`: Volume total de transações
- `qtd_socios`: Quantidade de sócios
- `score_risco_final`: Score de risco calculado

**Target**: `classificacao_risco` (Alto, Médio-Alto, Médio, Baixo)

**Parâmetros**:
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)
```

### Detecção de Anomalias (Isolation Forest)

**Função**: `detectar_anomalias()` (linha 499)

**Features utilizadas**:
- Mesmas do modelo de classificação
- Normalizadas com StandardScaler

**Parâmetros**:
```python
IsolationForest(
    contamination=0.1,
    random_state=42,
    n_estimators=100
)
```

**Output**: Score de anomalia (-1 para outliers, 1 para normais)

---

## 🗄️ Configuração do Banco de Dados

### Conexão Impala/Hive

**Função**: `get_impala_engine()` (linha 171)

```python
# String de conexão
connection_string = f"impala://{impala_host}:{impala_port}/{database}"

# Engine SQLAlchemy
engine = create_engine(
    connection_string,
    connect_args={'auth_mechanism': 'PLAIN'}
)
```

### Tabelas Utilizadas

**Principal**: `teste.dimp_score_final`

**Colunas esperadas**:
- `cnpj`: CNPJ da empresa
- `nm_razao_social`: Razão social
- `regime_tributario`: Regime tributário
- `classificacao_risco`: Alto/Médio-Alto/Médio/Baixo
- `score_risco_final`: Score numérico de risco
- `total_geral`: Volume total de transações
- `total_recebido_cpf`: Volume recebido via CPF
- `total_recebido_cnpj`: Volume recebido via CNPJ
- `perc_recebido_cpf`: Percentual CPF
- `qtd_socios`: Quantidade de sócios
- `municipio`: Município
- `uf`: Unidade Federativa
- `cnae`: Código CNAE

### Cache de Dados

O sistema utiliza `@st.cache_data` para otimizar performance:

```python
@st.cache_data(ttl=3600)  # Cache de 1 hora
def carregar_resumo_geral(_engine):
    # ...
```

---

## 🔒 Segurança

### Autenticação

**Função**: `check_password()` (linha 53)

- Sistema de senha única configurável
- Sessão persistente durante uso
- Logout automático ao fechar navegador

**IMPORTANTE**: Altere a senha padrão antes de usar em produção!

```python
SENHA = "tsevero963"  # ⚠️ TROCAR ANTES DE USAR
```

### Boas Práticas Recomendadas

1. **Senha Forte**: Use senhas complexas com letras, números e símbolos
2. **HTTPS**: Configure certificado SSL para ambiente de produção
3. **Firewall**: Restrinja acesso apenas a IPs autorizados
4. **Logs**: Implemente auditoria de acessos
5. **Variáveis de Ambiente**: Use `.env` para dados sensíveis

### Exemplo com variáveis de ambiente:

```python
import os
from dotenv import load_dotenv

load_dotenv()
SENHA = os.getenv("DIMP_PASSWORD")
impala_host = os.getenv("IMPALA_HOST")
```

---

## 🤝 Contribuição

Este é um projeto proprietário da **Receita Estadual de Santa Catarina**. Contribuições externas não são aceitas no momento.

Para sugestões ou reportar bugs, entre em contato com o autor.

---

## 👤 Autor

**Auditor Fiscal Tiago Severo**
Receita Estadual de Santa Catarina

📧 Email: [contato disponível mediante solicitação]
💼 LinkedIn: [perfil disponível mediante solicitação]

---

## 📄 Licença

Copyright © 2024 - Receita Estadual de Santa Catarina
Todos os direitos reservados.

Este software é proprietário e confidencial. Uso não autorizado é estritamente proibido.

---

## 📝 Notas de Versão

### Versão 1.0 (Atual)
- ✅ Dashboard executivo completo
- ✅ Sistema de autenticação
- ✅ Modelos de Machine Learning
- ✅ Análise multidimensional
- ✅ Drill-down por empresa
- ✅ Análise setorial, temporal e de funcionários
- ✅ Detecção de padrões suspeitos
- ✅ Visualizações interativas com Plotly

### Próximas Funcionalidades (Roadmap)
- 🔄 Exportação de relatórios em PDF
- 🔄 Integração com outros sistemas da Receita
- 🔄 Alertas automáticos por email
- 🔄 Módulo de predição de fraudes
- 🔄 API REST para integração
- 🔄 Mobile responsivo

---

## 🆘 Suporte e Documentação

### Documentação Adicional

Consulte o **Jupyter Notebook** incluído (`DIMP-Exemplo.ipynb`) para:
- Exemplos de uso
- Análises exploratórias
- Testes de funcionalidades
- Queries SQL customizadas

### Solução de Problemas Comuns

**Erro de conexão com Impala**:
```
Verifique:
1. Host e porta corretos
2. Firewall liberado
3. Credenciais válidas
4. Tabelas existentes no banco
```

**Dashboard não carrega**:
```
1. Verifique logs do Streamlit
2. Confirme instalação de todas as dependências
3. Teste conexão com BD separadamente
```

**Erro de memória**:
```
1. Aumente limite de memória do Python
2. Reduza TTL do cache
3. Limite queries com LIMIT menor
```

---

## 🎓 Sobre o Sistema DIMP

O sistema DIMP foi desenvolvido como ferramenta estratégica de inteligência fiscal, permitindo à Receita Estadual identificar empresas com comportamento atípico em suas operações de pagamento.

Através da análise de milhões de transações e aplicação de técnicas avançadas de Machine Learning, o sistema possibilita:

- **Priorização de Fiscalizações**: Foco em casos de maior risco
- **Otimização de Recursos**: Direcionamento eficiente de auditores
- **Aumento de Arrecadação**: Identificação de sonegação fiscal
- **Transparência**: Dados e métricas claras para tomada de decisão

---

<div align="center">

**Desenvolvido com ❤️ para a Receita Estadual de Santa Catarina**

⚖️ **Promovendo Justiça Fiscal e Transparência** ⚖️

</div>
