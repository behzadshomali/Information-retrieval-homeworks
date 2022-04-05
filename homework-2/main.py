import pandas as pd
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
    # print(inverted_indexing_df['term'])

    # idf_query = get_idf_query(query, inverted_indexing_df, docs_count, show_logs=True)
    # print(idf_query)
    # tf_query, tf_sum = get_tf_query(query ,inverted_indexing_df, preprocessed_df, show_logs=True)
    # print(tf_sum)

    # sum = 0
    # # vector_query = {}
    # vector_query = []
    # for i in " ".join(query).split(" "):
    #     temp = idf_query[f"{i}"] * tf_sum[f"{i}"]
    #     sum = sum + temp
    #     # vector_query[i] = temp
    #     vector_query.append(temp)
    # print(vector_query)

    # query_idf = get_idf_query(query, inverted_indexing_df, docs_count, show_logs=True)
    # query_tf, tf_sum = get_tf_query(query ,inverted_indexing_df, preprocessed_df, show_logs=True)

    # docs_idf = get_idf(inverted_indexing_df, docs_count, show_logs=True)
    # docs_tf = get_tf(inverted_indexing_df, preprocessed_df, show_logs=True)

    docs_vector = compute_docs_tf_idf(docs_count, preprocessed_df, inverted_indexing_df, show_logs=True)
    query_vector = compute_query_tf_idf(query, preprocessed_df, inverted_indexing_df)
    print(ranking(query_vector, docs_vector, 10))
