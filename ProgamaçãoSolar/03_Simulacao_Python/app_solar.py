import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy_financial as npf
import math
import sys
import os

# --- 1. CONFIGURAÇÃO GERAL DA PÁGINA ---
st.set_page_config(
    page_title="Simulador Híbrido - Fazenda Estrela Dalva", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. IMPORTAÇÃO DE DADOS ---
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_dados = os.path.join(diretorio_atual, '..', '02_Dados_Fazenda')
sys.path.append(os.path.abspath(caminho_dados))
try:
    import dados_fazenda as cf
except ImportError:
    st.error("Erro ao importar dados_fazenda. Verifique os caminhos das pastas.")
    st.stop()

# ==========================================================
# --- 3. NAVEGAÇÃO LATERAL PRINCIPAL ---
# ==========================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=50)
    st.title("⚡ Menu de Simulação")
    pagina_selecionada = st.radio(
        "Selecione o Módulo:",
        ["1. Energia Fotovoltaica (Solar)", "2. Biomassa (Biodigestor)", "3. Comparativo Final"]
    )
    st.markdown("---")
    st.subheader("📊 Taxa Mínima de Atratividade")
    # A TMA exigida pelo professor adicionada globalmente
    tma_anual = st.number_input("TMA (% a.a.)", value=10.0, step=0.5, help="Taxa de desconto para cálculo do VPL e Payback Descontado") / 100

# ==========================================================
# --- PÁGINA 1: ENERGIA SOLAR ---
# ==========================================================
if pagina_selecionada == "1. Energia Fotovoltaica (Solar)":
    
    PAINEIS = {
        "OSDA 340W (Entrada)":   {"potencia": 340, "preco": 694.95, "area": 1.65, "temp": -0.38, "bifacial": 1.0},
        "SGV 450W (Padrão)":     {"potencia": 450, "preco": 866.58, "area": 2.18, "temp": -0.57, "bifacial": 1.0},
        "OSDA 620W (Premium)":   {"potencia": 620, "preco": 799.90, "area": 2.80, "temp": -0.30, "bifacial": 1.05}
    }
    INVERSORES = {
        "Deye 8kW (Wi-Fi)":      {"preco": 3651.00},
        "Growatt 8kW (Padrão)":  {"preco": 4049.00},
        "Solis 8kW (Premium)":   {"preco": 4609.00}
    }

    with st.sidebar:
        st.subheader("🎛️ Parâmetros Financeiros")
        inflacao = st.slider("Inflação Energética (% a.a.)", 0.0, 10.0, 6.0) / 100
        simultaneidade = st.slider("Autoconsumo Imediato (%)", 0, 100, 30) / 100
        
        st.markdown("---")
        usar_financiamento = st.toggle("🏦 Usar Financiamento?", value=True)
        
        if usar_financiamento:
            banco_escolhido = st.radio("Instituição:", ["Banco do Brasil", "Caixa Econômica"])
            taxa_padrao = 14.0 if banco_escolhido == "Banco do Brasil" else 13.5
            carencia_meses = 0 if banco_escolhido == "Banco do Brasil" else st.slider("Carência (Meses)", 0, 12, 6)
            taxa_juros = st.number_input("Juros Anuais (% a.a.)", value=taxa_padrao)
            prazo_anos = st.slider("Prazo (Anos)", 1, 10, 5)
            entrada = st.number_input("Entrada (R$)", value=0.0, step=1000.0)
        else:
            taxa_juros, prazo_anos, carencia_meses, entrada = 0, 0, 0, 0

    st.title("☀️ Módulo: Análise Fotovoltaica")
    
    c1, c2 = st.columns(2)
    with c1: painel_nome = st.selectbox("Painel Fotovoltaico:", list(PAINEIS.keys()), index=2)
    with c2: inv_nome = st.selectbox("Inversor Solar:", list(INVERSORES.keys()), index=0)

    painel_dados, inv_dados = PAINEIS[painel_nome], INVERSORES[inv_nome]
    pr_sistema = 0.75 * painel_dados['bifacial']
    potencia_nec_kwp = (cf.MEDIA_MENSAL_REAL / 30) / (cf.HSP_MEDIA * pr_sistema)
    qtd_placas = math.ceil((potencia_nec_kwp * 1000) / painel_dados['potencia'])
    potencia_instalada_kwp = (qtd_placas * painel_dados['potencia']) / 1000

    capex_total = (qtd_placas * painel_dados['preco']) + inv_dados['preco'] + (qtd_placas * 180.00) + (potencia_instalada_kwp * 300.00) + 4000.00

    if not usar_financiamento:
        entrada = capex_total 

    valor_financiado = capex_total - entrada
    meses_totais = prazo_anos * 12
    meses_pagamento = meses_totais - carencia_meses
    taxa_mensal = ((1 + (taxa_juros/100))**(1/12)) - 1 if taxa_juros > 0 else 0
    parcela_full = npf.pmt(taxa_mensal, nper=meses_pagamento, pv=-valor_financiado) if (meses_pagamento > 0 and usar_financiamento) else 0
    parcela_carencia = valor_financiado * taxa_mensal if usar_financiamento else 0

    dados_anuais = [{
        "Ano": 0, "Receita Bruta": 0, "Custo Fio B": 0, "Manutenção": 0, "Pagto Banco": 0, 
        "Fluxo Líquido": -entrada, "Saldo Descontado": -entrada
    }]
    
    fluxo_acionista = [-entrada]
    fluxo_livre_solar = [-capex_total] # Para o cálculo correto da TIR
    saldo_acumulado_descontado = -entrada
    regra_fio_b = {1: 0.60, 2: 0.75, 3: 0.90}
    payback_ano = 0

    for ano in range(1, 26):
        tarifa_ano = cf.TARIFA_CEMIG_RURAL * ((1 + inflacao)**(ano-1))
        fio_b_ano = cf.TARIFA_FIO_B * ((1 + inflacao)**(ano-1))
        geracao_ano = potencia_instalada_kwp * cf.HSP_MEDIA * 30 * 12 * 0.80 * ((1 - cf.DEGRADACAO_ANUAL)**(ano-1))
        
        receita_bruta = geracao_ano * tarifa_ano
        despesa_fio_b = (geracao_ano * (1 - simultaneidade)) * fio_b_ano * regra_fio_b.get(ano, 1.0)
        
        # AQUI: Manutenção do Solar também acompanha a inflação
        manutencao = (capex_total * cf.CUSTO_MANUTENCAO) * ((1 + inflacao)**(ano-1))
        
        pagamento_banco = 0
        if usar_financiamento:
            for m in range(1, 13):
                mes_abs = (ano-1)*12 + m
                if mes_abs <= carencia_meses: pagamento_banco += parcela_carencia
                elif mes_abs <= meses_totais: pagamento_banco += parcela_full
                
        lucro_operacional = receita_bruta - despesa_fio_b - manutencao 
        fluxo_liquido_cliente = lucro_operacional - pagamento_banco 
        
        # Trazendo o fluxo do ano para o Valor Presente (Descontado pela TMA)
        fluxo_descontado = fluxo_liquido_cliente / ((1 + tma_anual)**ano)
        saldo_acumulado_descontado += fluxo_descontado
        
        fluxo_acionista.append(fluxo_liquido_cliente)
        fluxo_livre_solar.append(lucro_operacional)
        
        if saldo_acumulado_descontado >= 0 and payback_ano == 0:
            payback_ano = ano
        
        dados_anuais.append({
            "Ano": ano, "Receita Bruta": receita_bruta, "Custo Fio B": despesa_fio_b, 
            "Manutenção": manutencao, "Pagto Banco": pagamento_banco, 
            "Fluxo Líquido": fluxo_liquido_cliente, "Saldo Descontado": saldo_acumulado_descontado
        })

    df_final = pd.DataFrame(dados_anuais)
    vpl_projeto = npf.npv(tma_anual, fluxo_acionista)
    # AQUI: Usando o Fluxo Livre para calcular a TIR sem dar "nan%" no financiamento integral
    tir_projeto = npf.irr(fluxo_livre_solar) * 100 if npf.irr(fluxo_livre_solar) else 0

    tab_dash, tab_table = st.tabs(["📈 Dashboard Executivo", "📋 Tabela Analítica"])
    with tab_dash:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Investimento (CAPEX)", f"R$ {capex_total:,.2f}")
        k2.metric("VPL do Projeto", f"R$ {vpl_projeto:,.2f}")
        k3.metric("Payback Descontado", f"{payback_ano} Anos" if payback_ano > 0 else "Não Paga")
        k4.metric("TIR do Projeto", f"{tir_projeto:.2f}% a.a.")
        
        # --- GRÁFICO SOLAR (AGORA COM SALDO DESCONTADO) ---
        fig_fluxo_solar = go.Figure()
        
        fig_fluxo_solar.add_trace(go.Bar(
            x=df_final['Ano'], y=df_final['Fluxo Líquido'], 
            name='Lucro Anual (Nominal)', marker_color='#3498DB'
        ))
        
        fig_fluxo_solar.add_trace(go.Scatter(
            x=df_final['Ano'], y=df_final['Saldo Descontado'], 
            name='Saldo Acumulado Descontado (TMA)', mode='lines+markers',
            line=dict(color='#8E44AD', width=3), marker=dict(size=6) # Roxo para representar valor descontado
        ))

        fig_fluxo_solar.add_hline(y=0, line_dash="dash", line_color="black")
        
        fig_fluxo_solar.update_layout(
            title=f"Análise de Fluxo de Caixa Descontado (TMA = {tma_anual*100:.1f}%)",
            yaxis_title="Reais (R$)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig_fluxo_solar, use_container_width=True)

    with tab_table:
        st.dataframe(df_final.style.format({"Receita Bruta": "R$ {:,.2f}", "Custo Fio B": "R$ {:,.2f}", "Manutenção": "R$ {:,.2f}", "Pagto Banco": "R$ {:,.2f}", "Fluxo Líquido": "R$ {:,.2f}", "Saldo Descontado": "R$ {:,.2f}"}))

# ==========================================================
# --- PÁGINA 2: BIODIGESTOR ---
# ==========================================================
elif pagina_selecionada == "2. Biomassa (Biodigestor)":
    st.title("🐄 Módulo: Biodigestor e Biogás")
    
    with st.sidebar:
        st.subheader("⚙️ Parâmetros da Fazenda")
        inflacao_bio = st.slider("Inflação Geral (% a.a.)", 0.0, 10.0, 6.0, help="Inflação aplicada às Receitas e Manutenção") / 100
        cenario_projetado = st.radio("Cenário para Projeção (25 Anos):", ["Térmico (Só Tanque)", "Elétrico (Com Motor)"])
        
        st.markdown("---")
        usar_financiamento_bio = st.toggle("🏦 Financiar Biodigestor?", value=True)
        
        if usar_financiamento_bio:
            banco_escolhido_bio = st.radio("Instituição:", ["Banco do Brasil", "Caixa Econômica"], key="banco_bio")
            taxa_padrao_bio = 14.0 if banco_escolhido_bio == "Banco do Brasil" else 13.5
            taxa_juros_bio = st.number_input("Juros Anuais (% a.a.)", value=taxa_padrao_bio, key="juros_bio")
            prazo_anos_bio = st.slider("Prazo (Anos)", 1, 10, 5, key="prazo_bio")
            entrada_bio = st.number_input("Entrada (R$)", value=0.0, step=1000.0, key="entrada_bio")
        else:
            taxa_juros_bio, prazo_anos_bio, entrada_bio = 0, 0, 0

    producao_diaria_dejetos = cf.QTD_BOIS * cf.DEJETOS_POR_ANIMAL_DIA
    volume_total_m3 = (((producao_diaria_dejetos * 2) * 30) / 1000) * 1.10 
    botijoes_gerados_mes = ((producao_diaria_dejetos * cf.RENDIMENTO_BIOGAS * cf.PUREZA_METANO) * cf.PCI_METANO * 30) / (cf.PCI_GLP * 13)
    biofertilizante_mes = (producao_diaria_dejetos * 2 * 0.90) * 30

    capex_tanque = volume_total_m3 * cf.CUSTO_CONSTRUCAO_M3
    # capex_tanque = capex_tanque * 1.50 ISTO FOI USADO PARA TESTES DE SENSIBILIDADE COM O TANQUE CUSTANDO 50% A MAIS, MAS O VALOR REAL DEVE SER CONSIDERADO PARA A ANÁLISE FINAL
    CAPEX_MOTOR = 9775.12 
    
    capex_projeto = capex_tanque if cenario_projetado == "Térmico (Só Tanque)" else (capex_tanque + CAPEX_MOTOR)
    if not usar_financiamento_bio:
        entrada_bio = capex_projeto

    valor_fin_bio = capex_projeto - entrada_bio
    meses_totais_bio = prazo_anos_bio * 12
    taxa_mensal_bio = ((1 + (taxa_juros_bio/100))**(1/12)) - 1 if taxa_juros_bio > 0 else 0
    parcela_full_bio = npf.pmt(taxa_mensal_bio, nper=meses_totais_bio, pv=-valor_fin_bio) if (meses_totais_bio > 0 and usar_financiamento_bio) else 0

    dados_anuais_bio = [{
        "Ano": 0, "Econ. Gás/Adubo": 0, "Econ. Energia": 0, "Manutenção (OPEX)": 0, "Pagto Banco": 0, 
        "Fluxo Líquido": -entrada_bio, "Saldo Descontado": -entrada_bio
    }]
    
    fluxo_acionista_bio = [-entrada_bio]
    fluxo_livre_bio = [-capex_projeto] # Para o cálculo correto da TIR
    saldo_acumulado_descontado_bio = -entrada_bio
    payback_ano_bio = 0

    for ano in range(1, 26):
        preco_gas_ano = cf.PRECO_GLP_P13 * ((1 + inflacao_bio)**(ano-1))
        preco_adubo_ano = cf.PRECO_BIOFERTILIZANTE * ((1 + inflacao_bio)**(ano-1))
        # preco_adubo_ano = preco_adubo_ano*0.50 ISTO FOI USADO PARA TESTES DE SENSABILIDADES COM O ADUBO TENDO A METADE DO PREÇO
        # preco_adubo_ano = 0.00 ISTO FOI USADO PARA TESTES DE SENSABILIDADE SEM O ADUBO, MAS O VALOR REAL DEVE SER CONSIDERADO PARA A ANÁLISE FINAL
        tarifa_cemig_ano = cf.TARIFA_CEMIG_RURAL * ((1 + inflacao_bio)**(ano-1))

        receita_gas = 2.0 * preco_gas_ano * 12 
        receita_adubo = biofertilizante_mes * preco_adubo_ano * 12
        economia_luz = (cf.MEDIA_MENSAL_REAL * tarifa_cemig_ano * 12) if cenario_projetado == "Elétrico (Com Motor)" else 0
        #economia_luz = (cf.MEDIA_MENSAL_REAL * tarifa_cemig_ano * 12 * 0.80) if cenario_projetado == "Elétrico (Com Motor)" else 0 - Isto foi usado para o caso estresse 4 da analise sensabilidade para ver como ficaria se economia da luz tivesse cortado 20% por algum motivo
        
        receita_bruta_bio = receita_gas + receita_adubo + economia_luz
        
        # AQUI: Manutenção do Biodigestor também acompanha a inflação
        manutencao_bio = (capex_tanque * 0.01) * ((1 + inflacao_bio)**(ano-1))
        if cenario_projetado == "Elétrico (Com Motor)":
            manutencao_bio += (CAPEX_MOTOR * 0.05) * ((1 + inflacao_bio)**(ano-1))

        pagamento_banco_bio = 0
        if usar_financiamento_bio:
            for m in range(1, 13):
                if ((ano-1)*12 + m) <= meses_totais_bio:
                    pagamento_banco_bio += parcela_full_bio

        lucro_operacional_bio = receita_bruta_bio - manutencao_bio
        fluxo_liquido_bio = lucro_operacional_bio - pagamento_banco_bio
        
        # Desconto pela TMA
        fluxo_descontado_bio = fluxo_liquido_bio / ((1 + tma_anual)**ano)
        saldo_acumulado_descontado_bio += fluxo_descontado_bio
        
        fluxo_acionista_bio.append(fluxo_liquido_bio)
        fluxo_livre_bio.append(lucro_operacional_bio)
        
        if saldo_acumulado_descontado_bio >= 0 and payback_ano_bio == 0:
            payback_ano_bio = ano

        dados_anuais_bio.append({
            "Ano": ano, "Econ. Gás/Adubo": (receita_gas+receita_adubo), "Econ. Energia": economia_luz, 
            "Manutenção (OPEX)": manutencao_bio, "Pagto Banco": pagamento_banco_bio, 
            "Fluxo Líquido": fluxo_liquido_bio, "Saldo Descontado": saldo_acumulado_descontado_bio
        })

    df_bio = pd.DataFrame(dados_anuais_bio)
    vpl_bio = npf.npv(tma_anual, fluxo_acionista_bio)
    # AQUI: Usando o Fluxo Livre para calcular a TIR sem dar "nan%" no financiamento integral
    tir_bio = npf.irr(fluxo_livre_bio) * 100 if npf.irr(fluxo_livre_bio) else 0

    tab_dash_b, tab_table_b = st.tabs(["📈 Projeção 25 Anos", "📋 Tabela Analítica"])
    
    with tab_dash_b:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric(f"CAPEX ({cenario_projetado})", f"R$ {capex_projeto:,.2f}")
        k2.metric("VPL do Projeto", f"R$ {vpl_bio:,.2f}")
        k3.metric("Payback Descontado", f"{payback_ano_bio} Anos" if payback_ano_bio > 0 else "Não Paga")
        k4.metric("TIR do Projeto", f"{tir_bio:.2f}% a.a.")
        
        # --- GRÁFICO BIODIGESTOR ---
        fig_fluxo_bio = go.Figure()
        
        fig_fluxo_bio.add_trace(go.Bar(
            x=df_bio['Ano'], y=df_bio['Fluxo Líquido'], 
            name='Lucro Anual (Nominal)', marker_color='#3498DB' 
        ))
        
        fig_fluxo_bio.add_trace(go.Scatter(
            x=df_bio['Ano'], y=df_bio['Saldo Descontado'], 
            name='Saldo Acumulado Descontado (TMA)', mode='lines+markers',
            line=dict(color='#8E44AD', width=3), marker=dict(size=6) # Roxo para manter padrão
        ))

        fig_fluxo_bio.add_hline(y=0, line_dash="dash", line_color="black")
        
        fig_fluxo_bio.update_layout(
            title=f"Análise de Fluxo Descontado - {cenario_projetado} (TMA = {tma_anual*100:.1f}%)",
            yaxis_title="Reais (R$)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig_fluxo_bio, use_container_width=True)

    with tab_table_b:
        st.dataframe(df_bio.style.format({"Econ. Gás/Adubo": "R$ {:,.2f}", "Econ. Energia": "R$ {:,.2f}", "Manutenção (OPEX)": "R$ {:,.2f}", "Pagto Banco": "R$ {:,.2f}", "Fluxo Líquido": "R$ {:,.2f}", "Saldo Descontado": "R$ {:,.2f}"}))

# ==========================================================
# --- PÁGINA 3: COMPARATIVO FINAL ---
# ==========================================================
elif pagina_selecionada == "3. Comparativo Final":
    st.title("⚖️ Conclusão: Análise Financeira (VPL e Payback)")
    
    # Recalculando os VPLs simplificados para o comparativo
    anos = 25
    
    # 1. SOLAR
    capex_solar = 23973.60 
    economia_solar = cf.MEDIA_MENSAL_REAL * cf.TARIFA_CEMIG_RURAL * 12
    fluxo_solar = [-capex_solar] + [economia_solar] * anos
    vpl_solar = npf.npv(tma_anual, fluxo_solar)
    
    # 2. TÉRMICO
    prod_dejetos = cf.QTD_BOIS * cf.DEJETOS_POR_ANIMAL_DIA
    capex_termico = (((prod_dejetos * 2) * 30) / 1000 * 1.10) * cf.CUSTO_CONSTRUCAO_M3
    economia_termico = ((2.0 * cf.PRECO_GLP_P13) + (((prod_dejetos * 2) * 0.90 * 30) * cf.PRECO_BIOFERTILIZANTE)) * 12
    fluxo_termico = [-capex_termico] + [economia_termico] * anos
    vpl_termico = npf.npv(tma_anual, fluxo_termico)
    
    # 3. ELÉTRICO
    capex_eletrico = capex_termico + 9775.12 
    economia_eletrico = economia_termico + economia_solar 
    fluxo_eletrico = [-capex_eletrico] + [economia_eletrico] * anos
    vpl_eletrico = npf.npv(tma_anual, fluxo_eletrico)

    df_comp = pd.DataFrame({
        "Tecnologia": ["Solar (On-Grid)", "Biodigestor (Térmico)", "Biodigestor (Elétrico)"],
        "Investimento (CAPEX)": [capex_solar, capex_termico, capex_eletrico],
        "VPL (Valor Presente Líquido)": [vpl_solar, vpl_termico, vpl_eletrico]
    })

    c1, c2 = st.columns(2)
    with c1:
        fig_vpl = px.bar(df_comp, x="Tecnologia", y="VPL (Valor Presente Líquido)", 
                         color="Tecnologia", text_auto='R$ ,.2f', 
                         title=f"Comparativo de VPL (Rentabilidade) - TMA: {tma_anual*100:.1f}%")
        st.plotly_chart(fig_vpl, use_container_width=True)
    with c2:
        fig_cx = go.Figure()
        fig_cx.add_trace(go.Bar(x=df_comp["Tecnologia"], y=df_comp["Investimento (CAPEX)"], name="CAPEX Inicial", marker_color="#E74C3C"))
        fig_cx.add_trace(go.Bar(x=df_comp["Tecnologia"], y=[economia_solar, economia_termico, economia_eletrico], name="Economia Anual Bruta", marker_color="#2ECC71"))
        fig_cx.update_layout(title="Esforço de Investimento vs. Geração de Caixa", barmode='group')
        st.plotly_chart(fig_cx, use_container_width=True)