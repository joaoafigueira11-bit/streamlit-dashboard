import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Análise Política",
    layout="wide"
)

# Título e Apresentação (Aula 4)
st.title("📊 Dashboard: Perfil do Eleitorado e Participação Política")
st.write("""
Este dashboard apresenta uma análise de dados públicos sobre o perfil do eleitorado, 
permitindo compreender a distribuição dos eleitores por escolaridade e faixa etária em diferentes estados.
""")

# Upload do arquivo CSV (Aula 2)
arquivo = st.file_uploader("Envia o ficheiro CSV de dados políticos", type=["csv"])

if arquivo is not None:
    # Leitura dos dados com Pandas
    df = pd.read_csv(arquivo)

    # Tratamento básico dos dados (Aula 2)
    df = df.drop_duplicates()
    if 'Escolaridade' in df.columns:
        df['Escolaridade'] = df['Escolaridade'].astype(str).str.strip()

    # Informações Gerais e Métricas (Aula 2 e Aula 3)
    st.subheader("📌 Visão Geral dos Dados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registos", df.shape[0])
    col2.metric("Quantidade de Colunas", df.shape[1])
    
    if "Total_Eleitores" in df.columns:
        soma_eleitores = df["Total_Eleitores"].sum()
        col3.metric("Total de Eleitores Analisados", f"{soma_eleitores:,.0f}".replace(",", "."))

    st.markdown("---")

    # Visualização dos dados brutos
    with st.expander("Ver primeiras linhas da base de dados"):
        st.dataframe(df.head())

    # --- GRÁFICO 1: Eleitores por Escolaridade (Aula 3) ---
    st.subheader("1. Distribuição de Eleitores por Grau de Escolaridade")
    if 'Escolaridade' in df.columns and 'Total_Eleitores' in df.columns:
        fig1 = px.bar(
            df, 
            x="Escolaridade", 
            y="Total_Eleitores", 
            color="Estado",
            barmode="group",
            title="Total de Eleitores por Escolaridade e Estado",
            labels={"Escolaridade": "Grau de Escolaridade", "Total_Eleitores": "Nº de Eleitores"}
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Explicação do Gráfico 1 (Aula 4)
        st.markdown("""
        > **O que podemos observar?**  
        > Os dados mostram que a categoria de **Ensino Médio Completo** concentra o maior volume de eleitores nas faixas analisadas em estados de grande densidade populacional, como São Paulo e Minas Gerais.  
        > Também é possível notar diferenças expressivas no volume absoluto entre os estados representados na amostra.
        """)

    st.markdown("---")

    # --- GRÁFICO 2: Distribuição por Faixa Etária (Aula 3) ---
    st.subheader("2. Composição do Eleitorado por Faixa Etária")
    if 'Faixa_Etaria' in df.columns and 'Total_Eleitores' in df.columns:
        df_etaria = df.groupby('Faixa_Etaria')['Total_Eleitores'].sum().reset_index()
        fig2 = px.pie(
            df_etaria, 
            names="Faixa_Etaria", 
            values="Total_Eleitores", 
            title="Proporção de Eleitores por Faixa Etária",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Explicação do Gráfico 2 (Aula 4)
        st.markdown("""
        > **O que podemos observar?**  
        > O gráfico em rosca demonstra o peso relativo das diferentes faixas etárias dentro do conjunto de dados analisado.  
        > Observa-se uma concentração equilibrada entre os eleitores mais jovens (18-24 anos) e as faixas etárias intermediárias.
        """)

    st.markdown("---")

    # --- EXEMPLO DE USO DA INTELIGÊNCIA ARTIFICIAL (Aula 5) ---
    st.subheader("🤖 Exemplo de Uso da Inteligência Artificial no Projeto")
    st.markdown("""
    * **Problema encontrado:** Como agrupar os dados somando o total de eleitores por faixa etária para gerar um gráfico de setores (pizza/rosca) limpo no Plotly[cite: 18, 19].
    * **Prompt utilizado:** *"Como usar o Pandas para agrupar o `Total_Eleitores` por `Faixa_Etaria` e exibir num gráfico de rosca (`px.pie`) utilizando o Streamlit?"*[cite: 12, 19]
    * **Sugestão da IA:** A IA recomendou utilizar o método `df.groupby('Faixa_Etaria')['Total_Eleitores'].sum().reset_index()` antes de passá-lo para o Plotly Express[cite: 14, 19].
    * **Validação do Grupo:** Testámos a aplicação enviando o ficheiro CSV e conferindo se a soma apresentada no indicador coincidia com a soma manual dos dados do ficheiro[cite: 17, 19, 23].
    """)

else:
    st.info("Por favor, envia um ficheiro `.csv` de política acima para iniciar o dashboard.")