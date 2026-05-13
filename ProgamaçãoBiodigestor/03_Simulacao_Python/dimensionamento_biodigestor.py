import sys
import os
import math
import numpy_financial as npf # Adicionado para os cálculos de VPL e Payback Descontado

# --- 1. IMPORTAÇÃO DOS DADOS ---
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '02_Dados_Fazenda')))
    import dados_fazenda as cf
except ImportError:
    print("ERRO: Não foi possível importar 'dados_fazenda.py'.")
    sys.exit()

def calcular_payback_descontado(capex, fluxo_caixa_mensal, tma_anual):
    """
    Função auxiliar para calcular o Payback Descontado e o VPL.
    """
    tma_mensal = ((1 + (tma_anual / 100))**(1/12)) - 1
    
    # Montando um fluxo de caixa de 25 anos (300 meses)
    fluxo_projeto = [-capex] + [fluxo_caixa_mensal] * 300 
    
    vpl = npf.npv(tma_mensal, fluxo_projeto)
    
    saldo_acumulado = -capex
    meses_payback = 0
    
    for mes, fluxo in enumerate(fluxo_projeto[1:], start=1):
        # Desconta o fluxo do mês para o valor presente
        fluxo_descontado = fluxo / ((1 + tma_mensal)**mes)
        saldo_acumulado += fluxo_descontado
        
        if saldo_acumulado >= 0 and meses_payback == 0:
            meses_payback = mes
            break # Encontrou o mês do payback

    # Se não pagar em 25 anos, retorna infinito
    if meses_payback == 0:
        meses_payback = float('inf')
        
    return meses_payback, vpl

