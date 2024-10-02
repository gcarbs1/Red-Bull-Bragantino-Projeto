import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial.distance import braycurtis, cityblock, canberra
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from st_pages import add_page_title, hide_pages

add_page_title()
st.write('''
<p style="text-align: justify;">
Classifique jogadores com base em um amplo conjunto de métricas estatísticas e suas respectivas posições. 
Selecione a posição e as métricas de interesse, e a ferramenta irá calcular uma classificação dos jogadores, mostrando quais se aproximam mais do desempenho máximo nessas métricas.
</p>
''', unsafe_allow_html=True)
st.markdown("---")

# URLs diretas para os arquivos CSV (conteúdo bruto)
df1_url = 'https://raw.githubusercontent.com/gcarbs1/Dados-do-scraping/main/df_jogadores_br.csv'
df2_url = 'https://raw.githubusercontent.com/gcarbs1/Dados-do-scraping/main/df_jogadores_arg.csv'
df3_url = 'https://raw.githubusercontent.com/gcarbs1/Dados-do-scraping/main/df_jogadores_mex.csv'
df1_goleiros_url = 'https://raw.githubusercontent.com/gcarbs1/Dados-do-scraping/main/df_goleiros_br.csv'
df2_goleiros_url = 'https://raw.githubusercontent.com/gcarbs1/Dados-do-scraping/main/df_goleiros_arg.csv'
df3_goleiros_url = 'https://raw.githubusercontent.com/gcarbs1/Dados-do-scraping/main/df_goleiros_mex.csv'

# Carregar os dados dos jogadores e goleiros a partir das URLs
df1 = pd.read_csv(df1_url)
df2 = pd.read_csv(df2_url)
df3 = pd.read_csv(df3_url)
df1_goleiros = pd.read_csv(df1_goleiros_url)
df2_goleiros = pd.read_csv(df2_goleiros_url)
df3_goleiros = pd.read_csv(df3_goleiros_url)

def match_dtypes(df_from, df_to):
    for col in df_from.columns:
        if col in df_to.columns:
            # Tenta identificar se a coluna deve ser numérica com base em df_from
            if pd.api.types.is_numeric_dtype(df_from[col]):
                # Força a conversão para numérico, transformando valores inválidos em NaN
                df_to[col] = pd.to_numeric(df_to[col], errors='coerce')
            elif pd.api.types.is_datetime64_any_dtype(df_from[col]):
                # Força a conversão para datetime, transformando valores inválidos em NaN
                df_to[col] = pd.to_datetime(df_to[col], errors='coerce')
            else:
                # Se não for numérico nem datetime, converte para string
                df_to[col] = df_to[col].astype(str)
    return df_to

# Aplicando os tipos de df1 ao df2 e df3
df2 = match_dtypes(df1, df2)
df3 = match_dtypes(df1, df3)

# Tratamento de valores NaN
df2 = df2.fillna(0)
df3 = df3.fillna(0)

# Concatenar os dados de goleiros
df_goleiros = pd.concat([df1_goleiros, df2_goleiros, df3_goleiros], ignore_index=True)

# Função para normalizar os dados
def normalize_df(df):
    a = 0.01
    colunas_numericas = df.select_dtypes(include='number').columns
    df_normalized = df.copy()
    for col in colunas_numericas:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max - col_min != 0:
            df_normalized[col] = a + ((df[col] - col_min) / (col_max - col_min)) * (1 - a)
        else:
            df_normalized[col] = a  # Se todos os valores são iguais, define um valor padrão
    return df_normalized

# Filtro por minutos jogados (25% dos minutos máximos jogados)
min_minutes_df1 = 0.25 * df1['Minutos jogados'].max()
min_minutes_df2 = 0.25 * df2['Minutos jogados'].max()
min_minutes_df3 = 0.25 * df3['Minutos jogados'].max()
min_minutes_goleiros = 0.25 * df_goleiros['Minutos jogados'].max()

df1 = df1.loc[df1['Minutos jogados'] > min_minutes_df1]
df2 = df2.loc[df2['Minutos jogados'] > min_minutes_df2]
df3 = df3.loc[df3['Minutos jogados'] > min_minutes_df3]
df_goleiros = df_goleiros.loc[df_goleiros['Minutos jogados'] > min_minutes_goleiros]

