import pandas as pd
import numpy as np
import openpyxl

# Função para projetar os dados com base nas fórmulas fornecidas
def projetar_receitas(anos, premissas):
    # Criar DataFrame para armazenar os resultados
    df = pd.DataFrame({'Ano': range(anos + 1)})
    



    # Premissas iniciais
    df['CAGR_pop'] = premissas['CAGR_pop']
    df['Populacao'] = premissas['Populacao_inicial']
    df['CAGR_domicilio'] = premissas['CAGR_domicilio']
    df['Tx_ocupacao'] = premissas['Tx_ocupacao']
    df['Share_eco_res'] = premissas['Share_eco_res']
    df['Indice_atend_agua'] = premissas['Indice_atend_agua']
    df['Consumo_per_capita'] = premissas['Consumo_per_capita']
    df['Rel_vol_fat_med'] = premissas['Relacao_vol_fat_med']
    df['Tarifa_media'] = premissas['Tarifa_media']
    

    
    df['Indice_atend_esg'] = premissas['Indice_atend_esg']
    df['Tarifa_media_esg'] = premissas['Tarifa_media_esg']
    df['rel_fat_esg_ag']=premissas['rel_fat_esg_ag']

    
    # Cálculos para o ano 0
    df.loc[0, 'Domicilios'] = df.loc[0, 'Populacao'] / df.loc[0, 'Tx_ocupacao']
    df.loc[0, 'Eco_total'] = df.loc[0, 'Domicilios'] / df.loc[0, 'Share_eco_res']
    df.loc[0, 'Pop_atend_agua'] = df.loc[0, 'Populacao'] * df.loc[0, 'Indice_atend_agua']
    df.loc[0, 'Dom_atend_agua'] = df.loc[0, 'Pop_atend_agua'] / df.loc[0, 'Tx_ocupacao']
    df.loc[0, 'Total_economias'] = df.loc[0, 'Dom_atend_agua'] / df.loc[0, 'Share_eco_res']
    df.loc[0, 'Vol_consumido'] = df.loc[0, 'Pop_atend_agua'] * df.loc[0, 'Consumo_per_capita'] * 365 / 1000
    df.loc[0, 'Vol_eco'] = df.loc[0, 'Vol_consumido'] / df.loc[0, 'Total_economias'] / 12
    df.loc[0, 'Vol_fat'] = df.loc[0, 'Vol_consumido'] * df.loc[0, 'Rel_vol_fat_med']
    df.loc[0, 'Receita_bruta'] = df.loc[0, 'Vol_fat'] * df.loc[0, 'Tarifa_media']
    
    df.loc[0, 'Pop_atend_esg'] = df.loc[0, 'Populacao'] * df.loc[0, 'Indice_atend_esg']
    df.loc[0, 'Dom_atend_esg'] = df.loc[0, 'Pop_atend_esg'] / df.loc[0, 'Tx_ocupacao']
    df.loc[0, 'Total_economias_esg'] = df.loc[0, 'Dom_atend_esg'] / df.loc[0, 'Share_eco_res']
    df.loc[0, 'Vol_consumido_lig_esg'] = df.loc[0, 'Pop_atend_esg'] * df.loc[0, 'Consumo_per_capita'] * 365 / 1000
    df.loc[0, 'Vol_fat_esg'] = df.loc[0, 'Vol_consumido_lig_esg']* df.loc[0, 'Rel_vol_fat_med']*df.loc[0,'rel_fat_esg_ag']
    df.loc[0, 'Receita_bruta_esg'] = df.loc[0, 'Vol_fat_esg'] * df.loc[0, 'Tarifa_media_esg']
    df.loc[0, 'Receita_bruta_total'] = df.loc[0, 'Receita_bruta'] + df.loc[0, 'Receita_bruta_esg']
    

    

    

    # Projeção para os anos seguintes
    for ano in range(1, anos + 1):
        df.loc[ano, 'CAGR_pop'] = np.select([
            (1 <= ano) & (ano <= 5),
            (5 < ano) & (ano <= 10),
            (10 < ano) & (ano <= 15)
        ], [
            premissas['CAGR_pop'] * (1 - 0.5),
            premissas['CAGR_pop'] * (1 - 0.75),
            premissas['CAGR_pop'] * (1 - 0.95)
        ], default=0)

        df.loc[ano, 'Populacao'] = df.loc[ano - 1, 'Populacao'] * (1 + df.loc[ano, 'CAGR_pop'])

        df.loc[ano, 'CAGR_domicilio'] = np.select([
            (1 <= ano) & (ano <= 5),
            (5 < ano) & (ano <= 10),
            (10 < ano) & (ano <= 15)
        ], [
            premissas['CAGR_domicilio'] * (1 + 0.3),
            premissas['CAGR_domicilio'] * (1 + 0.6),
            premissas['CAGR_domicilio'] * (1 + 1.2)
        ], default=0)

        df.loc[ano, 'Tx_ocupacao'] = df.loc[ano - 1, 'Tx_ocupacao'] * (1 + df.loc[ano, 'CAGR_domicilio'])

        df.loc[ano, 'Domicilios'] = df.loc[ano, 'Populacao'] / df.loc[ano, 'Tx_ocupacao']
        df.loc[ano, 'Eco_total'] = df.loc[ano, 'Domicilios'] / df.loc[ano - 1, 'Share_eco_res']

        df.loc[ano, 'Indice_atend_agua'] = np.where(
            ano <= premissas['Ano_meta_agua'],
            df.loc[ano - 1, 'Indice_atend_agua']  + (premissas['Indice_meta_agua'] - premissas['Indice_atend_agua']) / premissas['Ano_meta_agua'],
            premissas['Indice_meta_agua']
        )
        df.loc[ano, 'Pop_atend_agua'] = df.loc[ano, 'Populacao'] * df.loc[ano, 'Indice_atend_agua']
        df.loc[ano, 'Dom_atend_agua'] = df.loc[ano, 'Pop_atend_agua'] / df.loc[ano, 'Tx_ocupacao']
        df.loc[ano, 'Total_economias'] = df.loc[ano, 'Dom_atend_agua'] / df.loc[ano, 'Share_eco_res']

        df.loc[ano, 'Consumo_per_capita'] = np.where(
            ano <= premissas['Ano_meta_agua'],
            df.loc[ano -1,  'Consumo_per_capita'] + (premissas['Consumo_alvo'] - premissas['Consumo_per_capita']) / premissas['Ano_meta_agua'],
            premissas['Consumo_alvo']
        )
        df.loc[ano, 'Vol_consumido'] = df.loc[ano, 'Pop_atend_agua'] * df.loc[ano, 'Consumo_per_capita'] * 365 / 1000
        df.loc[ano, 'Vol_eco'] = df.loc[ano, 'Vol_consumido'] / df.loc[ano, 'Total_economias'] / 12

        df.loc[ano, 'Rel_vol_fat_med'] = premissas['Relacao_vol_fat_med']
        df.loc[ano, 'Vol_fat'] = df.loc[ano, 'Vol_consumido']* df.loc[ano, 'Rel_vol_fat_med']

        df.loc[ano, 'Tarifa_media'] = np.where(
            ano <= premissas['Ano_meta_agua'],
            df.loc[ano - 1, 'Tarifa_media'] + (premissas['Tarifa_alvo'] - premissas['Tarifa_media']) / premissas['Ano_meta_agua'],
            premissas['Tarifa_alvo']
        )
        df.loc[ano, 'Receita_bruta'] = df.loc[ano, 'Vol_fat'] * df.loc[ano, 'Tarifa_media']



        df.loc[ano, 'Indice_atend_esg'] = np.where(
            ano <= premissas['Ano_meta_esg'],
            df.loc[ano - 1, 'Indice_atend_esg']  + (premissas['Indice_meta_esg'] - premissas['Indice_atend_esg']) / premissas['Ano_meta_esg'],
            premissas['Indice_meta_esg']
        )

        df.loc[ano, 'Tarifa_media_esg'] = np.where(
            ano <= premissas['Ano_meta_esg'],
            df.loc[ano - 1, 'Tarifa_media_esg'] + (premissas['Tarifa_alvo'] - premissas['Tarifa_media_esg']) / premissas['Ano_meta_esg'],
            premissas['Tarifa_alvo']
        )

        df.loc[ano, 'Pop_atend_esg'] = df.loc[ano, 'Populacao'] * df.loc[ano, 'Indice_atend_esg']
        df.loc[ano, 'Dom_atend_esg'] = df.loc[ano, 'Pop_atend_esg'] / df.loc[ano, 'Tx_ocupacao']
        df.loc[ano, 'Total_economias_esg'] = df.loc[ano, 'Dom_atend_esg'] / df.loc[ano, 'Share_eco_res']
        df.loc[ano, 'Vol_consumido_lig_esg'] = df.loc[ano, 'Pop_atend_esg'] * df.loc[ano, 'Consumo_per_capita'] * 365 / 1000
        df.loc[ano, 'Vol_fat_esg'] = df.loc[ano, 'Vol_consumido_lig_esg']* df.loc[ano, 'Rel_vol_fat_med']*df.loc[ano,'rel_fat_esg_ag']
        df.loc[ano, 'Receita_bruta_esg'] = df.loc[ano, 'Vol_fat_esg'] * df.loc[ano, 'Tarifa_media_esg']
        df.loc[ano, 'Receita_bruta_total'] = df.loc[ano, 'Receita_bruta'] + df.loc[ano, 'Receita_bruta_esg']

        



    return df