def simular_biodigestor():
    print(f"\n=======================================================")
    print(f"   DIMENSIONAMENTO BIODIGESTOR - FAZENDA ESTRELA DALVA")
    print(f"   Rebanho: {cf.QTD_BOIS} bois | Manejo: Semi-Confinamento")
    print(f"=======================================================\n")

    # --- A. ENGENHARIA ---
    producao_diaria_dejetos = cf.QTD_BOIS * cf.DEJETOS_POR_ANIMAL_DIA
    carga_diaria_total = producao_diaria_dejetos * 2 # Diluição 1:1
    
    # Volume
    TRH_DIAS = 30 
    volume_util_m3 = (carga_diaria_total * TRH_DIAS) / 1000
    volume_total_m3 = volume_util_m3 * 1.10 # +10% Gasômetro

    # Produção Física
    producao_biogas_dia = producao_diaria_dejetos * cf.RENDIMENTO_BIOGAS
    producao_metano_dia = producao_biogas_dia * cf.PUREZA_METANO
    
    # Equivalência Energética
    energia_termica_dia = producao_metano_dia * cf.PCI_METANO
    energia_botijao_p13 = cf.PCI_GLP * 13 
    botijoes_gerados_mes = (energia_termica_dia * 30) / energia_botijao_p13
    
    # Biofertilizante
    biofertilizante_mes = (carga_diaria_total * 0.90) * 30

    # --- B. CAPEX (Custo de Construção do Tanque) ---
    capex_tanque = volume_total_m3 * cf.CUSTO_CONSTRUCAO_M3

    # =========================================================
    # --- C. ANÁLISE DE CENÁRIOS: TÉRMICO vs ELÉTRICO ---
    # =========================================================

    USO_REAL_GAS_SEDE = 2.0  # Consumo da cozinha
    receita_adubo = biofertilizante_mes * cf.PRECO_BIOFERTILIZANTE
    
    # Receita base de Gás (limitada a 2 botijões para a sede)
    if botijoes_gerados_mes > USO_REAL_GAS_SEDE:
        receita_gas_sede = USO_REAL_GAS_SEDE * cf.PRECO_GLP_P13
        desperdicio_gas = botijoes_gerados_mes - USO_REAL_GAS_SEDE
    else:
        receita_gas_sede = botijoes_gerados_mes * cf.PRECO_GLP_P13
        desperdicio_gas = 0

    TMA_ANUAL = 10.0 # Taxa exigida pelo professor Leonardo

    # CENÁRIO 1: APENAS TÉRMICO (Sem Gerador)
    total_receita_termico = receita_gas_sede + receita_adubo
    # payback_simples = capex_tanque / total_receita_termico
    pb_desc_termico, vpl_termico = calcular_payback_descontado(capex_tanque, total_receita_termico, TMA_ANUAL)

    # CENÁRIO 2: COM GERAÇÃO ELÉTRICA (Zera a CEMIG)
    CAPEX_MOTOR = 6775.12 # Motomil 8kVA
    CAPEX_KIT_FILTRO = 500.00 + 2500.00 # Carburador Biogás + Filtro H2S
    capex_total_eletrico = capex_tanque + CAPEX_MOTOR + CAPEX_KIT_FILTRO
    
    economia_cemig = cf.MEDIA_MENSAL_REAL * cf.TARIFA_CEMIG_RURAL
    total_receita_eletrico = economia_cemig + receita_gas_sede + receita_adubo
    # payback_simples = capex_total_eletrico / total_receita_eletrico
    pb_desc_eletrico, vpl_eletrico = calcular_payback_descontado(capex_total_eletrico, total_receita_eletrico, TMA_ANUAL)

    # --- RELATÓRIO FINAL ---
    print(f"--- 1. ESTRUTURA FÍSICA E PRODUÇÃO MENSAL ---")
    print(f"   > Volume do Tanque:   {volume_total_m3:.1f} m³")
    print(f"   > Biogás Gerado:      {botijoes_gerados_mes:.1f} botijões equivalentes")
    print(f"   > Adubo Líquido:      {biofertilizante_mes:,.0f} Litros/mês")

    print(f"\n=======================================================")
    print(f"   ESTUDO DE VIABILIDADE (TMA = {TMA_ANUAL}%)")
    print(f"=======================================================")
    print(f"   INVESTIMENTO (CAPEX)")
    print(f"   > Só Tanque (Térmico):  R$ {capex_tanque:,.2f}")
    print(f"   > Tanque + Gerador:     R$ {capex_total_eletrico:,.2f} (+ R$ {CAPEX_MOTOR+CAPEX_KIT_FILTRO:,.2f} motor e filtro)")
    
    print(f"\n   RETORNO FINANCEIRO MENSAL")
    print(f"   ITEM                | TÉRMICO (Sem Motor) | ELÉTRICO (Com Motor)")
    print(f"   --------------------|---------------------|-----------------------")
    print(f"   Econ. Conta de Luz  | R$             0.00 | R$ {economia_cemig:8,.2f} (CEMIG)")
    print(f"   Econ. Gás Cozinha   | R$ {receita_gas_sede:15,.2f} | R$ {receita_gas_sede:8,.2f}")
    print(f"   Econ. Adubo (NPK)   | R$ {receita_adubo:15,.2f} | R$ {receita_adubo:8,.2f}")
    print(f"   --------------------|---------------------|-----------------------")
    print(f"   TOTAL ECONOMIZADO   | R$ {total_receita_termico:15,.2f} | R$ {total_receita_eletrico:8,.2f}")
    print(f"   PAYBACK DESCONTADO  | {pb_desc_termico:11.1f} meses | {pb_desc_eletrico:8.1f} meses")
    print(f"   VPL DO PROJETO      | R$ {vpl_termico:15,.2f} | R$ {vpl_eletrico:8,.2f}")
    print(f"=======================================================\n")
    
    if desperdicio_gas > 0:
        print(f"   [!] NOTA: No cenário 'Térmico', a fazenda queima {desperdicio_gas:.1f} botijões")
        print(f"       em biogás por falta de um motogerador para aproveitar o excedente.")
    
    return pb_desc_termico, pb_desc_eletrico

if __name__ == "__main__":
    simular_biodigestor()