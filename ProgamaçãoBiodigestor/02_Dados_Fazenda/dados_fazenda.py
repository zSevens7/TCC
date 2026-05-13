# Arquivo: dados_fazenda.py
# TCC: Viabilidade Híbrida (Solar + Biodigestor) - Fazenda Estrela Dalva (MG)
# Autor: Gabriel Teperino Percegoni Figueira

import math

# --- 1. DADOS SOLARIMÉTRICOS (LOCALIZAÇÃO) ---
try:
    import dados_solar
    HSP_MEDIA = dados_solar.HSP_MEDIA_ANUAL 
    print("Sucesso: Dados solarimétricos de Estrela Dalva carregados.")
except ImportError:
    HSP_MEDIA = 4.90  # Valor de fallback (kWh/m².dia)

# --- 2. CONSUMO ELÉTRICO E TARIFAS ---
CONSUMO_MENSAL = [824, 914, 919, 890, 901, 887, 713, 886, 890, 1379, 927, 924]
MEDIA_MENSAL_REAL = sum(CONSUMO_MENSAL) / len(CONSUMO_MENSAL) # ~921 kWh

TARIFA_CEMIG_RURAL = 0.68  # R$/kWh
TARIFA_FIO_B = 0.28        # R$/kWh (Taxação Lei 14.300)
CAPEX_SOLAR_OTIMIZADO = 23973.60 # Baseado em 14 placas de 620W

# --- 3. DADOS TÉCNICOS DO BIODIGESTOR (GADO DE CORTE) ---
# O dimensionamento baseia-se em 80 animais em regime de semi-confinamento.

# Rebanho e Manejo
QTD_BOIS = 80 
PESO_MEDIO_ANIMAL = 499.0  # kg
# Produção de dejetos considerando 12h/dia de confinamento (pernoite no curral)
DEJETOS_POR_ANIMAL_DIA = 12.0 # kg/dia 

# Potencial Energético (Biogás)
# Fator tecnológico de 60% adotado para biodigestores de lagoa coberta (BLC)
RENDIMENTO_BIOGAS = 0.036 # Nm3 de biogás por kg de dejeto 
PUREZA_METANO = 0.62      # 62% de CH4 no biogás de gado de corte 

# Constantes Físico-Químicas
PCI_METANO = 9.97         # kWh/Nm3 (Poder Calorífico Inferior)
PCI_GLP = 11.1            # kcal/kg (Referência para substituição de botijão)

# --- 4. PREMISSAS DE INVESTIMENTO E RECEITAS (BIODIGESTOR) ---
# Referência SciELO para CAPEX: Cervantes et al. (2016)
# O custo base na época era de aproximadamente R$ 180,00/m³ (Modelo Canadense Básico)
CUSTO_BASE_2016_M3 = 180.00 

# Atualização financeira (2016 para 2026)
TAXA_INCC_ANUAL = 0.075  # Inflação média anual da construção civil (~7,5% ao ano)
ANOS_DEFAZAGEM = 10      # 2026 - 2016

# Fórmula de Matemática Financeira (Juros Compostos para correção monetária)
CUSTO_ATUALIZADO_M3 = CUSTO_BASE_2016_M3 * ((1 + TAXA_INCC_ANUAL) ** ANOS_DEFAZAGEM)

# Margem de segurança para periféricos não contabilizados em 2016 (Flare, tubulações de PEAD modernas)
MARGEM_PERIFERICOS = 1.20 # +20%

# Custo final calculado dinamicamente
CUSTO_CONSTRUCAO_M3 = CUSTO_ATUALIZADO_M3 * MARGEM_PERIFERICOS # Vai dar ~R$ 445,00

# ATUALIZAÇÃO DE MERCADO (MARÇO/2026)
PRECO_GLP_P13 = 120.00       # R$ (Fonte: Painel Dinâmico ANP, MG)
PRECO_BIOFERTILIZANTE = 0.02 # R$/litro (Fonte: Cotação Granel MF Rural)

# --- 5. CRONOGRAMA LEI 14.300 ---
ANO_INICIO = 2026
TAXACAO_FIO_B = {2026: 0.60, 2027: 0.75, 2028: 0.90, 2029: 1.00}