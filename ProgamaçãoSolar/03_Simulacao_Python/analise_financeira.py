# Arquivo: analise_financeira.py
# Objetivo: Calcular Payback Descontado, VPL e TIR considerando a Lei 14.300
# Pasta: 03_Simulacao_Python

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import numpy_financial as npf

# --- 1. IMPORTAÇÕES DA NOSSA BASE DE DADOS ---
# Ponte para a pasta 02
try:
    caminho_dados = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '02_Dados_Fazenda'))
    sys.path.append(caminho_dados)
    import dados_fazenda as cf
except:
    pass

# Importa os resultados calculados nos outros scripts
import dados_orcamento as orc
import comparativo_tecnico as tech

def calcular_payback():
    print(f"\n=======================================================")
    print(f"      ANÁLISE DE VIABILIDADE FINANCEIRA (25 ANOS)")
    print(f"=======================================================")

    # 1. DADOS DE ENTRADA AUTOMÁTICOS
    CAPEX = orc.CAPEX_TOTAL  # Puxa os R$ 23.973,60
    
    # Puxa os dados técnicos do sistema escolhido
    SISTEMA = tech.obter_melhor_configuracao()
    potencia_instalada = SISTEMA['potencia_total_kwp']
    
    # 2. PREMISSAS FINANCEIRAS
    inflacao_energetica = 0.06  # 6% ao ano (Média histórica Brasil)
    tarifa_atual = cf.TARIFA_CEMIG_RURAL
    tarifa_fio_b = cf.TARIFA_FIO_B
    
    TMA_ANUAL = 0.10 # Taxa Mínima de Atratividade (10% ao ano)
    tma_mensal = ((1 + TMA_ANUAL)**(1/12)) - 1 # Converte TMA anual para mensal
    
    # 3. SIMULAÇÃO MÊS A MÊS (300 Meses = 25 Anos)
    fluxo_caixa_simples = [-CAPEX] # Para a TIR (não descontado)
    fluxo_caixa_descontado_acumulado = [-CAPEX] # Começa negativo (O gasto da compra)
    saldo_atual_descontado = -CAPEX
    
    payback_meses = 0
    payback_encontrado = False
    
    meses_eixo = [0]
    
    print(f"Calculando fluxo para {cf.HORIZONTE_PROJETO} anos...")
    
    mes_absoluto = 1
    
    for ano in range(1, cf.HORIZONTE_PROJETO + 1):
        # Define a regra da Lei 14.300 para aquele ano
        ano_calendario = cf.ANO_INICIO_OPERACAO + (ano - 1)
        taxa_fio_b_ano = cf.TAXACAO_FIO_B.get(ano_calendario, 1.0) # Se não achar, cobra 100%
        
        # Reajuste da Tarifa (Inflação)
        tarifa_ano = tarifa_atual * ((1 + inflacao_energetica) ** (ano - 1))
        custo_fio_b_ano = tarifa_fio_b * ((1 + inflacao_energetica) ** (ano - 1))
        
        # Degradação do Painel (Produz menos a cada ano)
        fator_degradacao = (1 - cf.DEGRADACAO_ANUAL) ** (ano - 1)
        
        # Loop pelos 12 meses do ano
        for mes in range(12):
            # Geração Mensal Estimada (Média simples baseada na potência)
            geracao_mes = potencia_instalada * cf.HSP_MEDIA * 30 * 0.80 * fator_degradacao
            consumo_mes = cf.CONSUMO_MENSAL[mes]
            
            # Lógica de Autoconsumo vs Injeção
            if geracao_mes >= consumo_mes:
                receita = consumo_mes * tarifa_ano 
                energia_fio_b = geracao_mes * 0.60 # 60% vai pra rede e volta
                despesa_taxacao = energia_fio_b * custo_fio_b_ano * taxa_fio_b_ano
            else:
                receita = geracao_mes * tarifa_ano
                energia_fio_b = geracao_mes * 0.60 
                despesa_taxacao = energia_fio_b * custo_fio_b_ano * taxa_fio_b_ano

            # Manutenção (Limpeza)
            custo_manut = (CAPEX * cf.CUSTO_MANUTENCAO) / 12
            
            # FLUXO NOMINAL (O dinheiro que sobrou na conta naquele mês)
            lucro_mensal_nominal = receita - despesa_taxacao - custo_manut
            fluxo_caixa_simples.append(lucro_mensal_nominal)
            
            # FLUXO DESCONTADO (Trazendo a dinheiro de hoje usando a TMA)
            lucro_mensal_descontado = lucro_mensal_nominal / ((1 + tma_mensal)**mes_absoluto)
            
            # Atualiza Saldo Descontado Acumulado
            saldo_atual_descontado += lucro_mensal_descontado
            fluxo_caixa_descontado_acumulado.append(saldo_atual_descontado)
            meses_eixo.append(mes_absoluto)
            
            if saldo_atual_descontado >= 0 and not payback_encontrado:
                payback_meses = mes_absoluto
                payback_encontrado = True
                
            mes_absoluto += 1

    # 4. EXIBINDO RESULTADOS FINANCEIROS
    anos = payback_meses // 12
    meses_residuais = payback_meses % 12
    
    # Cálculo do VPL e TIR usando numpy_financial no fluxo nominal
    vpl_projeto = npf.npv(tma_mensal, fluxo_caixa_simples)
    tir_projeto = npf.irr(fluxo_caixa_simples) * 12 * 100 # TIR Anualizada
    
    print(f"-------------------------------------------------------")
    print(f"RESULTADO FINAL (TMA = 10% a.a.):")
    print(f"VPL (Valor Presente Líquido): R$ {vpl_projeto:,.2f}")
    print(f"TIR do Projeto: {tir_projeto:.2f}% a.a.")
    if payback_encontrado:
        print(f"PAYBACK DESCONTADO: {anos} Anos e {meses_residuais} Meses ({payback_meses} meses no total)")
    else:
        print(f"PAYBACK DESCONTADO: Mais de {cf.HORIZONTE_PROJETO} anos (Não paga o investimento)")
    print(f"-------------------------------------------------------")

    # 5. GERANDO O GRÁFICO (AGORA COM FLUXO DESCONTADO)
    plt.figure(figsize=(10, 6))
    plt.plot(meses_eixo, fluxo_caixa_descontado_acumulado, label='Fluxo Descontado Acumulado', color='purple', linewidth=2)
    plt.axhline(0, color='red', linestyle='--', label='Ponto de Equilibrio (R$ 0)')
    
    # Marca o ponto de Payback
    if payback_encontrado:
        plt.scatter(payback_meses, 0, color='blue', s=100, zorder=5)
        plt.text(payback_meses, CAPEX*0.5, f' Payback:\n {anos}a {meses_residuais}m', color='blue', fontweight='bold')

    plt.title(f'Payback Solar - Fazenda Estrela Dalva\nInvestimento: R$ {CAPEX:,.2f} | Lei 14.300 | TMA: 10%', fontsize=12)
    plt.xlabel('Meses de Operação')
    plt.ylabel('Saldo Financeiro Atualizado (R$)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    
    print("Gerando gráfico...")
    plt.show()

if __name__ == "__main__":
    calcular_payback()