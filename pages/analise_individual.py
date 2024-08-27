import streamlit as st
import pandas as pd;
import plotly.express as px;
import plotly.graph_objects as go
import numpy as np

df_vendas = pd.read_excel('analitico.xlsx')
df_crescimento = pd.read_excel('crescimentoPeriodo1Ano.xlsx')

st.title('Analise individual - Grupo Avatim')
lojas_selecionadas = st.selectbox("Escolha uma loja:", options=sorted({"Aram", "Artemia", "Distribuição", "Pátio", "Mangara", "Maia"}))

despesas_por_loja = df_vendas.groupby('Loja')[['Aluguel', 'Energia, Água e Internet',
                                                 'Despesas Operacionais', 'Despesas Eventuais', 'Marketing',
                                                 'Impostos de mercadorias', 'Pessoal (Salários e impostos)', 'Outras despesas']].sum()


if(lojas_selecionadas == "Aram"):

    # Configurar a página
    st.title('Relatório Financeiro e de Crescimento')
    st.write('Análise das ARAM no período de Outubro de 2023 a Julho de 2024.')

    # Gráfico de Barras: Vendas por Loja
    st.header('Vendas Aram')

    df_aram = df_vendas[df_vendas['Loja'] == 'ARAM']
    df_aram['Competência'] = pd.to_datetime(df_aram['Competência'], format='%d/%m/%Y')
    

    vendas_por_mes = df_aram.resample('ME', on='Competência')['Vendas'].sum().reset_index()
    vendas_por_mes['Mês'] = vendas_por_mes['Competência'].dt.strftime('%B %Y')

    fig = px.bar(vendas_por_mes, x='Mês', y='Vendas', title='Vendas Mensais da ARAM', labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
    st.plotly_chart(fig)

    st.write("""
            Comparando as vendas da ARAM de outubro de 2022 a julho de 2023 com o mesmo período em 2023-2024, observamos uma melhora significativa em quase todos os meses:

            1. **Crescimento Anual Consistente**:
            - Em outubro, as vendas de 2023 foram 17,4% maiores que em 2022 (R\$ 140.816,05 vs. R\$ 119.934,17).
            - Essa tendência de crescimento se manteve em novembro (+9%).
            - O pico de dezembro de 2023 foi 19,4% superior ao de 2022, refletindo uma forte demanda sazonal.

            2. **Recuperação Acelerada no Novo Ano**:
            - As vendas de janeiro e fevereiro de 2024 superaram as de 2023 em 44,9% e 54,2%, respectivamente, mostrando uma recuperação mais rápida após o período festivo.

            3. **Desempenho Superior na Primavera e Verão**:
            - Entre março e julho de 2024, as vendas mantiveram-se consistentemente superiores às de 2023, com maio de 2024 apresentando um crescimento de 54,3% em relação ao mesmo mês do ano anterior.

            ### Conclusão:
            A ARAM teve um crescimento anual robusto, com aumentos substanciais em praticamente todos os meses comparados. Este desempenho reforça a eficácia das estratégias de vendas e marketing adotadas em 2023-2024, destacando uma expansão sólida e consistente.
            """)
    
    fig_lucro = go.Figure()

    df_loja = df_vendas[df_vendas['Loja'] == "ARAM"]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name="Aram"))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {"ARAM"}', line=dict(dash='dash')))

    fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
    st.plotly_chart(fig_lucro)

    # Dados hipotéticos para os lucros mensais
    # Calculando variações percentuais de lucro
    pico_lucro_2022 = 83517.36
    pico_lucro_2023 = 111595.72
    variação_pico = ((pico_lucro_2023 - pico_lucro_2022) / pico_lucro_2022) * 100

    prejuízo_2023 = -50255.29
    lucro_2024 = 10462.89
    melhora_julho = ((lucro_2024 - prejuízo_2023) / abs(prejuízo_2023)) * 100

    lucro_acumulado_2022_2023 = 160758.10
    lucro_acumulado_2023_2024 = 272389.26
    crescimento_acumulado = ((lucro_acumulado_2023_2024 - lucro_acumulado_2022_2023) / lucro_acumulado_2022_2023) * 100

    st.write(f"""
    ## Análise Detalhada do Desempenho Financeiro

    Entre outubro de 2022 e julho de 2023, a ARAM alcançou um pico de lucro significativo em dezembro de R\$ {pico_lucro_2022:,.2f}, mas enfrentou um desafiador prejuízo de R\$ {prejuízo_2023:,.2f} em julho de 2023. \n
    Já em dezembro de 2023, o lucro atingiu um novo recorde de R\$ {pico_lucro_2023:,.2f}, representando um aumento de {variação_pico:.2f}% em relação ao ano anterior. Este aumento pode ser atribuído a uma gestão mais eficiente das vendas de final de ano e otimizações nas estratégias de marketing.

    A situação em julho melhorou substancialmente em 2024, com um lucro de R\$ {lucro_2024:,.2f}, marcando uma melhora impressionante de {melhora_julho:.2f}% em comparação com o prejuízo do ano anterior. Este resultado reflete uma gestão mais eficaz das despesas.

    Ao comparar os lucros acumulados dos dois períodos, observamos que o lucro total de outubro de 2023 a julho de 2024 foi de R\$ {lucro_acumulado_2023_2024:,.2f}, um aumento de {crescimento_acumulado:.2f}% sobre o lucro acumulado de R\$ {lucro_acumulado_2022_2023:,.2f} do período anterior. Esta análise sugere que, apesar de desafios pontuais, a ARAM está em uma trajetória de crescimento e estabilização financeira, adaptando-se bem às flutuações do mercado e melhorando continuamente sua eficiência operacional.
    """)


    despesas_por_loja = df_vendas.groupby('Loja')[['Aluguel', 'Energia, Água e Internet',
                                                 'Despesas Operacionais', 'Despesas Eventuais', 'Marketing',
                                                 'Impostos de mercadorias', 'Pessoal (Salários e impostos)', 'Outras despesas']].sum()

    st.write()
    st.write()

    # Filtrar despesas da loja selecionada
    despesas_loja = despesas_por_loja.loc["ARAM"]

    # Criar o gráfico de barras
    fig_despesas = px.bar(x=despesas_loja.index, y=despesas_loja.values,
                        title=f'Distribuição das Despesas - Loja {"ARAM"}',
                        labels={'x': 'Tipo de Despesa', 'y': 'Valor'})

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_despesas)


