import pandas as pd


def load_data(path):
    df = pd.read_excel(path)

    selected_cols = ['title', 'content']
    df_selected = df[selected_cols]
    df_selected['index'] = df_selected.index

    return df_selected

def remove_null(data):
    
    df = data.dropna(axis=0, subset=['content'])
    df.to_excel('final_books_without_null.xlsx')

    return df

df = load_data('final_books.xlsx')

df = remove_null(df)
