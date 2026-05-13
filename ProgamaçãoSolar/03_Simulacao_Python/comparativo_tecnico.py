import math
import sys
import os

# --- 1. CRIA A PONTE COM A PASTA 02 (SÓ UMA VEZ) ---
# Pega o caminho da pasta atual, volta um nível e entra em '02_Dados_Fazenda'
try:
    caminho_dados = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '02_Dados_Fazenda'))
    sys.path.append(caminho_dados)
    import dados_fazenda as cf 
    import dados_paineis as db
except ImportError:
    print("ERRO CRÍTICO: Não foi possível encontrar os arquivos de dados na pasta 02.")
    sys.exit()

# --- 2. FUNÇÃO VISUAL (PARA O HUMANO LER) ---
def comparar_tecnologias():
    print(f"===========================================================")
    print(f"   ESTUDO COMPARATIVO DE TECNOLOGIAS - TCC SOLAR")
    print(f"   Local: Estrela Dalva/MG | Média HSP: {cf.HSP_MEDIA:.2f}")
    print(f"   Meta de Geração: {cf.MEDIA_MENSAL_REAL:.0f} kWh/mês")
    print(f"===========================================================\n")
    
    melhor_custo = float('inf')
    melhor_opcao = ""

    # Loop para testar cada painel
    for chave, painel in db.PAINEIS.items():
        print(f"--- ANÁLISE DO PRODUTO: {painel['modelo']} ---")
        
        # Cálculos (Mesma lógica da função de baixo, mas aqui imprimimos)
        delta_temp = 40 
        ganho_bifacial = painel.get('fator_bifacial', 1.0)
        pr_especifico = 0.75 * ganho_bifacial 
        
        energia_dia = cf.MEDIA_MENSAL_REAL / 30
        potencia_necessaria_kw = energia_dia / (cf.HSP_MEDIA * pr_especifico)
        qtd_placas = math.ceil((potencia_necessaria_kw * 1000) / painel['potencia_w'])
        
        custo_apenas_placas = qtd_placas * painel['preco_unitario']
        potencia_final_kwp = (qtd_placas * painel['potencia_w']) / 1000
        area_total = qtd_placas * painel['area_m2']
        
        print(f"   > Quantidade Necessária: {qtd_placas} placas")
        print(f"   > Potência Instalada: {potencia_final_kwp:.2f} kWp")
        print(f"   > Área de Telhado: {area_total:.1f} m²")
        print(f"   > Custo dos Painéis: R$ {custo_apenas_placas:,.2f}")
        
        if painel['coef_temp_potencia'] < -0.45:
            print(f"   [!] ALERTA TÉCNICO: Este painel sofre muito com calor ({painel['coef_temp_potencia']}%/ºC).")
        
        if custo_apenas_placas < melhor_custo:
            melhor_custo = custo_apenas_placas
            melhor_opcao = painel['modelo']
            
        print("")

    print(f"===========================================================")
    print(f"CONCLUSÃO FINANCEIRA (Apenas Painéis):")
    print(f"A opção mais econômica é: {melhor_opcao}")
    print(f"Custo: R$ {melhor_custo:,.2f}")
    print(f"===========================================================")

# --- 3. FUNÇÃO LÓGICA (PARA O COMPUTADOR USAR) ---
def obter_melhor_configuracao():
    """
    Roda a comparação silenciosamente e RETORNA os dados da melhor opção.
    """
    melhor_custo = float('inf')
    melhor_dados = {}

    for chave, painel in db.PAINEIS.items():
        ganho_bifacial = painel.get('fator_bifacial', 1.0)
        pr_especifico = 0.75 * ganho_bifacial 
        
        energia_dia = cf.MEDIA_MENSAL_REAL / 30
        potencia_necessaria_kw = energia_dia / (cf.HSP_MEDIA * pr_especifico)
        qtd_placas = math.ceil((potencia_necessaria_kw * 1000) / painel['potencia_w'])
        
        custo_placas = qtd_placas * painel['preco_unitario']
        
        if custo_placas < melhor_custo:
            melhor_custo = custo_placas
            melhor_dados = {
                "modelo": painel['modelo'],
                "qtd": qtd_placas,
                "potencia_modulo": painel['potencia_w'],
                "custo_paineis": custo_placas,
                "area_total": qtd_placas * painel['area_m2'],
                "potencia_total_kwp": (qtd_placas * painel['potencia_w']) / 1000
            }
            
    return melhor_dados

# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    comparar_tecnologias()
    