if(lojas_selecionadas == "Pátio"):
    st.title('Relatório Financeiro e de Crescimento')
    st.write('Análise das Pátio no período de Outubro de 2023 a Julho de 2024.')

    # Gráfico de Barras: Vendas por Loja
    st.header('Vendas Pátio')

    df_aram = df_vendas[df_vendas['Loja'] == 'PÁTIO']
    df_aram['Competência'] = pd.to_datetime(df_aram['Competência'], format='%d/%m/%Y')
    

    vendas_por_mes = df_aram.resample('ME', on='Competência')['Vendas'].sum().reset_index()
    vendas_por_mes['Mês'] = vendas_por_mes['Competência'].dt.strftime('%B %Y')

    fig = px.bar(vendas_por_mes, x='Mês', y='Vendas', title='Vendas Mensais do Pátio', labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
    st.plotly_chart(fig)
    st.write("""
    ### Análise Comparativa do Faturamento do Pátio

    **1. Crescimento Anual:**
    - **Outubro**: As vendas de outubro de 2023 foram 8.89% maiores que em outubro de 2022 (R\$ 63.400,90 vs. R\$ 58.225,30).
    - **Novembro**: Em novembro, o crescimento foi de 4.65%, com vendas passando de R\$ 53.367,00 em 2022 para R\$ 57.826,35 em 2023.
    - **Dezembro**: Dezembro de 2023 mostrou um aumento significativo de 9.51%, com vendas saltando de R\$ 132.896,83 para R\$ 145.538,40, indicando forte demanda sazonal.

    **2. Recuperação Acelerada no Novo Ano:**
    - **Janeiro e Fevereiro**: Janeiro de 2024 apresentou uma diminuição ligeira de 0.99% em comparação com janeiro de 2023, mas em fevereiro de 2024 houve um aumento de 12.29%, demonstrando uma recuperação robusta após o período festivo.

    - **Março a Julho**: O faturamento de março de 2024 foi menor que março de+
              2023 (-15.56%), mas a partir de abril, houve uma recuperação, com abril mostrando uma diminuição de 4.34%, maio um aumento significativo de 24.81%, junho praticamente estável (-0.86%), e julho de 2024 com um crescimento de 4.06% comparado a julho de 2023.

    ### Conclusão:
    O Pátio teve uma performance anual variável, com alguns meses mostrando um crescimento robusto, enquanto outros apresentaram pequenas reduções. A recuperação observada em maio e a estabilidade em junho e julho destacam a resiliência do negócio diante de desafios econômicos variados.

    Esta análise sugere que o Pátio poderia se beneficiar de uma estratégia de vendas e marketing que antecipa e capitaliza sobre tendências sazonais, garantindo que os esforços sejam maximizados durante os períodos de alta demanda e gerenciados de forma eficaz durante os períodos mais lentos.
    """)

    fig_lucro = go.Figure()

    df_loja = df_vendas[df_vendas['Loja'] == "PÁTIO"]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name="PÁTIO"))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {"PÁTIO"}', line=dict(dash='dash')))

    fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
    st.plotly_chart(fig_lucro)

    # Dados hipotéticos para os lucros mensais
    # Calculando variações percentuais de lucro
    pico_lucro_2022 = 83517.36
    pico_lucro_2023 = 111595.72
    variação_pico = ((pico_lucro_2023 - pico_lucro_2022) / pico_lucro_2022) * 100

    prejuízo_2023 = -50255.29
    lucro_2024 = 10462.89
    melhora_julho = ((lucro_2024 - prejuízo_2023) / abs(prejuízo_2023)) * 100

    lucro_acumulado_2022_2023 = 160758.10
    lucro_acumulado_2023_2024 = 272389.26
    crescimento_acumulado = ((lucro_acumulado_2023_2024 - lucro_acumulado_2022_2023) / lucro_acumulado_2022_2023) * 100
    # Dados de lucro (simulação dos cálculos com base nos dados fornecidos)
    lucro_acumulado_2022_2023 = sum([1644.88, -7096.64, 34441.98, -5204.88, -7525.03, 9908.93, -5215.93, 20678.70, 11562.24, 3871.20])
    lucro_acumulado_2023_2024 = sum([-9464.93, -17375.79, 26056.85, -1956.44, 4833.36, 9997.86, 9674.14, 23458.37, 13115.93, 14635.59])

    pico_lucro_2022 = 34441.98
    prejuízo_2023 = 17375.79
    pico_lucro_2023 = 26056.85
    lucro_2024 = 14635.59

    # Cálculo das variações percentuais
    variação_pico = (pico_lucro_2023 - pico_lucro_2022) / pico_lucro_2022 * 100
    melhora_julho = (lucro_2024 - prejuízo_2023) / prejuízo_2023 * 100
    crescimento_acumulado = (lucro_acumulado_2023_2024 - lucro_acumulado_2022_2023) / lucro_acumulado_2022_2023 * 100

    st.write(f"""
    ## Análise Detalhada do Desempenho Financeiro do Pátio

    Entre outubro de 2022 e julho de 2023, o Pátio enfrentou variações significativas em seu desempenho financeiro, com momentos de lucro e também de prejuízos consideráveis. O pico de lucro foi em dezembro de 2022, com R$ 34,441.98, enquanto que o maior prejuízo ocorreu em novembro de 2022, com R$ -7,096.64.

    Apesar do aumento das vendas em dezembro de 2023, o lucro alcançou R$ 26,056.85, marcando um decréscimo em comparação ao pico do ano anterior, mas ainda representando um resultado robusto para o mês.

    A situação em julho de 2024 melhorou substancialmente, registrando um lucro de R$ 14,635.59, uma recuperação notável em comparação com o prejuízo de novembro de 2023, refletindo uma gestão mais eficaz das despesas e possivelmente um aumento de vendas.

    Comparando os lucros acumulados dos períodos de outubro de 2022 a julho de 2023 com outubro de 2023 a julho de 2024, (R\$ {lucro_acumulado_2022_2023:,.2f} x R\$ {lucro_acumulado_2023_2024:,.2f}), observa-se que houve uma tendência de crescimento na capacidade do Pátio de gerar lucros mais consistentes, apesar dos desafios inerentes ao mercado e à operação.

    O Pátio está progressivamente superando seus desafios financeiros, adaptando-se às dinâmicas do mercado e aprimorando suas estratégias operacionais e comerciais. Os esforços contínuos para otimizar as operações e as abordagens de marketing devem ser mantidos para sustentar e expandir os ganhos observados.
    """)
    st.write()
    st.write()
    # Filtrar despesas da loja selecionada
    despesas_loja = despesas_por_loja.loc["PÁTIO"]

    # Criar o gráfico de barras
    fig_despesas = px.bar(x=despesas_loja.index, y=despesas_loja.values,
                        title=f'Distribuição das Despesas - Loja {"PÁTIO"}',
                        labels={'x': 'Tipo de Despesa', 'y': 'Valor'})

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_despesas)

