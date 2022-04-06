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


def get_idf(idf, inverted_indexing_df, docs_count, show_logs=False):
    '''term --> df(doc frequency) --> idf'''
    idf.append({})
    for i, term in enumerate(inverted_indexing_df.term):
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            doc_frequency = len(term_docs_ids)
            idf[0][term] = math.log((docs_count / doc_frequency), 10)
        except Exception as e:
            print(e)

        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print('Computed idf for {}/{} terms!'.format(i, len(inverted_indexing_df)))

    return idf


def get_tf(tf, inverted_indexing_df, preprocessed_df, show_logs=False):
    '''doc --> term --> tf'''
    tf.append({})
    for i, term in enumerate(inverted_indexing_df.term):
        try:
            term_docs_ids = inverted_indexing_df.loc[inverted_indexing_df.term == term, 'docs_id'].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            for doc_id in term_docs_ids:
                tf[0].setdefault(doc_id, {})
                doc_preprocessed_content = preprocessed_df.loc[preprocessed_df.index == doc_id, 'lemmatizer'].to_list()[0]
                doc_preprocessed_terms = doc_preprocessed_content.split('/')

                tf[0][doc_id][term] = 1 + math.log((doc_preprocessed_terms.count(term)), 10)
        except Exception as e:
            print(e)


        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print('Computed tf for {}/{} terms!'.format(i, len(inverted_indexing_df)))


    return tf



def ranking(vector_query, vector_doc_tf_idf, k):
    cosine_distances = []

    for i in range(vector_doc_tf_idf.shape[0]):
        z = spatial.distance.cosine(vector_doc_tf_idf[i], vector_query)
        cosine_distances.append(z.item())

    cosine_distances = np.array(cosine_distances)
    top_matches_indices = np.argsort(cosine_distances, axis=0)[:k]
    return top_matches_indices, cosine_distances[top_matches_indices]