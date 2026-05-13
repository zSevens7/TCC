# Arquivo: dados_solar.py
# Fonte: CRESESB / INPE
# Localização: Estrela Dalva - MG
# Latitude: -21.701 | Longitude: -42.449

# Dados de Irradiação Solar Diária Média Mensal (kWh/m².dia)
HSP_MENSAL = {
    "JAN": 5.89,
    "FEV": 6.04,
    "MAR": 5.08,
    "ABR": 4.41,
    "MAI": 3.65,
    "JUN": 3.42,
    "JUL": 3.55,
    "AGO": 4.27,
    "SET": 4.68,
    "OUT": 5.00,
    "NOV": 4.94,
    "DEZ": 5.74
}

# Lista simples para cálculos (ordem Jan-Dez)
HSP_LISTA = list(HSP_MENSAL.values())

# Cálculo da média anual exata baseada nos dados
HSP_MEDIA_ANUAL = sum(HSP_LISTA) / len(HSP_LISTA)

# Função auxiliar para pegar a HSP de um mês específico (1 a 12)
def get_hsp_mes(mes_numero):
    """
    Retorna a HSP do mês (1=Jan, 12=Dez).
    """
    chaves = list(HSP_MENSAL.keys())
    return HSP_MENSAL[chaves[mes_numero - 1]]

if __name__ == "__main__":
    print(f"--- DADOS SOLARIMÉTRICOS: ESTRELA DALVA/MG ---")
    print(f"Média Anual Calculada: {HSP_MEDIA_ANUAL:.2f} kWh/m².dia")
    print(f"Pior Mês (Dimensionar por aqui garante 100%): Junho ({HSP_MENSAL['JUN']} kWh)")
    print(f"Melhor Mês: Fevereiro ({HSP_MENSAL['FEV']} kWh)")