if(lojas_selecionadas == "Artemia"):
    # Configurar a página
    st.title('Relatório Financeiro e de Crescimento')
    st.write('Análise das Artêmia no período de Outubro de 2023 a Julho de 2024.')

    # Gráfico de Barras: Vendas por Loja
    st.header('Vendas Artêmia')

    df_aram = df_vendas[df_vendas['Loja'] == 'ARTÊMIA']
    df_aram['Competência'] = pd.to_datetime(df_aram['Competência'], format='%d/%m/%Y')
    

    vendas_por_mes = df_aram.resample('ME', on='Competência')['Vendas'].sum().reset_index()
    vendas_por_mes['Mês'] = vendas_por_mes['Competência'].dt.strftime('%B %Y')

    fig = px.bar(vendas_por_mes, x='Mês', y='Vendas', title='Vendas Mensais da ARTÊMIA', labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
    st.plotly_chart(fig)

    st.write("""
        ### Análise Comparativa das Vendas da Artêmia

        **1. Crescimento Anual Consistente:**
        - **Outubro**: As vendas de outubro de 2023 foram 6.04% maiores que em outubro de 2022 (R\$ 50.222,79 vs. R\$ 47.360,50).
        - **Novembro**: Em novembro, o crescimento foi de 36.85%, com vendas passando de R\$ 37.387,60 em 2022 para R\$ 51.164,34 em 2023.
        - **Dezembro**: Dezembro de 2023 mostrou um aumento significativo de 11.42%, com vendas saltando de R\$ 113.773,52 para R\$ 126.765,81, indicando forte demanda sazonal.

        **2. Início de Ano com Desempenho Estável:**
        - **Janeiro e Fevereiro**: Janeiro de 2024 apresentou uma diminuição de 4.34% em comparação com janeiro de 2023, mas em fevereiro de 2024 houve uma pequena redução de 4.49%, demonstrando estabilidade após o período festivo.

        **3. Desempenho Superior na Primavera e Verão:**
        - **Março a Julho**: O faturamento de março de 2024 foi 5.95% maior que março de 2023. De abril a julho de 2024, as vendas apresentaram crescimentos consistentes, com destaque para maio, que teve um aumento de 24.81%. Junho e julho também mostraram aumentos consideráveis de 9.62% e 13.27%, respectivamente.

        ### Conclusão:
        Artêmia demonstrou um crescimento anual de faturamento consideravel, com aumentos substanciais em praticamente todos os meses comparados, exceto em janeiro e fevereiro onde houve pequenas reduções. Este desempenho reforça a eficácia das estratégias de vendas e marketing adotadas em 2023-2024, destacando uma expansão sólida e consistente. A empresa, apesar de "tímida", mostra que tem um grande potencial para ocupar seu espaço no mercado.
        """)

    fig_lucro = go.Figure()

    df_loja = df_vendas[df_vendas['Loja'] == "ARTÊMIA"]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name="ARTÊMIA"))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {"ARTÊMIA"}', line=dict(dash='dash')))

    fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
    st.plotly_chart(fig_lucro)

    
    st.write("""
            ### Análise Detalhada do Desempenho Financeiro da Artêmia

            **Evolução do Lucro:**
            - **Pico de Lucro**: Dezembro de 2023 apresentou um pico com R$ 50.616,54, um aumento significativo comparado a R&#36; 32.487,96 em dezembro de 2022. Este aumento reflete uma gestão eficiente das atividades operacionais durante o período de alta demanda sazonal.
            - **Recuperação**: Apesar de enfrentar prejuízos em janeiro e fevereiro de ambos os anos, houve uma diminuição nos prejuízos em 2024 (R&#36; -6.225,37 e R&#36; -8.155,08) comparado a 2023 (R\$ -14.989,87 e R\$ 5.301,17), indicando uma gestão mais eficaz das despesas operacionais.
            - **Crescimento no Meio do Ano**: A Artêmia demonstrou um crescimento notável nos meses de maio a julho de 2024 com lucros substanciais (R\$ 26.661,38 em maio, R\$ 20.354,86 em junho, e R\$ 2.643,11 em julho) comparado aos resultados do ano anterior (R\$ 15.638,13, R\$ 14.371,45, e R\$ 11.300,95, respectivamente), mostrando uma melhora consistente nas operações e estratégias de vendas.

            **Análise do Lucro Acumulado:**
            - **2022-2023**: O lucro acumulado durante este período foi de R\$ 81.429,29.
            - **2023-2024**: O lucro acumulado aumentou para R\$ 104.090,16, refletindo um crescimento de 27.82%.

            ### Conclusão:
            O desempenho financeiro da Artêmia mostra uma melhora significativa ao longo do tempo, com a empresa conseguindo não só reduzir prejuízos em meses tradicionalmente desafiadores, mas também maximizar seus lucros durante os períodos de pico. \n
            Ainda assim, precisamos pensar em estratégias para aumentar o faturamento e reduzir custos, para que tenhamos um ganho expressivo nos lucros.""")
    st.write()
    st.write()
    despesas_loja = despesas_por_loja.loc["ARTÊMIA"]

    # Criar o gráfico de barras
    fig_despesas = px.bar(x=despesas_loja.index, y=despesas_loja.values,
                        title=f'Distribuição das Despesas - Loja {"Artêmia"}',
                        labels={'x': 'Tipo de Despesa', 'y': 'Valor'})

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_despesas)
    
