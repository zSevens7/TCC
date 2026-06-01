# ⚡ Simulador de Viabilidade Híbrida: Solar Fotovoltaica + Biomassa

Este repositório contém os códigos e rotinas de simulação desenvolvidos para o Trabalho de Conclusão de Curso (TCC) em Engenharia Elétrica pela Universidade Federal de Juiz de Fora (UFJF).

O projeto apresenta um estudo de viabilidade técnica e financeira para a implementação de um sistema híbrido de geração de energia (**Painéis Solares + Biodigestor**) em uma propriedade rural localizada em **Estrela Dalva, Minas Gerais**.

---

# 🎯 Objetivo do Projeto

Desenvolver uma ferramenta computacional capaz de:

- Dimensionar um sistema fotovoltaico ótimo (painéis e inversores) baseado no consumo real e dados solarimétricos (CRESESB/INPE).
- Dimensionar um biodigestor (modelo lagoa coberta) para gado de corte em semi-confinamento, estimando a produção de biogás e biofertilizante.
- Realizar a análise de engenharia econômica comparando cenários (Térmico vs. Elétrico) através de indicadores como:
  - VPL (Valor Presente Líquido)
  - TIR (Taxa Interna de Retorno)
  - Payback Descontado
- Projetar o fluxo de caixa considerando as regras tarifárias da Lei 14.300 (taxação do Fio B) e opções de financiamento bancário.

---

# 🛠️ Tecnologias Utilizadas

O simulador foi construído 100% em Python, utilizando uma arquitetura modularizada e finalizado com um dashboard web interativo.

| Tecnologia | Utilização |
|------------|------------|
| Python 3 | Linguagem principal |
| Streamlit | Interface gráfica e dashboard |
| Pandas | Manipulação de dados |
| NumPy Financial | Matemática financeira |
| Plotly | Gráficos interativos |
| CRESESB/INPE | Dados solarimétricos |

---

# 📂 Estrutura do Repositório

## 📁 02_Dados_Fazenda
### Módulo de Dados e Premissas Base

### 📄 dados_fazenda.py
Concentra as variáveis globais da propriedade:

- Histórico de consumo de energia
- Tarifas da CEMIG
- Regras da Lei 14.300 (Fio B)
- Premissas de custo
- Parâmetros do rebanho bovino
- Produção de dejetos

### 📄 dados_solar.py
Armazena os dados solarimétricos (HSP mensais) específicos da região de Estrela Dalva/MG, obtidos através do CRESESB/INPE.

---

## 📁 03_Simulacao_Python
### Módulo de Processamento e Engenharia Econômica

### 📄 dados_paineis.py
Banco de dados contendo módulos fotovoltaicos disponíveis no mercado.

Funcionalidades:

- Comparação de painéis
- Eficiência
- Coeficiente de temperatura
- Seleção automática da melhor opção custo-benefício

### 📄 dados_inversores.py
Banco de dados comparativo de inversores solares.

Exemplos:

- Deye
- Growatt

Responsável por selecionar automaticamente o inversor ideal com base na potência calculada do sistema.

### 📄 dados_orcamento.py
Script responsável pela composição automática do orçamento.

Calcula:

- Painéis fotovoltaicos
- Inversores
- Estrutura de fixação
- BOS (Balance of System)
- Cabeamento
- Mão de obra

Gerando o CAPEX total do sistema solar.

### 📄 analise_financeira.py
Motor de cálculo financeiro do sistema fotovoltaico.

Responsável por:

- Projetar o fluxo de caixa por 25 anos
- Aplicar inflação energética
- Aplicar regras da Lei 14.300
- Calcular:
  - VPL
  - TIR
  - Payback Descontado

### 📄 app_solar.py
Script principal da aplicação.

Funções:

- Integra todos os módulos do projeto
- Renderiza a interface web no Streamlit
- Exibe gráficos interativos
- Exibe tabelas dinâmicas
- Permite análise dos cenários simulados

---

# 📁 ProgramacaoBiodigestor
### Módulo de Biomassa e Biogás

## 📁 02_Dados_Fazenda

Contém o arquivo:

### 📄 dados_fazenda.py

Premissas relacionadas ao biodigestor:

- Rebanho bovino (80 cabeças)
- Produção diária de dejetos
- Potencial de produção de biogás
- Premissas de CAPEX civil

---

## 📁 03_Simulacao_Python

### 📄 dimensionamento_biodigestor.py

Responsável pelo:

- Dimensionamento volumétrico do biodigestor
- Estimativa de produção de biogás
- Estimativa de produção de biofertilizante
- Cálculo do OPEX
- Análise financeira

Comparação entre:

### Cenário Térmico
Substituição de GLP por biogás.

### Cenário Elétrico
Utilização de motogerador movido a biogás para geração de energia elétrica.

---

# 📊 Indicadores Econômicos Avaliados

O simulador calcula automaticamente:

- Valor Presente Líquido (VPL)
- Taxa Interna de Retorno (TIR)
- Payback Simples
- Payback Descontado
- Fluxo de Caixa Projetado
- Economia Acumulada
- Comparação entre cenários

---

# 🚀 Como Executar o Simulador Localmente

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

## 2️⃣ Acesse a pasta do projeto

```bash
cd seu-repositorio
```

## 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

## 4️⃣ Execute o dashboard

```bash
streamlit run 03_Simulacao_Python/app_solar.py
```

## 5️⃣ Acesse no navegador

```text
http://localhost:8501
```

---

# 📈 Principais Funcionalidades

✅ Dimensionamento fotovoltaico automatizado

✅ Seleção otimizada de painéis e inversores

✅ Cálculo de CAPEX e OPEX

✅ Simulação financeira em horizonte de 25 anos

✅ Aplicação das regras da Lei 14.300

✅ Simulação de biodigestor para bovinos

✅ Comparação de cenários térmico e elétrico

✅ Dashboard interativo em Streamlit

✅ Gráficos dinâmicos com Plotly

---

# 👨‍💻 Autor

**Gabriel Teperino Percegoni Figueira**

Trabalho de Conclusão de Curso (TCC)  
Engenharia Elétrica  
Universidade Federal de Juiz de Fora (UFJF)

---
