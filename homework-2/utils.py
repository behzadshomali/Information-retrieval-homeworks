import ast
import math
import preprocessing
import hazm as hzm
import numpy as np
from scipy import spatial

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
                doc_preprocessed_content = preprocessed_df.loc[preprocessed_df.index == doc_id, 'lemmatizer'].to_list()[
                    0]
                doc_preprocessed_terms = doc_preprocessed_content.split('/')

                tf[doc_id][term] = 1 + math.log((doc_preprocessed_terms.count(term)), 10)
        except Exception as e:
            print(e)


        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print('Computed tf for {}/{} terms!'.format(i, len(inverted_indexing_df)))


    return tf



def ranking(vector_query, vector_doc_tf_idf, k):
    cosine_similarities = []

    for i in vector_doc_tf_idf:
        count = 0
        query_vec2 = vector_query.copy()
        temp = []
        for vec_doc in vector_doc_tf_idf[i]:
            temp.append(vector_doc_tf_idf[i][vec_doc])
            count = count + 1
            if count > len(vector_query): query_vec2.append(0)
        # cosine_similarities.append(np.dot(query_np, docs_np) / (np.linalg.norm(query_np) * np.linalg.norm(docs_np)))
        z = spatial.distance.cosine(query_vec2, temp)
        cosine_similarities.append(z)

        temp.clear()

    cosine_np = 1-np.array(cosine_similarities)
    top_matches_indices = np.argsort(cosine_np, axis=0)[::-1][:k]
    return top_matches_indices, cosine_np[top_matches_indices]