if (lojas_selecionadas == "Distribuição"):
    # Configurar a página
    st.title('Relatório Financeiro e de Crescimento')
    st.write('Análise das M.A no período de Outubro de 2023 a Julho de 2024.')

    # Gráfico de Barras: Vendas por Loja
    st.header('Vendas M.A')

    df_aram = df_vendas[df_vendas['Loja'] == 'MA']
    df_aram['Competência'] = pd.to_datetime(df_aram['Competência'], format='%d/%m/%Y')
    

    vendas_por_mes = df_aram.resample('ME', on='Competência')['Vendas'].sum().reset_index()
    vendas_por_mes['Mês'] = vendas_por_mes['Competência'].dt.strftime('%B %Y')

    fig = px.bar(vendas_por_mes, x='Mês', y='Vendas', title='Vendas Mensais da MA', labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
    st.plotly_chart(fig)

    st.write("""
        ### Análise Comparativa das Vendas da MA

       **1. Crescimento Anual Consistente:**
        - **Outubro**: O faturamento em outubro de 2023 foi R\$ 100.034,59, uma diminuição significativa de 37.18% comparado ao faturamento de outubro de 2022, que foi R\$ 159.319,00. Este declínio pode ser explicado de diversas formas (como reflexos de uma pré-cisão societária).
        - **Novembro**: Comparado a novembro de 2022 (R\$ 215.649,40), novembro de 2023 mostra uma diminuição para R\$ 196.243,80, refletindo uma queda de 8.99%.
        - **Dezembro**: Dezembro de 2023, com R\$ 249.441,39, exibe um aumento de 5.93% sobre dezembro de 2022 (R\$ 235.463,75).

        **2. Desempenho Estável no Início do Ano:**
        - **Janeiro a Fevereiro**: Janeiro de 2024 registra R\$ 110.219,85, que, apesar de ser menor que janeiro de 2023 (R\$ 129.815,55), ainda mostra um bom volume no início do ano, conseguindo faturar bem mesmo com o mercado frio do pós-natal. Fevereiro de 2024 apresenta uma ligeira elevação para R\$ 118.729,70 comparado a R\$ 109.283,20 de fevereiro de 2023, demonstrando estabilidade.
        
         - Importante frisar que a MA estava sem um marketing atuante nesse final de 2023 / início de 2024, o que com certeza afeta nos números do faturamento.
        **3. Crescimento Sustentado na Primavera e Verão:**
        - **Março a Julho**: O faturamento em março de 2024 alcança R\$ 191.879,59, um declínio em relação a março de 2023 (R\$ 201.914,60). No entanto, abril e maio de 2024 mostram aumentos significativos, com abril atingindo R\$ 212.747,45 (comparado a R&#36; 154.811,00 em abril de 2023) e maio R&#36; 214.606,95 (contra R\$ 196.402,30 em maio de 2023). 
             
             Junho e julho continuam essa tendência ascendente, com junho em R\$ 163.543,75 (contra R\$ 160.194,79 em 2023) e julho em R\$ 190.928,78 (comparado a R\$ 171.391,80 em 2023).

        ### Conclusão:
        A análise do faturamento da MA revela um padrão de crescimento timido, mas continuo. As variações mostram a capacidade da empresa de se adaptar e prosperar, mesmo diante de flutuações sazonais, cisão da sociedade, abertura da distribuição em Paulo Afonso, falta de mercadoria, falta de fluxo de caixa, entre outras adversidades. A resiliencia da distribuição mostra que é mais que possivel arriscar e tentar galgar outros mercados, de forma que possamos aumentar o faturamento e o lucro. 
                    """)
    
    fig_lucro = go.Figure()
    df_loja = df_vendas[df_vendas['Loja'] == "MA"]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name="MA"))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {"MA"}', line=dict(dash='dash')))

    fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
    st.plotly_chart(fig_lucro)


    st.write("""
        ### Análise Detalhada do Desempenho Financeiro da MA

        **1. Variações Mensais e Tendências de Lucro:**
        - **Outubro**: O lucro em outubro de 2023 foi de -R\$ 17.032,70, representando uma queda significativa comparado ao lucro de R\$ 29.567,79 em outubro de 2022.
        - **Novembro a Dezembro**: Houve uma recuperação em novembro de 2023 com um lucro de R\$ 34.034,68, smas ainda menor que o lucro de novembro de 2022 (R\$ 35.369,60). Em dezembro, o lucro continuou a subir para R\$ 62.450,03, excedendo os R\$ 59.757,81 de dezembro de 2022.

        **2. Crescimento Sustentado no Início do Ano:**
        - **Janeiro a Fevereiro**: Janeiro de 2024 mostrou um lucro de R\$ 5.815,74, um decréscimo em comparação a janeiro de 2023 (R\$ 24.494,18), mas ainda assim positivo. Fevereiro de 2024 teve um lucro de R\$ 14.494,76, superando os R\$ 11.097,64 de fevereiro de 2023.

        **3. Desempenho de março a junho de 2024:**
        - **Março a Julho**: Março de 2024 registrou um lucro de R\$ 38.107,28, um aumento substancial sobre R\$ 24.170,46 em março de 2023. 
                    
            Abril, maio, junho e julho de 2024 continuaram a tendência de crescimento, com abril reportando R\$ 31.652,83 (comparado a R\$ 17.016,01 em 2023), maio com R\$ 55.373,20 (superando os R\$ 32.069,87 de 2023), junho com R\$ 23.608,11 (comparado a R\$ 27.383,93 de 2023) e julho com R\$ 29.719,54 (superando significativamente os R\$ 9.815,99 de julho de 2023).

        ### Conclusão:
        A MA experimentou uma variação significativa no lucro ao longo dos meses analisados. Importante salientar que esses lucros consideram os descontos de 25% e 30% que são dados aos revendedores. Podemos dizer então que a distribuição é uma das mais lurativas do grupo (Se não a mais lucrativa.)
                    Agora, adotando estratégias para a diminuição de custos (Como a divisão dos salarios dos colaboradores entre as lojas), marketing alinhando e prospecção de negócios, a tendencia é a lucratividade aumentar ainda mais.
                    """)
    
    st.write()
    st.write()
    despesas_loja = despesas_por_loja.loc["MA"]

    # Criar o gráfico de barras
    fig_despesas = px.bar(x=despesas_loja.index, y=despesas_loja.values,
                        title=f'Distribuição das Despesas - Loja {"MA"}',
                        labels={'x': 'Tipo de Despesa', 'y': 'Valor'})

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_despesas)

