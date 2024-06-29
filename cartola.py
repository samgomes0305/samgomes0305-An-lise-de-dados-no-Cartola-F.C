import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Dados fornecidos
data = {
    'Nome do Participante': ['TropadaQuadra', 'KeynesMarx', 'Exodia47', 'Club de Regatas Parque Real', 'Giulia FR', 'Burkina Faso AC', 'Timoneiro Luis Inácio FC', 'FluBomba', 'TJBEZO', 'Motomami AC', 'Timesocafofo'],
    'Rodada 1': [44.82, 61.92, 56.13, 50.23, 40.10, 0, 30.38, 64.41, 47.28, 0, 0],
    'Rodada 2': [49.05, 57.91, 61.18, 29.90, 46.90, 23.34, 37.74, 21.90, 58.75, 0, 0],
    'Rodada 3': [68.60, 59.80, 41.50, 29.67, 42.37, 34.05, 58.67, 54.53, 66.76, 0, 0],
    'Rodada 4': [52.92, 47.00, 22.61, 61.40, 19.11, 35.09, 28.56, 38.59, 29.06, 0, 0],
    'Rodada 5': [77.74, 50.93, 67.37, 48.53, 52.28, 88.78, 24.14, 47.15, 32.93, 0, 0],
    'Rodada 6': [93.62, 67.17, 72.01, 84.52, 59.50, 59.92, 54.91, 45.96, 33.10, 0, 0],
    'Rodada 7': [46.06, 80.47, 88.53, 35.98, 51.33, 50.13, 60.15, 16.41, 47.35, 0, 0],
    'Rodada 8': [93.70, 41.45, 56.13, 79.43, 62.00, 60.88, 60.00, 76.73, 46.32, 0, 0],
    'Rodada 9': [64.04, 54.63, 36.84, 48.28, 55.03, 40.33, 31.88, 18.94, 14.24, 0, 0],
    'Rodada 10': [52.15, 67.40, 93.56, 77.82, 77.57, 105.27, 38.67, 28.85, 34.42, 0, 0],
    'Rodada 11': [74.07, 68.46, 55.02, 68.07, 65.00, 37.16, 62.26, 32.30, 36.27, 0, 0],
    'Rodada 12': [49.10, 65.60, 39.05, 51.98, 54.31, 61.86, 52.40, 46.51, 37.95, 35.52, 52.48] 
}

df = pd.DataFrame(data)
df.set_index('Nome do Participante', inplace=True)

# Streamlit interface
st.title('Gráfico de Pontuação no Cartola')

participantes = df.index.tolist()
selecionados = st.multiselect('Selecione os Participantes', participantes, default=participantes)

# Filtrar DataFrame
df_selecionados = df.loc[selecionados]

# Criação do gráfico
fig = go.Figure()

for participante in selecionados:
    fig.add_trace(go.Scatter(
        x=df.columns,  # Rodadas
        y=df.loc[participante],
        mode='lines+markers',
        name=participante
    ))

fig.update_layout(
    title='Evolução das Pontuações por Rodada',
    xaxis_title='Rodadas',
    yaxis_title='Pontos',
    template='plotly_dark'
)

st.plotly_chart(fig)

# Adicionar opções de estatísticas
stat_option = st.selectbox(
    'Escolha a estatística para exibir',
    ('Menor Pontuação', 'Maior Pontuação', 'Média de Pontuação', 'Total de Pontuação', 'Comparação com a Média do Grupo', 'Comparação com a Mediana do Grupo', 'Média nos Últimos 3 Jogos', 'Regularidade (Desvio Padrão)')
)

if stat_option == 'Menor Pontuação':
    stat_df = df_selecionados.min(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Menor Pontuação']
elif stat_option == 'Maior Pontuação':
    stat_df = df_selecionados.max(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Maior Pontuação']
elif stat_option == 'Média de Pontuação':
    stat_df = df_selecionados.mean(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Média de Pontuação']
    stat_df['Média de Pontuação'] = stat_df['Média de Pontuação'].round(2)
elif stat_option == 'Total de Pontuação':
    stat_df = df_selecionados.sum(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Total de Pontuação']
elif stat_option == 'Comparação com a Média do Grupo':
    media_grupo = df.mean(axis=1).mean()
    stat_df = df_selecionados.mean(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Média do Participante']
    stat_df['Comparação com a Média do Grupo'] = stat_df['Média do Participante'] - media_grupo
    stat_df['Comparação com a Média do Grupo'] = stat_df['Comparação com a Média do Grupo'].round(2)
elif stat_option == 'Comparação com a Mediana do Grupo':
    mediana_grupo = df.mean(axis=1).median()
    stat_df = df_selecionados.mean(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Média do Participante']
    stat_df['Comparação com a Mediana do Grupo'] = stat_df['Média do Participante'] - mediana_grupo
    stat_df['Comparação com a Mediana do Grupo'] = stat_df['Comparação com a Mediana do Grupo'].round(2)
elif stat_option == 'Média nos Últimos 3 Jogos':
    stat_df = df_selecionados.iloc[:, -3:].mean(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Média nos Últimos 3 Jogos']
    stat_df['Média nos Últimos 3 Jogos'] = stat_df['Média nos Últimos 3 Jogos'].round(2)
elif stat_option == 'Regularidade (Desvio Padrão)':
    stat_df = df_selecionados.std(axis=1).reset_index()
    stat_df.columns = ['Nome do Participante', 'Desvio Padrão']
    stat_df['Desvio Padrão'] = stat_df['Desvio Padrão'].round(2)

# Exibir DataFrame sem índice
st.dataframe(stat_df)
