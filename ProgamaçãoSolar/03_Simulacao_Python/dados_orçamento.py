# Arquivo: dados_orcamento.py
# Objetivo: Calcular o CAPEX (Investimento Inicial) 100% automatizado
# Pasta: 03_Simulacao_Python

import sys
import os

# --- 1. CONFIGURAÇÃO DE PASTAS ---
# Ponte para a pasta 02 (Dados da Fazenda)
try:
    caminho_dados = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '02_Dados_Fazenda'))
    sys.path.append(caminho_dados)
    import dados_fazenda as cf
except:
    pass

# Importação dos módulos locais (da pasta 03)
import comparativo_tecnico as tech
import dados_inversores as inv  # <--- NOVO: Importa nossa pesquisa de preços

# --- 2. SELEÇÃO INTELIGENTE DE EQUIPAMENTOS ---

# A. Melhor Painel (Menor custo global)
SISTEMA_PAINEIS = tech.obter_melhor_configuracao()
# Ex: 14x OSDA 620W

# B. Melhor Inversor (Menor custo que atende a potência)
INVERSOR_VENCEDOR = inv.obter_melhor_inversor()
# Ex: Deye 8kW

print(f"... Calculando orçamento com: {SISTEMA_PAINEIS['modelo']} + {INVERSOR_VENCEDOR['modelo']} ...")

# --- 3. COMPOSIÇÃO DE CUSTOS (BOM) ---

# A. Custo dos Painéis (Vem do comparativo)
CUSTO_MODULOS = SISTEMA_PAINEIS['custo_paineis']

# B. Custo do Inversor (Vem do dados_inversores)
CUSTO_INVERSOR = INVERSOR_VENCEDOR['preco']

# C. Estrutura de Fixação (Fonte: Artigo UFGD)
# Média de R$ 180,00 por módulo (trilhos + grampos + parafusos inox)
CUSTO_ESTRUTURA = SISTEMA_PAINEIS['qtd'] * 180.00

# D. Materiais Elétricos / BOS (Fonte: Artigo FARESE/UFGD)
# Cabos 6mm, Conectores MC4, String Box, Disjuntores, Eletrodutos.
# Estimativa: R$ 300,00 por kWp instalado
CUSTO_MATERIAIS_ELETRICOS = SISTEMA_PAINEIS['potencia_total_kwp'] * 300.00

# E. Serviços (Projeto + Homologação + Instalação)
# Preço médio na Zona da Mata MG para sistemas de 8kWp
CUSTO_SERVICOS = 4000.00 

# --- 4. RESULTADO FINAL ---
CAPEX_TOTAL = (
    CUSTO_MODULOS +
    CUSTO_INVERSOR +
    CUSTO_ESTRUTURA +
    CUSTO_MATERIAIS_ELETRICOS +
    CUSTO_SERVICOS
)

def exibir_memorial_orcamentario():
    potencia_total = SISTEMA_PAINEIS['potencia_total_kwp']
    
    print(f"\n=======================================================")
    print(f"      MEMORIAL DE ORÇAMENTO DETALHADO (CAPEX)")
    print(f"=======================================================")
    print(f"EQUIPAMENTOS SELECIONADOS:")
    print(f"  > Painéis:  {SISTEMA_PAINEIS['qtd']}x {SISTEMA_PAINEIS['modelo']} ({potencia_total:.2f} kWp)")
    print(f"  > Inversor: 1x {INVERSOR_VENCEDOR['modelo']}")
    print(f"-------------------------------------------------------")
    print(f"COMPOSIÇÃO DE CUSTOS:")
    print(f"  1. Kit Painéis:           R$ {CUSTO_MODULOS:,.2f}")
    print(f"  2. Inversor:              R$ {CUSTO_INVERSOR:,.2f} (Cotado no ML)")
    print(f"  3. Estrutura Fixação:     R$ {CUSTO_ESTRUTURA:,.2f}")
    print(f"  4. BOS (Cabos/Proteção):  R$ {CUSTO_MATERIAIS_ELETRICOS:,.2f}")
    print(f"  5. Projeto e Mão de Obra: R$ {CUSTO_SERVICOS:,.2f}")
    print(f"-------------------------------------------------------")
    print(f"  TOTAL INVESTIMENTO:       R$ {CAPEX_TOTAL:,.2f}")
    print(f"-------------------------------------------------------")
    print(f"INDICADOR DE COMPETITIVIDADE:")
    print(f"  Preço por Watt (R$/Wp):   R$ {CAPEX_TOTAL / (potencia_total*1000):.2f}")
    
    if (CAPEX_TOTAL / (potencia_total*1000)) < 3.00:
        print("  [CONCLUSÃO] O custo está EXCELENTE (Abaixo de R$ 3,00/Wp).")
    else:
        print("  [CONCLUSÃO] O custo está dentro da média de mercado.")
    print(f"=======================================================\n")
    
    # Retorna o valor final para quem quiser usar (Ex: main.py)
    return CAPEX_TOTAL

if __name__ == "__main__":
    exibir_memorial_orcamentario()