import pandas as pd
from utils import *


if __name__ == '__main__':
    inverted_indexing_df_path = '../data/inverted_indexing.xlsx'
    inverted_indexing_df = pd.read_excel(inverted_indexing_df_path)

    preprocessed_df_path = '../data/preprocessed_data.xlsx'
    preprocessed_df = pd.read_excel(preprocessed_df_path)
    docs_count = preprocessed_df.shape[0]
    print('Total number of docs:', docs_count)

    # idf = get_idf(inverted_indexing_df, docs_count, show_logs=True)
    tf = get_tf(inverted_indexing_df, preprocessed_df, show_logs=True)