# Informações gerais
st.header('Informações Gerais')

# Seleção do usuário para a posição do jogador
posicao = st.selectbox('Selecione a posição do jogador', ['Goleiro', 'Defensor', 'Meio-campista', 'Atacante'])

# Filtrar DataFrame com base na posição selecionada
if posicao == 'Goleiro':
    df_final = normalize_df(df_goleiros)
else:
    df1_p = df1[df1['Posição do jogador'] == posicao]
    df2_p = df2[df2['Posição do jogador'] == posicao]
    df3_p = df3[df3['Posição do jogador'] == posicao]
    df1_p = normalize_df(df1_p)
    df2_p = normalize_df(df2_p)
    df3_p = normalize_df(df3_p)
    df_final = pd.concat([df1_p, df2_p, df3_p], ignore_index=True)

colunas_para_remover = ['Posição do jogador', 'Minutos jogados']
df_final = df_final.drop(columns=colunas_para_remover, errors='ignore')

# Seleção das colunas de interesse
# Não definir colunas padrão selecionadas
colunas_interesse = st.multiselect(
    'Selecione as colunas de interesse',
    df_final.select_dtypes(include=np.number).columns.tolist(),
    default=[]
)

# Verificar se o usuário selecionou colunas
if not colunas_interesse:
    st.warning('Por favor, selecione pelo menos uma coluna de interesse.')
    st.stop()

# Agrupamento
st.header('Agrupamento')
st.write('''
<p style="text-align: justify;">
O agrupamento de variáveis permite reduzir a dimensionalidade dos dados, combinando métricas correlacionadas em componentes principais. 
Isso não é obrigatório, mas pode proporcionar uma análise mais robusta. Deixe os agrupamentos vazios se não desejar agrupar.
</p>
''', unsafe_allow_html=True)

# Definir os agrupamentos antes da filtragem
agrupamento1 = st.multiselect('Agrupamento 1', colunas_interesse, default=[], help="Deixe vazio para 'Não agrupar'")
agrupamento2 = st.multiselect('Agrupamento 2', [col for col in colunas_interesse if col not in agrupamento1], default=[], help="Deixe vazio para 'Não agrupar'")
agrupamento3 = st.multiselect('Agrupamento 3', [col for col in colunas_interesse if col not in agrupamento1 + agrupamento2], default=[], help="Deixe vazio para 'Não agrupar'")

# Verifica se o usuário agrupou as colunas
usar_agrupamento = any([agrupamento1, agrupamento2, agrupamento3])

# Função para aplicar PCA
def aplicar_pca(df, agrupamentos, n_components=1):
    pca_result = pd.DataFrame(df['Nome do jogador'], columns=['Nome do jogador'])
    for key, columns in agrupamentos.items():
        if columns:
            df_group = df[columns]
            scaler = StandardScaler()
            df_group_scaled = scaler.fit_transform(df_group)
            pca = PCA(n_components=n_components)
            pca_resultado = pca.fit_transform(df_group_scaled)
            # Rescale PCA component to be between 0.01 and 1
            component = pca_resultado[:, 0]
            # Rescale
            a = 0.01
            col_min = component.min()
            col_max = component.max()
            if col_max - col_min != 0:
                component_normalized = a + ((component - col_min) / (col_max - col_min)) * (1 - a)
            else:
                component_normalized = np.full_like(component, a)
            pca_result[key] = component_normalized
    return pca_result

# Aplicar agrupamento (PCA) se for selecionado
if usar_agrupamento:
    agrupamentos = {
        'Agrupamento 1': agrupamento1,
        'Agrupamento 2': agrupamento2,
        'Agrupamento 3': agrupamento3
    }
    df_final_filtered = df_final[['Nome do jogador'] + sum(agrupamentos.values(), [])]
    df_normalized = aplicar_pca(df_final_filtered, agrupamentos)
    # Pesos
    st.header('Pesos')
    pesos = {key: st.slider(f'Peso para {key}', min_value=0, max_value=10, value=1, step=1) for key in agrupamentos.keys() if agrupamentos[key]}
else:
    df_normalized = df_final[['Nome do jogador'] + colunas_interesse]
    # Pesos
    st.header('Pesos')
    pesos = {col: st.slider(f'Peso para {col}', min_value=0, max_value=10, value=1, step=1) for col in colunas_interesse}

