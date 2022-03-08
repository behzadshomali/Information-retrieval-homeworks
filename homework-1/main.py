import pandas as pd
from preprocessing import preprocess_pipeline

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


df = load_data('final_books_without_null.xlsx')
df['stop_word'] = ''
df['lemmatizer'] = ''

preprocess_pipeline(
    df,
    normalize_flag=True,
    remove_stop_words_flag=True,
    remove_punctuations_flag=True,
    lemmatize_flag=True,
)