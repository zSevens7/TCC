# ⚡ Simulador de Viabilidade Híbrida: Solar Fotovoltaica + Biomassa

Este repositório contém os códigos e rotinas de simulação desenvolvidos para o Trabalho de Conclusão de Curso (TCC) em Engenharia Elétrica pela Universidade Federal de Juiz de Fora (UFJF). 

O projeto apresenta um estudo de viabilidade técnica e financeira para a implementação de um sistema híbrido de geração de energia (Painéis Solares + Biodigestor) em uma propriedade rural localizada em Estrela Dalva, Minas Gerais.

## 🎯 Objetivo do Projeto
Desenvolver uma ferramenta computacional capaz de:
- Dimensionar um sistema fotovoltaico ótimo (painéis e inversores) baseado no consumo real e dados solarimétricos (CRESESB/INPE).
- Dimensionar um biodigestor (modelo lagoa coberta) para gado de corte em semi-confinamento, estimando a produção de biogás e biofertilizante.
- Realizar a análise de engenharia econômica comparando cenários (Térmico vs. Elétrico) através de indicadores como **VPL**, **TIR** e **Payback Descontado**.
- Projetar o fluxo de caixa considerando as regras tarifárias da **Lei 14.300** (taxação do Fio B) e opções de financiamento bancário.

## 🛠️ Tecnologias Utilizadas
O simulador foi construído 100% em **Python**, utilizando uma arquitetura modularizada e finalizado com um Dashboard web interativo.
- **Linguagem:** Python 3
- **Interface Gráfica (Dashboard):** Streamlit
- **Análise de Dados e Matemática Financeira:** Pandas, NumPy Financial
- **Visualização de Dados:** Plotly (Gráficos dinâmicos de fluxo de caixa)

## 📂 Estrutura do Repositório

O projeto está dividido em dois grandes módulos (Solar e Biodigestor), separando os dados brutos da fazenda das lógicas de engenharia e simulação financeira. Abaixo está o detalhamento:

| Diretório / Arquivo | Descrição e Objetivo Técnico |
| :--- | :--- |
| 📁 **`02_Dados_Fazenda/`** | **Módulo de Dados e Premissas Base** |
| 📄 `dados_fazenda.py` | Concentra as variáveis globais da propriedade. Inclui o histórico de consumo, tarifas da CEMIG, regras da Lei 14.300 (Fio B), premissas de custo e parâmetros do rebanho bovino (produção de dejetos). |
| 📄 `dados_solar.py` | Armazena os dados solarimétricos (índices HSP mensais) específicos da região de Estrela Dalva/MG, com base na plataforma CRESESB/INPE. |
| 📁 **`03_Simulacao_Python/`** | **Módulo de Processamento e Engenharia Econômica** |
| 📄 `dados_paineis.py` | Banco de dados com opções de módulos fotovoltaicos do mercado. Contém as especificações técnicas (eficiência, coeficiente de temperatura) e a lógica para selecionar a placa de melhor custo-benefício. |
| 📄 `dados_inversores.py` | Banco de dados comparativo de inversores solares (ex: Deye, Growatt). Contém a rotina que escolhe o inversor ideal com base na potência calculada do sistema. |
| 📄 `dados_orcamento.py` | Script de precificação automatizada. Ele unifica o painel e o inversor vencedores e calcula os custos adicionais (estrutura, BOS/fiação e mão de obra) para compor o CAPEX total do projeto solar. |
| 📄 `analise_financeira.py` | Motor de cálculo financeiro do sistema fotovoltaico. Projeta o fluxo de caixa para 25 anos, aplicando a inflação energética e as taxas Fio B para calcular **VPL**, **TIR** e **Payback Descontado**. |
| 📄 `app_solar.py` | Script principal (`Main`). Renderiza o simulador visual utilizando o framework **Streamlit**, unindo todos os cálculos das duas pastas em um Dashboard interativo com gráficos e tabelas dinâmicas. |
| |
| 📁 **`ProgamaçãoBiodigestor/`** | **Módulo de Biomassa e Biogás** |
| 📁 `02_Dados_Fazenda/` | Contém o `dados_fazenda.py` focado no rebanho bovino (80 cabeças), produção de dejetos, potencial de biogás e premissas de CAPEX civil. |
| 📁 `03_Simulacao_Python/` | Contém o script `dimensionamento_biodigestor.py` que calcula a volumetria do tanque, OPEX e faz a engenharia econômica comparando o cenário Térmico (GLP) com o Elétrico (Motogerador). |

## 🚀 Como Executar o Simulador Localmente

1. Clone este repositório:
   ```bash
   git clone [https://github.com/zSevens7/TCC.git](https://github.com/zSevens7/TCC.git)
   ```

2. Acesse a pasta do projeto:

    ```bash
    cd TCC
    ```

3. Instale as dependências necessárias:
   ```bash
   pip install streamlit pandas plotly numpy-financial
   ```
   
4. Execute o dashboard do Streamlit (aponte para o arquivo da interface gráfica):

    ```bash
    streamlit run ProgamaçãoSolar/03_Simulacao_Python/app_solar.py
    ```


## 👨‍💻 Autor
**Gabriel Teperino Percegoni Figueira**


   
