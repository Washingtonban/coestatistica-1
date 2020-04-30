import streamlit as st
import pandas as pd
import altair as alt


def main():
    st.sidebar.title('AceleraDev - Data Science')
    st.sidebar.image('./image/logo.png', use_column_width=True)
    file = st.sidebar.file_uploader('Escolha a base de dados que deseja analisar (.csv)', type='csv')
    if file is None:
        st.title('Insira um arquivo CSV para começar')
        st.image('./image/rick.gif', use_column_width=True)
    if file is not None:
        tratamento = st.sidebar.selectbox('Selecione a coluna :', ('Introdução', 'Visualizar Data Frame',
                                                                   'Estatistica', 'Visualizando dados'))
        if tratamento == 'Introdução':
            if file is not None:
                linkedin = 'https://www.linkedin.com/in/washingtonban/'
                github = 'https://github.com/Washingtonban'
                st.title('Aplicativo de analise de dados')
                st.subheader('Desenvolvido por Washington Barbosa')
                st.subheader(f'Linkedin: {linkedin}')
                st.subheader(f'Github: {github}')
                st.image('./image/ds.gif', use_column_width=True)


        elif tratamento == 'Visualizar Data Frame':
            if file is not None:
                st.title('Visualização do Data Frame')
                slider = st.slider('Valores', 1, 100)
                df = pd.read_csv(file)
                st.markdown('Data Frame')
                st.dataframe(df.head(slider))

        elif tratamento == 'Estatistica':
            if file is not None:
                st.sidebar.text('Configurando Estatística descritiva')
                st.title('Resultado Estatística descritiva')
                df = pd.read_csv(file)
                aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
                colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
                col = st.sidebar.selectbox('Selecione a coluna :', colunas_numericas)
                if col is not None:
                    st.sidebar.markdown('Selecione o que deseja analisar :')
                    mean = st.sidebar.checkbox('Média')
                    if mean:
                        st.subheader(f'A média da {col} é: {df[col].mean()}' )
                    median = st.sidebar.checkbox('Mediana')
                    if median:
                        st.subheader(f'A mediana da {col} é: {df[col].median()}')
                    desvio_pad = st.sidebar.checkbox('Desvio padrão')
                    if desvio_pad:
                        st.subheader(f'O desvio padrão da {col} é: {df[col].std()}')
                    kurtosis = st.sidebar.checkbox('Kurtosis')
                    if kurtosis:
                        st.subheader(f'O calculo do kurtosis da {col} é: {df[col].kurtosis()}')
                    skewness = st.sidebar.checkbox('Skewness')
                    if skewness:
                        st.subheader(f'O Calculo do skewness da {col} é: {df[col].skew()}')
                    describe = st.sidebar.checkbox('Describe')
                    if describe:
                        st.subheader(f'A descrição da {col} é:')
                        st.table(df[colunas_numericas].describe().transpose())
        elif tratamento == 'Visualizando dados':
            if file is not None:
                st.title('Analisando os dados')
                df = pd.read_csv(file)
                aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
                colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
                colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
                colunas = list(df.columns)
                st.sidebar.subheader('Visualização dos dados')
                st.sidebar.markdown('Selecione a visualizacao:')
                histograma = st.sidebar.checkbox('Histograma')
                if histograma:
                    st.subheader('Histograma:')
                    col_num = st.selectbox('Selecione a Coluna Numerica: ', colunas_numericas, key='unique')
                    st.markdown('Histograma da coluna : ' + str(col_num))
                    st.write(criar_histograma(col_num, df))
                barras = st.sidebar.checkbox('Gráfico de barras')
                if barras:
                    st.subheader('Grafico de barras:')
                    col_num_barras = st.selectbox('Selecione a coluna numerica: ', colunas_numericas, key='unique')
                    col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key='unique')
                    st.markdown('Gráfico de barras da coluna ' + str(col_cat_barras) + ' pela coluna ' + col_num_barras)
                    st.write(criar_barras(col_num_barras, col_cat_barras, df))
                boxplot = st.sidebar.checkbox('Boxplot')
                if boxplot:
                    st.subheader('Boxplot:')
                    col_num_box = st.selectbox('Selecione a Coluna Numerica:', colunas_numericas, key='unique')
                    col_cat_box = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key='unique')
                    st.markdown('Boxplot ' + str(col_cat_box) + ' pela coluna ' + col_num_box)
                    st.write(criar_boxplot(col_num_box, col_cat_box, df))
                scatter = st.sidebar.checkbox('Scatterplot')
                if scatter:
                    st.subheader('Scatterplot:')
                    col_num_x = st.selectbox('Selecione o valor de x ', colunas_numericas, key='unique')
                    col_num_y = st.selectbox('Selecione o valor de y ', colunas_numericas, key='unique')
                    col_color = st.selectbox('Selecione a coluna para cor', colunas)
                    st.markdown('Selecione os valores de x e y')
                    st.write(criar_scatterplot(col_num_x, col_num_y, col_color, df))
                correlacao = st.sidebar.checkbox('Correlacao')
                if correlacao:
                    st.subheader('Matriz de correlação:')
                    st.markdown('Gráfico de correlação das colunas númericas')
                    st.write(cria_correlationplot(df, colunas_numericas))

def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart

def criar_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width = 600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars

def criar_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def criar_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x, y]
    ).interactive()
    return scatter

def cria_correlationplot(df, colunas_numericas):
    cor_data = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data, width=500, height=500).encode( x = 'variable2:O', y = 'variable:O')
    text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    alt.value('black')))


# The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
    color = 'correlation:Q')

    return cor_plot + text

if __name__ == '__main__':
    main()