# Criar 'Jogador Máximo'
numeric_columns = df_normalized.select_dtypes(include='number').columns

jogador_maximo_nome = 'Jogador Máximo'
jogador_maximo_values = {col: df_normalized[col].max() for col in numeric_columns}
jogador_maximo_values['Nome do jogador'] = jogador_maximo_nome

# Adicionar 'Jogador Máximo' ao DataFrame
df_normalized = pd.concat([df_normalized, pd.DataFrame([jogador_maximo_values])], ignore_index=True)

# Funções de similaridade
def similaridade_bray_curtis(df_normalized, jogador_maximo_nome, pesos):
    # Seleciona as colunas numéricas
    numeric_columns = df_normalized.select_dtypes(include='number').columns

    # Filtra os valores do 'Jogador Máximo'
    jogador_maximo_valores = df_normalized[df_normalized['Nome do jogador'] == jogador_maximo_nome][numeric_columns].values.flatten()

    similaridade_resultados = []

    # Itera sobre cada jogador no DataFrame
    for index, row in df_normalized.iterrows():
        nome_jogador = row['Nome do jogador']
        if nome_jogador != jogador_maximo_nome:
            jogador_valores = row[numeric_columns].values

            # Aplica os pesos às colunas
            jogador_maximo_valores_ponderados = jogador_maximo_valores * np.array([pesos[col] for col in numeric_columns])
            jogador_valores_ponderados = jogador_valores * np.array([pesos[col] for col in numeric_columns])

            # Calcula a similaridade de Bray-Curtis com os valores ponderados
            with np.errstate(divide='ignore', invalid='ignore'):
                similaridade_media = 1 - braycurtis(jogador_maximo_valores_ponderados, jogador_valores_ponderados)
                similaridade_media = np.clip(similaridade_media, 0, 1)
            similaridade_resultados.append({
                'Nome do jogador': nome_jogador,
                'Similaridade de Bray-Curtis': similaridade_media
            })

    # Cria o DataFrame com os resultados de similaridade
    df_similaridade = pd.DataFrame(similaridade_resultados)
    df_similaridade = df_similaridade.sort_values(by='Similaridade de Bray-Curtis', ascending=False).reset_index(drop=True)

    return df_similaridade

def similaridade_euclidiana(df_normalized, jogador_maximo_nome, pesos):
    # Seleciona as colunas numéricas
    numeric_columns = df_normalized.select_dtypes(include='number').columns

    # Filtra os valores do 'Jogador Máximo'
    jogador_maximo_valores = df_normalized[df_normalized['Nome do jogador'] == jogador_maximo_nome][numeric_columns].values.flatten().astype(float)

    distancia_euclidiana_resultados = []

    # Itera sobre cada jogador no DataFrame
    for index, row in df_normalized.iterrows():
        nome_jogador = row['Nome do jogador']
        if nome_jogador != jogador_maximo_nome:
            jogador_valores = row[numeric_columns].values.astype(float)

            # Aplica os pesos às colunas
            jogador_maximo_valores_ponderados = jogador_maximo_valores * np.array([pesos[col] for col in numeric_columns])
            jogador_valores_ponderados = jogador_valores * np.array([pesos[col] for col in numeric_columns])

            # Calcula a distância Euclidiana com os valores ponderados
            distancia = np.linalg.norm(jogador_maximo_valores_ponderados - jogador_valores_ponderados)
            distancia_euclidiana_resultados.append({
                'Nome do jogador': nome_jogador,
                'Distância Euclidiana': distancia
            })

    # Cria o DataFrame com os resultados de distância Euclidiana
    df_distancia_euclidiana = pd.DataFrame(distancia_euclidiana_resultados)
    max_distancia = df_distancia_euclidiana['Distância Euclidiana'].max()

    # Calcula a similaridade com base na distância Euclidiana
    df_distancia_euclidiana['Similaridade Euclidiana'] = 1 - (df_distancia_euclidiana['Distância Euclidiana'] / max_distancia)
    df_distancia_euclidiana['Similaridade Euclidiana'] = df_distancia_euclidiana['Similaridade Euclidiana'].clip(0, 1)
    df_distancia_euclidiana = df_distancia_euclidiana.drop(columns=['Distância Euclidiana'])
    df_distancia_euclidiana = df_distancia_euclidiana.sort_values(by='Similaridade Euclidiana', ascending=False).reset_index(drop=True)

    return df_distancia_euclidiana

