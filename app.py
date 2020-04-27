import streamlit as st
import pandas as pd


def main():
    st.sidebar.title('AceleraDev - Data Science')
    st.sidebar.image('./image/logo.png', use_column_width=True)
    file = st.sidebar.file_uploader('Upload your file', type='csv')
    show_df(file)
    if file is not None:
        genre = st.sidebar.radio(
            "Escolha como analisar seu Data Frame",
            ('Describe', 'Drama', 'Terror')
        )
        if genre == 'Describe':
            wip()
        elif genre == 'Drama':
            wip()
        elif genre == 'Terror':
            wip()


def show_df(file):
    if file is not None:
        slider = st.slider('Valores', 1, 100)
        df = pd.read_csv(file)
        st.markdown('Data Frame')
        st.dataframe(df.head(slider))

def wip():
    st.title('Work in progress')
    st.image('./image/olhos.gif', use_column_width=True)

def run_describe(file):
    st.title('Será aplicado o método Describe')
    st.sidebar.title('Describe:')
    df = pd.read_csv(file)
    describe_columns = st.selectbox(
        'Escolha a coluna a ser analisada: ', (list(df.columns)
                                               ))


if __name__ == '__main__':
    main()