if(lojas_selecionadas == "Mangara"):
    faturamento = [
    31861.59, 116335.75, 34274.65, 35094.60, 44023.95,
    48297.50, 79252.72, 63918.00, 54238.69
    ]
    lucro_acumulado_faturamento = sum(faturamento)

    # Cálculo da média de crescimento do faturamento
    crescimento_faturamento = [(j - i) / i * 100 for i, j in zip(faturamento[:-1], faturamento[1:])]
    media_crescimento_faturamento = sum(crescimento_faturamento) / len(crescimento_faturamento)

    # Primeiro st.write()

    st.header('Vendas Mangara')

    df_aram = df_vendas[df_vendas['Loja'] == 'MANGARA']
    df_aram['Competência'] = pd.to_datetime(df_aram['Competência'], format='%d/%m/%Y')
    

    vendas_por_mes = df_aram.resample('ME', on='Competência')['Vendas'].sum().reset_index()
    vendas_por_mes['Mês'] = vendas_por_mes['Competência'].dt.strftime('%B %Y')

    fig = px.bar(vendas_por_mes, x='Mês', y='Vendas', title='Vendas Mensais da Mangara', labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
    st.plotly_chart(fig)


    st.write(f"""
    ### Análise de Faturamento da Mangara

    - **Faturamento Acumulado**: R$ {lucro_acumulado_faturamento:,.2f}
    - **Média de Crescimento de Faturamento**: {media_crescimento_faturamento:.2f}%

    A Mangara mostrou uma variação significativa no faturamento ao longo dos meses, com picos notáveis em dezembro de 2023 e maio de 2024 (Natal e dia das mães). A média de crescimento, apesar de positiva, indica flutuações que precisam ser trabalhadas (talvez com uma estrategia de marketing mais direcionadas.
    """)

    # Cálculo do lucro acumulado
    lucros = [
        1444.95, 45487.94, -2030.40, -125.69, 4644.90,
        9128.17, 15288.43, 18688.16, 11205.98
    ]
    lucro_acumulado = sum(lucros)

    # Cálculo da média de crescimento do lucro
    crescimento_lucro = [(j - i) / abs(i) * 100 if i != 0 else 0 for i, j in zip(lucros[:-1], lucros[1:])]
    media_crescimento_lucro = sum(crescimento_lucro) / len(crescimento_lucro)
    
    fig_lucro = go.Figure()
    df_loja = df_vendas[df_vendas['Loja'] == "MANGARA"]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name="MANGARA"))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {"MANGARA"}', line=dict(dash='dash')))

    fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
    st.plotly_chart(fig_lucro)

    # Proposta de estratégia
    estrategia = """
    Para aumentar os lucros, a Mangara deveria focar na otimização de custos durante os meses de baixa e reforçar as estratégias de marketing e vendas antes dos picos sazonais. 
    Implementar ofertas especiais, aumentar a eficiência operacional (REDUÇÃO DE CUSTOS, PRINCIPALMENTE ALUGUEL) podem contribuir significativamente para elevar os lucros.
    """

    # Segundo st.write()
    st.write(f"""
    ### Análise de Lucro da Mangara

    - **Lucro Acumulado**: R$ {lucro_acumulado:,.2f}
    - **Média de Crescimento de Lucro**: {media_crescimento_lucro:.2f}%

    **Estratégia Proposta para Aumentar Lucros:**
    {estrategia}
""")
    st.write()
    st.write()
    despesas_loja = despesas_por_loja.loc["MANGARA"]

    # Criar o gráfico de barras
    fig_despesas = px.bar(x=despesas_loja.index, y=despesas_loja.values,
                        title=f'Distribuição das Despesas - Loja {"MANGARA"}',
                        labels={'x': 'Tipo de Despesa', 'y': 'Valor'})

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_despesas)
    