def similaridade_cosseno(df_normalized, jogador_maximo_nome, pesos):
    # Seleciona as colunas numéricas
    numeric_columns = df_normalized.select_dtypes(include='number').columns

    # Filtra os valores do 'Jogador Máximo'
    jogador_maximo_valores = df_normalized[df_normalized['Nome do jogador'] == jogador_maximo_nome][numeric_columns].values

    # Aplica os pesos às colunas
    df_normalized_ponderado = df_normalized[numeric_columns] * np.array([pesos[col] for col in numeric_columns])
    jogador_maximo_valores_ponderados = jogador_maximo_valores * np.array([pesos[col] for col in numeric_columns])

    # Calcula a similaridade cosseno com os valores ponderados
    similaridades = cosine_similarity(df_normalized_ponderado, jogador_maximo_valores_ponderados)
    similaridades = similaridades.flatten()
    similaridades = np.clip(similaridades, 0, 1)

    # Cria o DataFrame com os resultados de similaridade
    df_similaridade_cosseno = pd.DataFrame({
        'Nome do jogador': df_normalized['Nome do jogador'],
        'Similaridade Cosseno': similaridades
    })

    # Remove o 'Jogador Máximo' do DataFrame
    df_similaridade_cosseno = df_similaridade_cosseno[df_similaridade_cosseno['Nome do jogador'] != jogador_maximo_nome]

    # Ordena os jogadores por similaridade
    df_similaridade_cosseno = df_similaridade_cosseno.sort_values(by='Similaridade Cosseno', ascending=False).reset_index(drop=True)

    return df_similaridade_cosseno

def similaridade_manhattan(df_normalized, jogador_maximo_nome, pesos):
    # Seleciona as colunas numéricas
    numeric_columns = df_normalized.select_dtypes(include='number').columns

    # Filtra os valores do 'Jogador Máximo'
    jogador_maximo_valores = df_normalized[df_normalized['Nome do jogador'] == jogador_maximo_nome][numeric_columns].values.flatten().astype(float)

    distancia_manhattan_resultados = []

    # Itera sobre cada jogador no DataFrame
    for index, row in df_normalized.iterrows():
        nome_jogador = row['Nome do jogador']
        if nome_jogador != jogador_maximo_nome:
            jogador_valores = row[numeric_columns].values.astype(float)

            # Aplica os pesos às colunas
            jogador_maximo_valores_ponderados = jogador_maximo_valores * np.array([pesos[col] for col in numeric_columns])
            jogador_valores_ponderados = jogador_valores * np.array([pesos[col] for col in numeric_columns])

            # Calcula a distância de Manhattan com os valores ponderados
            distancia = np.sum(np.abs(jogador_maximo_valores_ponderados - jogador_valores_ponderados))
            distancia_manhattan_resultados.append({
                'Nome do jogador': nome_jogador,
                'Distância Manhattan': distancia
            })

    # Cria o DataFrame com os resultados de distância Manhattan
    df_distancia_manhattan = pd.DataFrame(distancia_manhattan_resultados)
    max_distancia = df_distancia_manhattan['Distância Manhattan'].max()

    # Calcula a similaridade com base na distância Manhattan
    df_distancia_manhattan['Similaridade Manhattan'] = 1 - (df_distancia_manhattan['Distância Manhattan'] / max_distancia)
    df_distancia_manhattan['Similaridade Manhattan'] = df_distancia_manhattan['Similaridade Manhattan'].clip(0, 1)
    df_distancia_manhattan = df_distancia_manhattan.drop(columns=['Distância Manhattan'])
    df_distancia_manhattan = df_distancia_manhattan.sort_values(by='Similaridade Manhattan', ascending=False).reset_index(drop=True)

    return df_distancia_manhattan

