import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 Função para calcular a porcentagem de votos em cada bairro
def calcular_percentual(df, coluna_votos):
    total_votos = df[coluna_votos].sum()  # Soma total de votos do candidato
    df['% VOTOS'] = (df[coluna_votos] / total_votos) * 100  # Calcula a porcentagem
    df = df.rename(columns={coluna_votos: 'VOTOS_ABSOLUTOS'})  # Padroniza o nome da coluna de votos
    return df

# 📍 Carregar e processar os dados de Pedro Porto
df_pedro = pd.read_csv('Relatório_de_votos_com_coordenadas.csv')
df_pedro = df_pedro.groupby('BAIRRO', as_index=False).agg({'PEDRO PORTO 2024 1T': 'sum'})
df_pedro = calcular_percentual(df_pedro, 'PEDRO PORTO 2024 1T')
df_pedro['CANDIDATO'] = 'Pedro Porto'

# 📍 Carregar e processar os dados de Martha Rocha
df_martha = pd.read_csv('martha_rocha_com_coordenadas.csv')
df_martha = calcular_percentual(df_martha, 'Votos Absolutos')
df_martha['CANDIDATO'] = 'Martha Rocha'

# 📍 Carregar e processar os dados de Ciro Gomes
df_ciro = pd.read_csv('ciro_com_coordenadas.csv')
df_ciro = calcular_percentual(df_ciro, 'Votos Absolutos')
df_ciro['CANDIDATO'] = 'Ciro Gomes'

# 🔹 Padronizar a coluna de bairros nos três DataFrames
df_martha = df_martha.rename(columns={'Bairro': 'BAIRRO'})
df_ciro = df_ciro.rename(columns={'Bairro': 'BAIRRO'})

# 🔹 Criar um DataFrame com todos os bairros presentes em qualquer um dos candidatos
bairros_unicos = pd.DataFrame({'BAIRRO': sorted(set(df_pedro['BAIRRO']) | set(df_martha['BAIRRO']) | set(df_ciro['BAIRRO']))})

# 🔹 Fazer um merge para garantir que todos os bairros estejam nos três DataFrames
df_pedro = bairros_unicos.merge(df_pedro, on='BAIRRO', how='left')
df_martha = bairros_unicos.merge(df_martha, on='BAIRRO', how='left')
df_ciro = bairros_unicos.merge(df_ciro, on='BAIRRO', how='left')

# 🔹 Unir os três DataFrames corretamente
df_total = pd.concat([df_pedro, df_martha, df_ciro], ignore_index=True)

# 🔹 Mapeamento fixo de cores para cada candidato
cores_candidatos = {
    'Pedro Porto': 'green',  # Verde
    'Martha Rocha': 'blue',  # Azul
    'Ciro Gomes': 'yellow'   # Amarelo
}

# 🔹 Layout do Streamlit
st.title('Comparação de Votação por Bairro - Scatterplot')

# Dropdown para selecionar os candidatos a serem comparados
candidatos_selecionados = st.multiselect(
    "Selecione os candidatos",
    options=['Pedro Porto', 'Martha Rocha', 'Ciro Gomes'],
    default=['Pedro Porto', 'Martha Rocha', 'Ciro Gomes']
)

# Filtrar os dados com base na seleção
df_filtrado = df_total[df_total['CANDIDATO'].isin(candidatos_selecionados)]

# Criar o scatterplot com linhas conectando os pontos
fig = px.line(
    df_filtrado,
    x='BAIRRO',
    y='% VOTOS',
    color='CANDIDATO',
    markers=True,  # Adiciona bolinhas nos pontos
    color_discrete_map=cores_candidatos,  # Mapeamento de cores fixo
    title="Comparação de Votação por Bairro - Scatterplot",
    category_orders={"BAIRRO": df_total['BAIRRO'].unique()}  # Ordena os bairros corretamente
)

# Ajustar o tamanho das bolinhas proporcional à porcentagem de votos
fig.update_traces(marker=dict(size=df_filtrado['% VOTOS'] * 2))

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
