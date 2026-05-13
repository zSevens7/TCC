# Arquivo: dados_inversores.py
# Comparativo de Inversores Reais (Mercado Livre - Fev/2026)

INVERSORES = {
    "DEYE_8KW": {
        "modelo": "Deye SUN-8K-G02P1-EU-AM2",
        "potencia_nominal_kw": 8.0,
        "tensao_saida": "220V Monofásico",
        "mppt": 2,
        "preco": 3651.00,
        "link": "https://www.mercadolivre.com.br/inversor-solar-on-grid-deye-sun-8kw-220v-cwifi-integrado/p/MLB2053344166",
        "descricao": "Inversor robusto com WiFi integrado e 2 MPPTs. Melhor custo-benefício atual."
    },
    
    "GROWATT_8KW": {
        "modelo": "Growatt MIN8000TL-X2",
        "potencia_nominal_kw": 8.0,
        "tensao_saida": "220V Monofásico",
        "mppt": 3, # Growatt às vezes tem 3 MPPTs no modelo X2, ponto positivo
        "preco": 4049.00,
        "link": "https://www.mercadolivre.com.br/inversor-solar-ongrid-growatt-8kw-min8000tl-x2-3mppt-afci/p/MLB2051522655",
        "descricao": "Marca tradicional, mas preço superior ao Deye."
    },
    
    "SOLIS_8KW": {
        "modelo": "Solis S6-GR1P8K02-NV-YD-HC",
        "potencia_nominal_kw": 8.0,
        "tensao_saida": "220V Monofásico",
        "mppt": 2,
        "preco": 4609.00,
        "link": "https://www.mercadolivre.com.br/inversor-solar-on-grid-8kw-para-residencias-solis-afci-2mppt/p/MLB50707249",
        "descricao": "Alta tecnologia com proteção AFCI, porém custo elevado."
    }
}

# Função para retornar o melhor custo-benefício automaticamente
def obter_melhor_inversor():
    # Lógica: Menor preço que atenda 8kW
    melhor = min(INVERSORES.values(), key=lambda x: x['preco'])
    return melhor