def similaridade_canberra(df_normalized, jogador_maximo_nome, pesos):
    # Seleciona as colunas numéricas
    numeric_columns = df_normalized.select_dtypes(include='number').columns

    # Filtra os valores do 'Jogador Máximo'
    jogador_maximo_valores = df_normalized[df_normalized['Nome do jogador'] == jogador_maximo_nome][numeric_columns].values.flatten().astype(float)

    distancia_canberra_resultados = []

    # Itera sobre cada jogador no DataFrame
    for index, row in df_normalized.iterrows():
        nome_jogador = row['Nome do jogador']
        if nome_jogador != jogador_maximo_nome:
            jogador_valores = row[numeric_columns].values.astype(float)

            # Aplica os pesos às colunas
            jogador_maximo_valores_ponderados = jogador_maximo_valores * np.array([pesos[col] for col in numeric_columns])
            jogador_valores_ponderados = jogador_valores * np.array([pesos[col] for col in numeric_columns])

            # Calcula a distância Canberra com os valores ponderados
            with np.errstate(divide='ignore', invalid='ignore'):
                distancia = canberra(jogador_maximo_valores_ponderados, jogador_valores_ponderados)
                if np.isnan(distancia):
                    distancia = np.inf
            distancia_canberra_resultados.append({
                'Nome do jogador': nome_jogador,
                'Distância Canberra': distancia
            })

    # Cria o DataFrame com os resultados de distância Canberra
    df_distancia_canberra = pd.DataFrame(distancia_canberra_resultados)
    max_distancia = df_distancia_canberra['Distância Canberra'].replace(np.inf, np.nan).max()

    # Evita divisão por zero
    df_distancia_canberra['Distância Canberra'] = df_distancia_canberra['Distância Canberra'].replace(np.inf, max_distancia)
    df_distancia_canberra['Similaridade Canberra'] = 1 - (df_distancia_canberra['Distância Canberra'] / max_distancia)
    df_distancia_canberra['Similaridade Canberra'] = df_distancia_canberra['Similaridade Canberra'].clip(0, 1)
    df_distancia_canberra = df_distancia_canberra.drop(columns=['Distância Canberra'])
    df_distancia_canberra = df_distancia_canberra.sort_values(by='Similaridade Canberra', ascending=False).reset_index(drop=True)

    return df_distancia_canberra

def similaridade_kulczynski(df_normalized, jogador_maximo_nome, pesos):
    # Seleciona as colunas numéricas
    numeric_columns = df_normalized.select_dtypes(include='number').columns

    # Filtra os valores do 'Jogador Máximo'
    jogador_maximo_valores = df_normalized[df_normalized['Nome do jogador'] == jogador_maximo_nome][numeric_columns].values.flatten().astype(float)

    similaridade_kulczynski_resultados = []

    # Itera sobre cada jogador no DataFrame
    for index, row in df_normalized.iterrows():
        nome_jogador = row['Nome do jogador']
        if nome_jogador != jogador_maximo_nome:
            jogador_valores = row[numeric_columns].values.astype(float)

            # Aplica os pesos às colunas
            jogador_maximo_valores_ponderados = jogador_maximo_valores * np.array([pesos[col] for col in numeric_columns])
            jogador_valores_ponderados = jogador_valores * np.array([pesos[col] for col in numeric_columns])

            # Calcula a diferença e a soma ponderadas
            diferencas = np.abs(jogador_maximo_valores_ponderados - jogador_valores_ponderados)
            total = jogador_maximo_valores_ponderados + jogador_valores_ponderados

            # Evita divisão por zero
            with np.errstate(divide='ignore', invalid='ignore'):
                distancia = np.where(total != 0, diferencas / total, 0)
                distancia = np.nanmean(distancia)  # Ignora NaNs

            similaridade = 1 - distancia
            similaridade = np.clip(similaridade, 0, 1)
            similaridade_kulczynski_resultados.append({
                'Nome do jogador': nome_jogador,
                'Similaridade Kulczynski': similaridade
            })

    # Cria o DataFrame com os resultados de similaridade Kulczynski
    df_similaridade_kulczynski = pd.DataFrame(similaridade_kulczynski_resultados)
    df_similaridade_kulczynski = df_similaridade_kulczynski.sort_values(by='Similaridade Kulczynski', ascending=False).reset_index(drop=True)

    return df_similaridade_kulczynski

