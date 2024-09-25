import pandas as pd
import matplotlib.pyplot as plt
import os
pasta_graficos = 'graficos'
os.makedirs(pasta_graficos, exist_ok=True)
# Ler o arquivo CSV local
df = pd.read_csv('CAMADASATERRO.csv', delimiter=';', skiprows=0, encoding='latin-1')

# Exibir as primeiras linhas do DataFrame
print(df.head())

# Selecionar as colunas necessárias
df = df[['Local do Ensaio', 'Praça', 'Estaca Inicial', 'Estaca Final', 'Camada (Nº)']]

# Preencher valores ausentes com 0
df = df.fillna(0)

# Converter as colunas 'Estaca Inicial' e 'Estaca Final' para numérico
df['Estaca Inicial'] = pd.to_numeric(df['Estaca Inicial'], errors='coerce').fillna(0)
df['Estaca Final'] = pd.to_numeric(df['Estaca Final'], errors='coerce').fillna(0)

# Garantir que a coluna 'Camada (Nº)' é do tipo string
df['Camada (Nº)'] = df['Camada (Nº)'].astype(str)

# Definir uma lista de cores para as camadas
cores_camadas = ['blue', 'green', 'red', 'orange', 'purple', 'cyan']  # Adicione mais cores se necessário

# Obter uma lista de locais únicos
locais_unicos = df['Local do Ensaio'].unique()

# Criar gráficos separados para cada local de ensaio
for local in locais_unicos:
    # Filtrar o DataFrame para o local atual
    df_local = df[df['Local do Ensaio'] == local]
    
    # Obter uma lista de praças únicas dentro do local
    praças_unicas = df_local['Praça'].unique()

    # Criar gráficos separados para cada praça
    for praça in praças_unicas:
        # Filtrar o DataFrame para a praça atual
        df_praça = df_local[df_local['Praça'] == praça]

        # Garantir que há pelo menos 5 camadas
        camadas_padrao = ['1ª', '2ª', '3ª', '4ª', '5ª']  # Definindo as camadas padrão
        camadas_existentes = df_praça['Camada (Nº)'].unique()

        for camada in camadas_padrao:
            if camada not in camadas_existentes:
                # Adiciona uma camada vazia
                nova_linha = pd.DataFrame({
                    'Local do Ensaio': [local],
                    'Praça': [praça],
                    'Estaca Inicial': [0],
                    'Estaca Final': [0],
                    'Camada (Nº)': [camada]  # Garantindo que seja string
                })
                df_praça = pd.concat([df_praça, nova_linha], ignore_index=True)

        # Reordenar o DataFrame de acordo com as camadas padrão
        df_praça['Camada (Nº)'] = pd.Categorical(df_praça['Camada (Nº)'], categories=camadas_padrao, ordered=True)
        df_praça = df_praça.sort_values('Camada (Nº)')

        # Criar figura e eixos
        fig, ax = plt.subplots(figsize=(12, 8))

        # Adicionar barras horizontais para cada linha do dataframe filtrado
        for i, row in df_praça.iterrows():
            # Garantir que o valor é uma string antes de aplicar replace
            camada_str = str(row['Camada (Nº)']).replace('ª', '')  # Remover 'ª'
            camada_index = int(camada_str) - 1 if camada_str.isdigit() else 0  # Ajustar para 0-index
            ax.barh(
                y=f"{row['Local do Ensaio']} - {row['Praça']} - Camada {row['Camada (Nº)']}",
                width=row['Estaca Final'] - row['Estaca Inicial'],
                left=row['Estaca Inicial'],
                color=cores_camadas[camada_index % len(cores_camadas)],  # Alternar cores com base na camada
                edgecolor='black'
            )

        # Personalização do gráfico
        ax.set_xlabel('Estaca')
        ax.set_ylabel('Local do Ensaio - Praça - Camada')
        ax.set_title(f'Gráfico de Intervalos para {local} - {praça}')
        
        # Definir limites do eixo X
        ax.set_xlim(left=0)  # Começar em 0
        ax.set_xticks(range(0, int(df_praça['Estaca Final'].max()) + 10, 10))  # Ajustar para um intervalo de 10, se necessário
        plt.grid(True)

        # Salvar gráfico
        print("salvando imagem")
        plt.savefig(f'{pasta_graficos}/{local} - {praça}.png')  # Salvar a imagem
        #plt.show()  # Mostrar gráfico
