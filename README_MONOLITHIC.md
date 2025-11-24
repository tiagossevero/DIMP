# 💳 DIMP v2.0 - Versão Monolítica

<div align="center">

**ARQUIVO ÚNICO PRONTO PARA DEPLOY**

Sistema completo consolidado em um único arquivo Python

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Status](https://img.shields.io/badge/Status-Ready-success.svg)

</div>

---

## 🎯 Sobre Esta Versão

Esta é a **versão monolítica** do DIMP v2.0, onde **TODO O CÓDIGO** foi consolidado em um **ÚNICO ARQUIVO PYTHON** para facilitar o deploy em servidores que requerem um arquivo único.

### ✨ Características

- ✅ **Arquivo Único**: Todo o sistema em `DIMP_v2_monolithic.py`
- ✅ **Pronto para Deploy**: Sem dependências de módulos externos
- ✅ **Mesmas Funcionalidades**: Todas as features da versão modular
- ✅ **Fácil de Usar**: Execute apenas 1 arquivo
- ✅ **Organizado**: Código bem comentado e estruturado

---

## 🚀 Como Usar

### 1️⃣ Requisitos

```bash
# Versão Python
Python 3.8 ou superior
```

### 2️⃣ Instalar Dependências

```bash
# Instalar requirements
pip install -r requirements.txt
```

**Conteúdo do requirements.txt:**
```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.14.0
sqlalchemy>=1.4.0
pyhive>=0.6.5
thrift>=0.16.0
thrift-sasl>=0.4.3
scikit-learn>=1.2.0
scipy>=1.10.0
openpyxl>=3.1.0
```

### 3️⃣ Configurar Credenciais

#### Opção A: Usar Streamlit Secrets (Recomendado)

Crie o arquivo `.streamlit/secrets.toml`:

```toml
[auth]
password = "sua_senha_dashboard"

[impala_credentials]
user = "seu_usuario_impala"
password = "sua_senha_impala"
```

#### Opção B: Usar Variáveis de Ambiente

```bash
export DIMP_PASSWORD="sua_senha_dashboard"
export IMPALA_USER="seu_usuario_impala"
export IMPALA_PASSWORD="sua_senha_impala"
```

#### Opção C: Editar Diretamente no Código

Edite as linhas no arquivo `DIMP_v2_monolithic.py`:

```python
# Linha ~90
DEFAULT_PASSWORD = "sua_senha_aqui"  # ⚠️ Trocar!

# Linhas ~100-106
IMPALA_CONFIG = {
    'host': 'seu_servidor_impala',  # ⚠️ Ajustar!
    'port': 21050,
    'database': 'teste',
    # ...
}
```

### 4️⃣ Executar o Dashboard

```bash
streamlit run DIMP_v2_monolithic.py
```

O dashboard abrirá automaticamente em: `http://localhost:8501`

---

## 📋 Estrutura do Arquivo Monolítico

O arquivo `DIMP_v2_monolithic.py` está organizado em seções bem definidas:

```python
# ═══════════════════════════════════════════════════
# SEÇÃO 1: IMPORTAÇÕES (linhas 1-50)
# ═══════════════════════════════════════════════════
# Todas as bibliotecas necessárias

# ═══════════════════════════════════════════════════
# SEÇÃO 2: CONFIGURAÇÕES DA PÁGINA (linhas 51-70)
# ═══════════════════════════════════════════════════
# Configuração do Streamlit

# ═══════════════════════════════════════════════════
# SEÇÃO 3: CONSTANTES E CONFIGS (linhas 71-200)
# ═══════════════════════════════════════════════════
# Senhas, Impala, Tabelas, Cache, Cores, ML, etc.

# ═══════════════════════════════════════════════════
# SEÇÃO 4: ESTILOS CSS (linhas 201-350)
# ═══════════════════════════════════════════════════
# CSS customizado para interface moderna

# ═══════════════════════════════════════════════════
# SEÇÃO 5: FUNÇÕES DE FORMATAÇÃO (linhas 351-450)
# ═══════════════════════════════════════════════════
# format_currency, format_percentage, format_number
# get_risk_color, get_risk_emoji, export functions

# ═══════════════════════════════════════════════════
# SEÇÃO 6: AUTENTICAÇÃO (linhas 451-520)
# ═══════════════════════════════════════════════════
# check_password() - Sistema de login

# ═══════════════════════════════════════════════════
# SEÇÃO 7: CONEXÃO BD (linhas 521-600)
# ═══════════════════════════════════════════════════
# get_engine(), test_connection()

# ═══════════════════════════════════════════════════
# SEÇÃO 8: CARREGAMENTO DE DADOS (linhas 601-750)
# ═══════════════════════════════════════════════════
# load_main_data(), filter_data(), search_empresa()

# ═══════════════════════════════════════════════════
# SEÇÃO 9: ANÁLISE E KPIs (linhas 751-900)
# ═══════════════════════════════════════════════════
# calculate_kpis(), calculate_kpis_by_municipio()
# calculate_descriptive_stats(), correlation_matrix()

# ═══════════════════════════════════════════════════
# SEÇÃO 10: MACHINE LEARNING (linhas 901-1050)
# ═══════════════════════════════════════════════════
# prepare_ml_data(), train_random_forest()
# detect_anomalies()

# ═══════════════════════════════════════════════════
# SEÇÃO 11: VISUALIZAÇÕES (linhas 1051-1250)
# ═══════════════════════════════════════════════════
# create_risk_distribution_pie(), create_top_empresas_bar()
# create_scatter_cpf_vs_total(), create_histogram()
# create_correlation_heatmap(), create_box_plot()

# ═══════════════════════════════════════════════════
# SEÇÃO 12: PÁGINAS DO DASHBOARD (linhas 1251-1700)
# ═══════════════════════════════════════════════════
# page_dashboard_executivo()
# page_ranking_empresas()
# page_machine_learning()
# page_estatisticas()
# page_diagnostico()

# ═══════════════════════════════════════════════════
# SEÇÃO 13: APLICAÇÃO PRINCIPAL (linhas 1701-1800)
# ═══════════════════════════════════════════════════
# main() - Lógica principal e roteamento

# ═══════════════════════════════════════════════════
# SEÇÃO 14: EXECUÇÃO (linhas 1801+)
# ═══════════════════════════════════════════════════
# if __name__ == "__main__": main()
```

---

## 🎨 Funcionalidades Incluídas

### 📊 Dashboard Executivo
- KPIs consolidados
- Gráficos de distribuição de risco
- Top empresas por score
- Análise geográfica por município

### 🏆 Ranking de Empresas
- Busca por CNPJ/Razão Social
- Filtros dinâmicos
- Ordenação múltipla
- Exportação CSV/Excel

### 🤖 Machine Learning
- **Random Forest**: Classificação de risco
- **Isolation Forest**: Detecção de anomalias
- Feature importance
- Métricas detalhadas

### 📈 Estatísticas Avançadas
- Estatísticas descritivas
- Matriz de correlação
- Histogramas
- Box plots

### 🔧 Diagnóstico
- Status de conexão
- Informações do sistema
- Métricas de dados

---

## ⚙️ Configurações Avançadas

### Alterar Porta do Streamlit

```bash
streamlit run DIMP_v2_monolithic.py --server.port 8080
```

### Desabilitar Navegador Automático

```bash
streamlit run DIMP_v2_monolithic.py --server.headless true
```

### Modo de Desenvolvimento

```bash
streamlit run DIMP_v2_monolithic.py --server.runOnSave true
```

---

## 🔒 Segurança

### ⚠️ IMPORTANTE - Antes de usar em Produção:

1. **Trocar Senha Padrão**
   ```python
   DEFAULT_PASSWORD = "tsevero963"  # ⚠️ TROCAR IMEDIATAMENTE!
   ```

2. **Configurar Firewall**
   - Restringir acesso apenas a IPs autorizados

3. **Usar HTTPS**
   - Configure certificado SSL

4. **Proteger Credenciais**
   - Use secrets.toml (nunca commite!)
   - Ou variáveis de ambiente

5. **Atualizar Dependências**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 🐛 Solução de Problemas

### ❌ Erro: "ModuleNotFoundError"

```bash
# Instalar todas as dependências
pip install -r requirements.txt
```

### ❌ Erro: "Connection Failed"

```
Verifique:
1. Host e porta do Impala estão corretos
2. Credenciais estão corretas
3. Firewall está liberado
4. Tabelas existem no banco
```

### ❌ Dashboard lento

```
1. Limpar cache do Streamlit
2. Reduzir TTL de cache no código
3. Usar filtros para reduzir dados carregados
4. Verificar conexão de rede
```

### ❌ Erro de autenticação

```
1. Verificar senha em secrets.toml
2. Verificar variável DIMP_PASSWORD
3. Verificar senha hardcoded no código
```

---

## 📊 Diferenças: Modular vs Monolítico

| Aspecto | Versão Modular | Versão Monolítica |
|---------|---------------|-------------------|
| **Arquivos** | 17 módulos | 1 arquivo único |
| **Deploy** | Precisa copiar estrutura | Copiar 1 arquivo |
| **Manutenção** | Mais fácil | Um pouco mais complexa |
| **Performance** | Mesma | Mesma |
| **Funcionalidades** | Todas | Todas |
| **Organização** | Por módulos | Por seções |
| **Uso Recomendado** | Desenvolvimento | Produção/Deploy |

---

## 📝 Checklist de Deploy

- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Senha padrão alterada
- [ ] Credenciais Impala configuradas
- [ ] Conexão com BD testada
- [ ] Firewall configurado
- [ ] HTTPS configurado (produção)
- [ ] Arquivo testado localmente
- [ ] Documentação revisada

---

## 🚀 Deploy Rápido

### Deploy Local

```bash
# 1. Clonar repositório
git clone https://github.com/tiagossevero/DIMP.git
cd DIMP

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Editar secrets.toml com suas credenciais

# 4. Executar
streamlit run DIMP_v2_monolithic.py
```

### Deploy em Servidor Linux

```bash
# 1. Transferir arquivo
scp DIMP_v2_monolithic.py usuario@servidor:/path/to/app/
scp requirements.txt usuario@servidor:/path/to/app/

# 2. SSH no servidor
ssh usuario@servidor

# 3. Instalar dependências
cd /path/to/app
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
export DIMP_PASSWORD="senha_segura"
export IMPALA_USER="usuario"
export IMPALA_PASSWORD="senha"

# 5. Executar
nohup streamlit run DIMP_v2_monolithic.py --server.port 8501 --server.headless true &
```

---

## 📞 Suporte

### Documentação
- **README Principal**: `README_V2.md`
- **README Monolítico**: Este arquivo
- **README Original**: `README.md`

### Contato
- **Autor**: Auditor Fiscal Tiago Severo
- **Organização**: Receita Estadual de Santa Catarina

---

## 📊 Tamanho do Arquivo

```
DIMP_v2_monolithic.py: ~1800 linhas
Tamanho: ~70 KB
Linhas de código: ~1500
Linhas de comentários: ~300
```

---

## ✅ Vantagens do Arquivo Monolítico

1. ✅ **Deploy Simplificado**: Copiar 1 arquivo apenas
2. ✅ **Sem Imports Complexos**: Tudo em um lugar
3. ✅ **Fácil de Transferir**: Enviar por email, USB, etc.
4. ✅ **Menos Erros de Path**: Sem problemas de módulos
5. ✅ **Compatível**: Funciona em qualquer servidor Python
6. ✅ **Portável**: Rodar de qualquer lugar
7. ✅ **Pronto para Produção**: Deploy imediato

---

<div align="center">

**🎉 Versão Monolítica Pronta para Uso! 🎉**

Desenvolvido por **Auditor Fiscal Tiago Severo**

Receita Estadual de Santa Catarina

---

**DIMP v2.0 Monolithic** | Janeiro 2025

</div>