# Definir premissas iniciais
premissas = {
    'Populacao_inicial': 2675656,
    'CAGR_pop': 0.0091,
    'CAGR_domicilio': -0.003,
    'Indice_atend_agua': 0.7,
    'Indice_atend_esg': 0.2,
    'Indice_meta_agua': 0.99,
    'Indice_meta_esg': 0.95,
    'Ano_meta_agua': 10,
    'Ano_meta_esg': 15,
    'Consumo_per_capita': 150.0,
    'Consumo_alvo': 180,
    'Relacao_vol_fat_med': 1.2,
    'Tarifa_media': 6.15,
    'Tarifa_media_esg': 7.0,
    'Tarifa_alvo': 8.5,
    'Tx_ocupacao':3.03,
    'Share_eco_res':  0.92,
    'rel_fat_esg_ag':0.8
    
    
    
}


# Executar projeção para 35 anos
resultado = projetar_receitas(35, premissas)

# resultado.head(20)

# resultado.info()

# resultado['Receita_bruta'].sum()
# resultado['Receita_bruta_total'].sum()
# Exibir os resultados


# Salvar os resultados em um arquivo Excel
resultado.to_excel(r'C:\Users\Luiz Antonio Lopes\consultoria\proj_python\outputs\outputs_20012025.xlsx', index=False)