def calcular_similaridades(df_normalized, jogador_maximo_nome, pesos):
    # Chama todas as funções de similaridade
    df_similaridade_bray_curtis = similaridade_bray_curtis(df_normalized, jogador_maximo_nome, pesos).drop_duplicates(subset='Nome do jogador')
    df_similaridade_euclidiana = similaridade_euclidiana(df_normalized, jogador_maximo_nome, pesos).drop_duplicates(subset='Nome do jogador')
    df_similaridade_cosseno = similaridade_cosseno(df_normalized, jogador_maximo_nome, pesos).drop_duplicates(subset='Nome do jogador')
    df_similaridade_manhattan = similaridade_manhattan(df_normalized, jogador_maximo_nome, pesos).drop_duplicates(subset='Nome do jogador')
    df_similaridade_canberra = similaridade_canberra(df_normalized, jogador_maximo_nome, pesos).drop_duplicates(subset='Nome do jogador')
    df_similaridade_kulczynski = similaridade_kulczynski(df_normalized, jogador_maximo_nome, pesos).drop_duplicates(subset='Nome do jogador')

    # Inicia o DataFrame final com a similaridade de Bray-Curtis
    df_similaridade = df_similaridade_bray_curtis[['Nome do jogador', 'Similaridade de Bray-Curtis']]

    # Faz o merge com base na coluna 'Nome do jogador' para adicionar as demais similaridades
    df_similaridade = df_similaridade.merge(df_similaridade_euclidiana[['Nome do jogador', 'Similaridade Euclidiana']], on='Nome do jogador', how='left')
    df_similaridade = df_similaridade.merge(df_similaridade_cosseno[['Nome do jogador', 'Similaridade Cosseno']], on='Nome do jogador', how='left')
    df_similaridade = df_similaridade.merge(df_similaridade_manhattan[['Nome do jogador', 'Similaridade Manhattan']], on='Nome do jogador', how='left')
    df_similaridade = df_similaridade.merge(df_similaridade_canberra[['Nome do jogador', 'Similaridade Canberra']], on='Nome do jogador', how='left')
    df_similaridade = df_similaridade.merge(df_similaridade_kulczynski[['Nome do jogador', 'Similaridade Kulczynski']], on='Nome do jogador', how='left')

    # Definir os pesos
    peso_bray_curtis = 5
    peso_euclidiana = 1
    peso_cosseno = 1
    peso_manhattan = 1
    peso_canberra = 1
    peso_kulczynski = 1
    peso_total = peso_bray_curtis + peso_euclidiana + peso_cosseno + peso_manhattan + peso_canberra + peso_kulczynski

    # Calcula a Similaridade total (média ponderada)
    df_similaridade['Classificação'] = (
        (df_similaridade['Similaridade de Bray-Curtis'] * peso_bray_curtis) +
        (df_similaridade['Similaridade Euclidiana'].fillna(0) * peso_euclidiana) +
        (df_similaridade['Similaridade Cosseno'].fillna(0) * peso_cosseno) +
        (df_similaridade['Similaridade Manhattan'].fillna(0) * peso_manhattan) +
        (df_similaridade['Similaridade Canberra'].fillna(0) * peso_canberra) +
        (df_similaridade['Similaridade Kulczynski'].fillna(0) * peso_kulczynski)
    ) / peso_total

    # Clipa os valores de Classificação entre 0 e 1
    df_similaridade['Classificação'] = df_similaridade['Classificação'].clip(0, 1)

    # Ordena a coluna de Classificação em ordem decrescente
    df_similaridade = df_similaridade.sort_values(by='Classificação', ascending=False).reset_index(drop=True)
    
    return df_similaridade

# Interface de cálculo da classificação
if st.button('Calcular Classificação'):
    df_similaridade = calcular_similaridades(df_normalized, jogador_maximo_nome, pesos)
    
    # Ordenar o DataFrame pelos maiores valores de 'Classificação' antes de converter para string
    df_similaridade = df_similaridade.sort_values(by='Classificação', ascending=False)
    
    # Converter a coluna 'Classificação' para porcentagem com duas casas decimais
    df_similaridade['Classificação'] = (df_similaridade['Classificação'] * 100).round(2).astype(str) + '%'
    
    # Pegar os 30 maiores valores
    df_classificacao_top30 = df_similaridade.head(30)
    
    # Exibir apenas 'Nome do jogador' e 'Classificação' com maior largura
    st.dataframe(df_classificacao_top30[['Nome do jogador', 'Classificação']], use_container_width=True)

    # Exibir o DataFrame estilizado
    st.dataframe(df_classificacao_top30.style, use_container_width=True)
