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

    idf_query = get_idf_query(query, inverted_indexing_df, docs_count, show_logs=True)
    print(idf_query)
    tf_query, tf_sum = get_tf_query(query ,inverted_indexing_df, preprocessed_df, show_logs=True)
    print(tf_sum)

    sum = 0
    # vector_query = {}
    vector_query = []
    for i in " ".join(query).split(" "):
        temp = idf_query[f"{i}"] * tf_sum[f"{i}"]
        sum = sum + temp
        # vector_query[i] = temp
        vector_query.append(temp)
    print(vector_query)

    idf = get_idf(inverted_indexing_df, docs_count, show_logs=True)
    tf = get_tf(inverted_indexing_df, preprocessed_df, show_logs=True)

    # doc_tf_idf = {}
    # for d_id in tf:
    #     temp = 0
    #     for word in tf[d_id]:
    #         temp = temp + (tf[d_id][word] * idf[word])
    #     doc_tf_idf[d_id] = temp

    vector_doc_tf_idf = {}
    for d_id in tf:
        vector_doc_tf_idf.setdefault(d_id, {})
        for word in tf[d_id]:
            vector_doc_tf_idf[d_id][word] = (tf[d_id][word] * idf[word])


    # شباهت کوسینوسی- طول بردار پرس و جو و سند یکی نبود!!!
    for i in vector_doc_tf_idf:
        temp = []
        for vec_doc in vector_doc_tf_idf[i]:
            temp.append(vector_doc_tf_idf[i][vec_doc])
        print(temp)
        print(vector_query)
        cos_dis = spatial.distance.cosine(vector_query, temp)
        print(cos_dis)
