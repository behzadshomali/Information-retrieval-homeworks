import pandas as pd
import numpy as np
from utils import *
from scipy import spatial


if __name__ == '__main__':

    query = getPreProccessedInput("تاریخ تحولات سیاسی اجتماعی ایران")

    inverted_indexing_df_path = '../data/inverted_indexing.xlsx'
    inverted_indexing_df = pd.read_excel(inverted_indexing_df_path)

    preprocessed_df_path = '../data/preprocessed_data.xlsx'
    preprocessed_df = pd.read_excel(preprocessed_df_path)
    docs_count = preprocessed_df.shape[0]
    print('Total number of docs:', docs_count)

    idf_query = get_idf_query(query, inverted_indexing_df, docs_count, show_logs=True)
    tf_query, tf_sum = get_tf_query(query ,inverted_indexing_df, preprocessed_df, show_logs=True)


    # --- TF*IDF ---------
    # IN HERE
    # for QUERY and DOCs
    sum = 0
    vector_query = []

    for i in " ".join(query).split(" "):
        temp = idf_query[f"{i}"] * tf_sum[f"{i}"]
        sum = sum + temp
        vector_query.append(temp)

    idf = get_idf(inverted_indexing_df, docs_count, show_logs=True)
    tf = get_tf(inverted_indexing_df, preprocessed_df, show_logs=True)

    vector_doc_tf_idf = {}
    for d_id in tf:
        vector_doc_tf_idf.setdefault(d_id, {})
        for word in tf[d_id]:
            vector_doc_tf_idf[d_id][word] = (tf[d_id][word] * idf[word])

    print(ranking(vector_query, vector_doc_tf_idf, 10))

