import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Carregar os dados
df_vendas = pd.read_excel('analitico.xlsx')
df_crescimento = pd.read_excel('crescimentoPeriodo1Ano.xlsx')

# Configurar a página
st.title('Relatório Financeiro e de Crescimento')
st.write('Análise das lojas no período de Outubro de 2023 a Julho de 2024.')

# Gráfico de Barras: Vendas por Loja
st.header('Vendas por Loja')
vendas_loja = df_vendas.groupby('Loja')['Vendas'].sum().reset_index()
fig = px.bar(vendas_loja, x='Loja', y='Vendas', title='Vendas por Loja')
st.plotly_chart(fig)

# Gráfico de Linhas: Evolução do Lucro
st.header('Evolução do Lucro')

# Selecionar as lojas para exibir
lojas_selecionadas = st.multiselect('Escolha as lojas', options=df_vendas['Loja'].unique(), default=df_vendas['Loja'].unique())

# Filtrar o DataFrame com base nas lojas selecionadas
df_selecionado = df_vendas[df_vendas['Loja'].isin(lojas_selecionadas)]

# Criar o gráfico de linhas com as lojas selecionadas
fig_lucro = go.Figure()

for loja in lojas_selecionadas:
    df_loja = df_selecionado[df_selecionado['Loja'] == loja]
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=df_loja['Lucro'], mode='lines+markers', name=loja))

    # Adicionar linha de tendência
    z = np.polyfit(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9, df_loja['Lucro'], 1)
    p = np.poly1d(z)
    fig_lucro.add_trace(go.Scatter(x=df_loja['Competência'], y=p(pd.to_datetime(df_loja['Competência']).astype(int) / 10**9), 
                                   mode='lines', name=f'Tendência {loja}', line=dict(dash='dash')))

fig_lucro.update_layout(title='Evolução do Lucro', xaxis_title='Competência', yaxis_title='Lucro')
st.plotly_chart(fig_lucro)
st.header('Distribuição das Despesas')



despesas_por_loja = df_selecionado.groupby('Loja')[['Aluguel', 'Energia, Água e Internet',
                                                 'Despesas Operacionais', 'Despesas Eventuais', 'Marketing',
                                                 'Impostos de mercadorias', 'Pessoal (Salários e impostos)', 'Outras despesas']].sum()

# Selecionar a loja desejada
loja = st.selectbox('Escolha a loja', options=despesas_por_loja.index)

# Filtrar despesas da loja selecionada
despesas_loja = despesas_por_loja.loc[loja]

# Criar o gráfico de barras
fig_despesas = px.bar(x=despesas_loja.index, y=despesas_loja.values,
                     title=f'Distribuição das Despesas - Loja {loja}',
                     labels={'x': 'Tipo de Despesa', 'y': 'Valor'})

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_despesas)



# Gráfico de Dispersão: Correlacionando Marketing e Lucro
st.header('Marketing x Faturamento')
fig = px.scatter(df_selecionado, x='Marketing', y='Vendas', title='Correlacionando Marketing e Lucro', trendline='ols')
fig.update_traces(marker=dict(size=10, opacity=0.7))
st.plotly_chart(fig)

# Gráfico de Crescimento: Crescimento do Faturamento com seleção de Lojas e Linha de Tendência
st.header('Crescimento do Faturamento')

datas = df_crescimento.columns[1:]  # Ignorar a primeira coluna (empresa)
lojas = df_crescimento.iloc[:, 0]   # Coluna com os nomes das empresas

# Adicionar uma caixa de seleção para filtrar as lojas
lojas_selecionadas = st.multiselect('Selecione as Lojas para exibir no gráfico', options=lojas.unique(), default=lojas.unique())

fig = go.Figure()

for loja in lojas_selecionadas:
    # Filtrar as colunas para a loja selecionada
    df_loja = df_crescimento[df_crescimento.iloc[:, 0] == loja].dropna(axis=1, how='all')

    # Transpor o DataFrame para ter datas como índice
    df_loja = df_loja.set_index(df_loja.columns[0]).T

    # Adicionar a linha de crescimento da loja
    fig.add_trace(go.Scatter(x=df_loja.index, y=df_loja[loja], mode='lines+markers', name=loja))

    # Adicionar a linha de tendência
    x = np.arange(len(df_loja))
    y = df_loja[loja].values
    coef = np.polyfit(x, y, 1)
    trendline = np.polyval(coef, x)
    fig.add_trace(go.Scatter(x=df_loja.index, y=trendline, mode='lines', name=f'{loja} (Tendência)', line=dict(dash='dash')))

fig.update_layout(title='Crescimento do Faturamento (Em comparação a out/2022 ~ jul/2023)', xaxis_title='Data', yaxis_title='Faturamento')
st.plotly_chart(fig)

# Análises adicionais
st.write('Análises detalhadas a serem incluídas com base nos gráficos.')
