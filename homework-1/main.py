import pandas as pd


def load_data(path):
    df = pd.read_excel(path)

    selected_cols = ['title', 'content']
    df_selected = df[selected_cols]
    df_selected['index'] = df_selected.index

    return df_selected

df = load_data('final_books.xlsx')