# Arquivo: dados_paineis.py
# Comparativo de Produtos Reais (Mercado Livre - Fev/2026)
# Detalhe: Inclui Eficiência, Dimensões e Coeficientes Térmicos

PAINEIS = {
    "BASICO": {
        "modelo": "OSDA 340W Poli/Mono (Entrada)",
        "potencia_w": 340,
        "preco_unitario": 694.95,
        "eficiencia": 0.2067, # 20.67%
        "area_m2": 1.65,      # 1.87m x 0.88m
        "coef_temp_potencia": -0.38, # %/ºC (Estimado para padrão de mercado)
        "bifacial": False
    },
    
    "INTERMEDIARIO": {
        "modelo": "SGV 450W Monocristalino (Mais Vendido)",
        "potencia_w": 450,
        "preco_unitario": 866.58, # Preço Promocional
        "eficiencia": 0.2070, # 20.7% (Conforme anúncio)
        "area_m2": 2.18,      # Exato: 2.094m x 1.038m (Do anúncio)
        "coef_temp_potencia": -0.574, # ATENÇÃO: Perda alta no calor (-0.57%/ºC)
        "bifacial": False
    },
    
    "TOP_LINHA": {
        "modelo": "OSDA 620W Bifacial (Alta Potência)",
        "potencia_w": 620,
        "preco_unitario": 799.90, # Preço Agressivo
        "eficiencia": 0.221,  # ~22.1% (Padrão para Bifaciais N-Type dessa potência)
        "area_m2": 2.80,      # Estimado: ~2.46m x 1.13m (Padrão 620W)
        "coef_temp_potencia": -0.30, # N-Type aquece menos (Melhor para MG)
        "bifacial": True,     # Ganho extra de ~5% a 10% com reflexo do chão
        "fator_bifacial": 1.05 # Consideramos 5% de ganho traseiro no cálculo
    }
}