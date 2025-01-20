import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import farol

# Função para criar o front-end
def main():
    st.title("Farol do Saneamento - Receita")
    st.write("Bem-vindo ao Farol do Saneamento! Aqui você pode ajustar as premissas e visualizar as projeções de receita.")

    # Configurações iniciais das premissas
    premissas = {
        'Populacao_inicial': st.number_input('População inicial', value=2675656, step=1000),
        'CAGR_pop': st.number_input('CAGR População (%)', value=0.0091, step=0.0001, format="%.4f"),
        'CAGR_domicilio': st.number_input('CAGR Domicílio (%)', value=-0.003, step=0.0001, format="%.4f"),
        'Indice_atend_agua': st.slider('Índice de Atendimento Água', 0.0, 1.0, value=0.7),
        'Indice_atend_esg': st.slider('Índice de Atendimento Esgoto', 0.0, 1.0, value=0.2),
        'Indice_meta_agua': st.slider('Índice Meta Água', 0.0, 1.0, value=0.99),
        'Indice_meta_esg': st.slider('Índice Meta Esgoto', 0.0, 1.0, value=0.95),
        'Ano_meta_agua': st.number_input('Ano Meta Água', value=10, step=1),
        'Ano_meta_esg': st.number_input('Ano Meta Esgoto', value=15, step=1),
        'Consumo_per_capita': st.number_input('Consumo per Capita (litros/dia)', value=150.0, step=1.0),
        'Consumo_alvo': st.number_input('Consumo Alvo (litros/dia)', value=180, step=1),
        'Relacao_vol_fat_med': st.number_input('Relação Volume Faturado/Medido', value=1.2, step=0.1, format="%.1f"),
        'Tarifa_media': st.number_input('Tarifa Média Água', value=6.15, step=0.1, format="%.2f"),
        'Tarifa_media_esg': st.number_input('Tarifa Média Esgoto', value=7.0, step=0.1, format="%.2f"),
        'Tarifa_alvo': st.number_input('Tarifa Alvo', value=8.5, step=0.1, format="%.2f"),
        'Tx_ocupacao': st.number_input('Taxa de Ocupação (pessoas/domicílio)', value=3.03, step=0.01, format="%.2f"),
        'Share_eco_res': st.number_input('Share de Economia Residencial', value=0.92, step=0.01, format="%.2f"),
        'rel_fat_esg_ag': st.number_input('Relação Faturamento Esgoto/Água', value=0.8, step=0.1, format="%.1f")
    }

    # Configuração de anos de projeção
    anos = st.number_input('Número de anos de projeção', value=35, step=1)

    # Botão para gerar projeção
    if st.button("Gerar Projeção"):
        # Chamada da função projetar_receitas
        df = farol.projetar_receitas(anos, premissas)

        # Exibir tabela de resultados
        st.write("### Resultados da Projeção")
        st.dataframe(df)

        # Criar gráficos de receita
        st.write("### Gráfico de Receitas")
        plt.figure(figsize=(10, 6))
        plt.plot(df['Ano'], df['Receita_bruta'], label='Receita Bruta Água')
        plt.plot(df['Ano'], df['Receita_bruta_esg'], label='Receita Bruta Esgoto')
        plt.xlabel('Ano')
        plt.ylabel('Receita Bruta')
        plt.title('Projeção de Receitas')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

# Certifique-se de que a função projetar_receitas está importada no mesmo escopo
if __name__ == "__main__":
    main()