if(lojas_selecionadas == "Maia"):
    # Cálculo do lucro acumulado
    lucros_maia = [-115906.97, 8526.50, 9851.92]
    lucro_acumulado_maia = sum(lucros_maia)

    st.title('Relatório Financeiro e de Crescimento')
    st.write('Análise da Maia no período de Outubro de 2023 a Julho de 2024.')

    # Gráfico de Barras: Vendas por Loja
    st.header('Vendas Maia')

    df_aram = df_vendas[df_vendas['Loja'] == 'MAIA']
    df_aram['Competência'] = pd.to_datetime(df_aram['Competência'], format='%d/%m/%Y')
    

    vendas_por_mes = df_aram.resample('ME', on='Competência')['Vendas'].sum().reset_index()
    vendas_por_mes['Mês'] = vendas_por_mes['Competência'].dt.strftime('%B %Y')

    fig = px.bar(vendas_por_mes, x='Mês', y='Vendas', title='Vendas Mensais da MAIA', labels={'Mês': 'Mês', 'Vendas': 'Vendas'})
    st.plotly_chart(fig)

    fig_lucro = go.Figure()
    df_loja = df_vendas[df_vendas['Loja'] == "MAIA"]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name="MAIA"))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {"MAIA"}', line=dict(dash='dash')))

    fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
    st.plotly_chart(fig_lucro)
    # Proposta de estratégia para reverter prejuízos
    estrategia_reversao = """
    A Maia vem de um cenário de recente abertura de loja, registrando um primeiro mês negativo (O que é esperado, dado que os custos de abertura são muito altos). 
    Além disso, estratégias para aumentar o faturamento através de campanhas de marketing agressivas, ofertas especiais e programas de fidelidade podem ser implementadas nos meses de baixa para preparar o terreno para o pico de dezembro.
    """

    # Plano de quitação do empréstimo
    plano_quitacao = """
    Considerando o pico de vendas em dezembro, a Maia deve alocar uma porcentagem significativa do faturamento desse mês para quitar o empréstimo de R$ 247.090,57. Ajustes no fluxo de caixa para os meses antecedentes devem garantir que a empresa possa cobrir suas despesas operacionais e ainda acumular capital suficiente para abater uma grande parte do empréstimo no final do ano.
    """

    # Primeiro st.write()
    st.write(f"""
    ### Análise Financeira da Maia

    - **Lucro Acumulado (Maio a Julho 2024)**: R$ {lucro_acumulado_maia:,.2f}

    **Estratégia Proposta para Reversão de Prejuízo:**
    {estrategia_reversao}

    **Plano de Quitação do Empréstimo:**
    {plano_quitacao}
    """)

    lucro_acumulado = -115906.97 + 8526.50 + 9851.92
    saldo_devedor = 247090.57 - lucro_acumulado
    media_lucro = saldo_devedor/12


    # Cálculo baseado nas informações fornecidas
    

    st.write(f"""
    ### Plano Financeiro para Quitação de Dívida da Maia (Em 1 ano)

    - **Saldo Devedor Atual (após lucros e prejuízos)**: R$ {saldo_devedor:,.2f}
    - **Lucro Médio por Mês**: R\$ {media_lucro:,.2f}
    - **Percentual (média) de lucro por faturamento:** 18,26%
    - **Faturamento Médio Necessário por Mês para Quitação da Dívida**: R\$ {media_lucro/0.1826:,.2f}

    **Nota**: Este cálculo assume que o lucro médio recente continuará sendo gerado nos próximos meses e será adicionado ao faturamento necessário para quitar a dívida.
    """)

