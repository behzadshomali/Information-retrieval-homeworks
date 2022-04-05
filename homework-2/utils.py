import ast
import math
import preprocessing
import hazm as hzm
import numpy as np

def getPreProccessedInput(query):
    text = preprocessing.normalizer(query)
    text_tokens = hzm.word_tokenize(text)
    text_tokens = preprocessing.remove_punctuations(text_tokens)
    text_tokens = preprocessing.removeStopWords(text_tokens)
    text_tokens = preprocessing.lemma(text_tokens)

    return text_tokens

def get_idf_query(query,inverted_indexing_df, docs_count, show_logs=False):
    '''term --> df(doc frequency) --> idf'''
    idf = {}
    for term in query:
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            doc_frequency = len(term_docs_ids)
            idf[term] = math.log((docs_count / doc_frequency), 10)
        except Exception as e:
            print(e)

        # if show_logs:
        #     if i % int(inverted_indexing_df.shape[0]/20) == 0:
        #         print('Computed idf for {}/{} terms!'.format(i, len(inverted_indexing_df)))

    return idf

def get_tf_query(query, inverted_indexing_df, preprocessed_df, show_logs=False):
    '''term --> doc --> tf'''
    tf = {}
    tf_sum = {}
    for term in query:
        sum = 0
        tf.setdefault(term, {})
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            for doc_id in term_docs_ids:

                doc_preprocessed_content = preprocessed_df.loc[preprocessed_df.index == doc_id, 'lemmatizer'].to_list()[0]
                doc_preprocessed_terms = doc_preprocessed_content.split('/')
                cal = 1 + math.log((doc_preprocessed_terms.count(term)), 10)
                tf[term][doc_id] = cal
                sum = sum + cal
                tf_sum[term] = sum
        except Exception as e:
            print(e)

        # if show_logs:
        #     if i % int(inverted_indexing_df.shape[0]/20) == 0:
        #         print('Computed tf for {}/{} terms!'.format(i, len(inverted_indexing_df)))

    return tf, tf_sum

def get_idf(inverted_indexing_df, docs_count, show_logs=False):
    '''term --> df(doc frequency) --> idf'''
    idf = {}
    for i, term in enumerate(inverted_indexing_df.term):
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            doc_frequency = len(term_docs_ids)
            idf[term] = math.log((docs_count / doc_frequency), 10)
        except Exception as e:
            print(e)

        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print('Computed idf for {}/{} terms!'.format(i, len(inverted_indexing_df)))

    return idf

def get_tf(inverted_indexing_df, preprocessed_df, show_logs=False):
    '''term --> doc --> tf'''
    tf = {}
    for i, term in enumerate(inverted_indexing_df.term):
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            for doc_id in term_docs_ids:
                tf.setdefault(doc_id, {})
                doc_preprocessed_content = preprocessed_df.loc[preprocessed_df.index == doc_id, 'lemmatizer'].to_list()[0]
                doc_preprocessed_terms = doc_preprocessed_content.split('/')

                tf[doc_id][term] = 1 + math.log((doc_preprocessed_terms.count(term)), 10)
        except Exception as e:
            print(e)


        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print('Computed tf for {}/{} terms!'.format(i, len(inverted_indexing_df)))


    return tf

def compute_docs_tf_idf(docs_count, preprocessed_df, inverted_indexing_df, show_logs=False):
    terms_list = inverted_indexing_df['term'].to_list()

    docs_vector = np.zeros((docs_count, len(terms_list)))
    docs_tf = get_tf(inverted_indexing_df, preprocessed_df, show_logs=True)
    docs_idf = get_idf(inverted_indexing_df, docs_count,show_logs=True)

    for i, term in enumerate(terms_list):
        if show_logs:
            if i % int(len(terms_list) / 20) == 0:
                print('Computed tf-idf for {}/{} terms!'.format(i, len(terms_list)))
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            for j, doc_id in enumerate(term_docs_ids):
                if term in docs_tf[doc_id].keys():
                    if term in docs_idf.keys():
                        docs_vector[j][i] = docs_tf[doc_id][term] * docs_idf[term]
        except Exception as e:
            print(e)
    return docs_vector

def compute_query_tf_idf(query, preprocessed_df, inverted_indexing_df):
    terms_list = inverted_indexing_df['term'].to_list()

    query_vector = np.zeros((1, len(terms_list)))
    query_tf, _ = get_tf_query(query, inverted_indexing_df, preprocessed_df)
    query_idf = get_idf_query(query, inverted_indexing_df, len(preprocessed_df))

    for i, term in enumerate(terms_list):
        if term in query_idf.keys():
            if term in query_tf.keys():
                term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
                term_docs_ids = ast.literal_eval(term_docs_ids)
                for doc_id in term_docs_ids:
                    if doc_id in query_tf[term].keys():
                        query_vector[0][i] = query_tf[term][doc_id] * query_idf[term]

    return query_vector

def ranking(query_vector, docs_vector, k):
    cosine_similarity = np.dot(query_vector, docs_vector.T) / (np.linalg.norm(query_vector) * np.linalg.norm(docs_vector))
    # top_matches_indices = np.argsort(cosine_similarity, axis=0)[::-1][:k]
    return top_matches_indices