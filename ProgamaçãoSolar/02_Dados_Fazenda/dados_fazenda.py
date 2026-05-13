# Arquivo: dados_fazenda.py
# TCC: Viabilidade Híbrida (Solar + Biomassa) - Fazenda Estrela Dalva (MG)
# Autor: Gabriel Teperino Percegoni Figueira

try:
    import dados_solar  # Importa o arquivo com os dados do CRESESB/INPE
    print("Sucesso: Dados solarimétricos de Estrela Dalva carregados.")
except ImportError:
    print("ERRO: O arquivo 'dados_solar.py' não foi encontrado na mesma pasta.")
    # Valor de fallback caso o arquivo não exista (apenas segurança)
    class dados_solar:
        HSP_MEDIA_ANUAL = 4.90
        HSP_MENSAL = {"JUN": 3.42} 

# ====================================================================
# --- 1. DADOS DE CONSUMO REAL E SOLAR (2025) ---
# ====================================================================

# Extraído da tabela de contas de energia da fazenda (Jan-Dez)
CONSUMO_MENSAL = [
    824, 914, 919, 890, 901, 887, 713, 886, 890, 1379, 927, 924
]

# Cálculo automático da média para dimensionamento
MEDIA_MENSAL_REAL = sum(CONSUMO_MENSAL) / len(CONSUMO_MENSAL) # ~921 kWh

# Agora puxamos a média exata calculada no outro arquivo
HSP_MEDIA = dados_solar.HSP_MEDIA_ANUAL 

TARIFA_CEMIG_RURAL = 0.68  # R$/kWh (Com impostos)
TARIFA_FIO_B = 0.28        # R$/kWh (Componente TUSD Fio B para taxação)

# Parâmetros do Sistema Solar
PERDA_SISTEMA = 0.25       # 25% (Perda por temperatura, poeira de curral e cabos)
DEGRADACAO_ANUAL = 0.005   # 0.5% ao ano (Degradação natural do silício)
CAPEX_ESTIMADO = 28000.00  # R$ (Custo estimado kit + instalação + projeto)
CUSTO_MANUTENCAO = 0.005   # 0.5% do Capex ao ano (Limpeza própria)

# --- LEI 14.300 (CRONOGRAMA DE COBRANÇA) ---
ANO_INICIO_OPERACAO = 2026
HORIZONTE_PROJETO = 20     # Anos de análise (2026 até 2046)

TAXACAO_FIO_B = {
    2026: 0.60, # 60%
    2027: 0.75, # 75%
    2028: 0.90, # 90%
    2029: 1.00, # 100% (Transição concluída)
}

# ====================================================================
# --- 2. DADOS TÉCNICOS DO BIODIGESTOR (GADO DE CORTE) ---
# ====================================================================

QTD_BOIS = 80 
PESO_MEDIO_ANIMAL = 499.0 
DEJETOS_POR_ANIMAL_DIA = 12.0 
RENDIMENTO_BIOGAS = 0.036 
PUREZA_METANO = 0.62      
PCI_METANO = 9.97         
PCI_GLP = 11.1            

# --- PREMISSAS DE INVESTIMENTO E RECEITAS (BIODIGESTOR) ---
CUSTO_CONSTRUCAO_M3 = 444.79 # Custo da obra civil por m³ (Já com juros INCC)
PRECO_GLP_P13 = 120.00       # Preço do botijão em MG
PRECO_BIOFERTILIZANTE = 0.02 # Preço a granel do litro (equivalente NPK)