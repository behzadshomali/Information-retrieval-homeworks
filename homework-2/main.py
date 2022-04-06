import pandas as pd
import numpy as np
from utils import *
from scipy import spatial
from threading import Thread


if __name__ == '__main__':

    
    inverted_indexing_df_path = '../data/inverted_indexing.xlsx'
    inverted_indexing_df = pd.read_excel(inverted_indexing_df_path)

    preprocessed_df_path = '../data/preprocessed_data.xlsx'
    preprocessed_df = pd.read_excel(preprocessed_df_path)
    docs_count = preprocessed_df.shape[0]
    print('Total number of docs:', docs_count)

     # --- TF*IDF ---------
    # IN HERE
    # for DOCS
    idf = []
    tf = []
    idf_thread = Thread(target=get_idf, args=(idf, inverted_indexing_df, docs_count, True))
    tf_thread = Thread(target=get_tf, args=(tf, inverted_indexing_df, preprocessed_df, True))
    idf_thread.start()
    tf_thread.start()
    idf_thread.join()
    tf_thread.join()
    # idf = get_idf(inverted_indexing_df, docs_count, show_logs=True)
    # tf = get_tf(inverted_indexing_df, preprocessed_df, show_logs=True)

    idf = idf[0]
    tf = tf[0]

    vector_doc_tf_idf = np.zeros((docs_count, len(inverted_indexing_df.term)))
    for d, d_id in enumerate(preprocessed_df.index):
        for w, word in enumerate(inverted_indexing_df.term):
            vector_doc_tf_idf[d, w] = (tf.get(d_id, {}).get(word, 0) * idf.get(word, 0))
            

    # --- TF*IDF ---------
    # IN HERE
    # for QUERY
    query = getPreProccessedInput(input('Enter your query: '))
    while True:
        # idf_query = get_idf_query(query, inverted_indexing_df, docs_count, show_logs=True)
        tf_query, tf_sum = get_tf_query(query ,inverted_indexing_df, preprocessed_df, show_logs=True)
        
        vector_query = np.zeros(len(inverted_indexing_df.term))
        # for d, d_id in enumerate(preprocessed_df.index):
        for w, word in enumerate(inverted_indexing_df.term):
            if word in query:
                vector_query[w] = (tf_sum.get(word, 0) * idf.get(word, 0))
                print(word, ':', tf_sum.get(word, 0), idf.get(word, 0))

        matches_indices, matches_scores =  ranking(vector_query, vector_doc_tf_idf, 10)
        print('10 most relevant docs for the input query are as follows:', )
        for i, match_index in enumerate(matches_indices[::-1]):
            print(f"Doc_ID: {match_index}, score: {matches_scores[i]}/ {preprocessed_df.iloc[match_index]['title']}")
        
        query = getPreProccessedInput(input('Enter another query: '))