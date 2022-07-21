import ast
import math
import numpy as np
from scipy import spatial
from argparse import ArgumentParser
from threading import Thread
import json
import os


def init_parser():
    parser = ArgumentParser(description="Cosine distance & Query expansion")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="whether to print verbose output",
    )

    parser.add_argument(
        "-k", default=10, type=int, help="number of top matches to be returned",
    )

    parser.add_argument(
        "-i",
        "--inverted-indexing-dataframe-path",
        type=str,
        help="path to the inverted indexing dataframe",
    )

    parser.add_argument(
        "-p",
        "--preprocessed-dataframe-path",
        type=str,
        help="path to the preprocessed dataframe",
    )

    parser.add_argument(
        "--normalize",
        help="specify whether to normalize the text",
        action="store_true",
    )

    parser.add_argument(
        "--remove-stop-words",
        help="specify whether to remove stop words",
        action="store_true",
    )

    parser.add_argument(
        "--remove-punctuations",
        help="specify whether to remove punctuations",
        action="store_true",
    )

    parser.add_argument(
        "--lemmatize",
        help="specify whether to lemmatize the text",
        action="store_true",
    )

    parser.add_argument(
        "--stemmer", help="specify whether to stem the text", action="store_true",
    )

    return parser


def get_idf_query(query, inverted_indexing_df, docs_count, show_logs=False):
    """term --> idf"""
    idf = {}
    for term in query:
        try:
            term_docs_ids = inverted_indexing_df.loc[
                inverted_indexing_df.term == term, "docs_id"
            ].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            doc_frequency = len(term_docs_ids)
            idf[term] = math.log((docs_count / doc_frequency), 10)
        except Exception as e:
            print(e)

    return idf


def get_tf_query(query, inverted_indexing_df, preprocessed_df, show_logs=False):
    """term --> doc --> tf"""
    tf = {}
    tf_sum = {}
    for term in query:
        sum = 0
        tf.setdefault(term, {})
        try:
            term_docs_ids = inverted_indexing_df.loc[
                inverted_indexing_df.term == term, "docs_id"
            ].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            for doc_id in term_docs_ids:

                doc_preprocessed_content = preprocessed_df.loc[
                    preprocessed_df.index == doc_id, "lemmatizer"
                ].to_list()[0]
                doc_preprocessed_terms = doc_preprocessed_content.split("/")
                cal = 1 + math.log((doc_preprocessed_terms.count(term)), 10)
                tf[term][doc_id] = cal
                sum = sum + cal
                tf_sum[term] = sum
        except Exception as e:
            print(e)

    return tf, tf_sum


def get_tf_idf_query(
    query, inverted_indexing_df, preprocessed_df, idf, show_logs=False
):
    tf_query, tf_sum = get_tf_query(
        query, inverted_indexing_df, preprocessed_df, show_logs=show_logs
    )

    vector_query_tf_idf = np.zeros(len(inverted_indexing_df.term))
    for w, word in enumerate(inverted_indexing_df.term):
        if word in query:
            vector_query_tf_idf[w] = tf_sum.get(word, 0) * idf.get(word, 0)

    return vector_query_tf_idf


def get_idf(idf, inverted_indexing_df, docs_count, show_logs=False):
    """term --> idf"""
    idf.append({})
    for i, term in enumerate(inverted_indexing_df.term):
        try:
            term_docs_ids = inverted_indexing_df.loc[
                inverted_indexing_df.term == term, "docs_id"
            ].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            doc_frequency = len(term_docs_ids)
            idf[0][term] = math.log((docs_count / doc_frequency), 10)
        except Exception as e:
            print(e)

        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print(
                    "Computed idf for {}/{} terms!".format(i, len(inverted_indexing_df))
                )

    return idf


def get_tf(tf, inverted_indexing_df, preprocessed_df, show_logs=False):
    """doc --> term --> tf"""
    tf.append({})
    for i, term in enumerate(inverted_indexing_df.term):
        try:
            term_docs_ids = inverted_indexing_df.loc[
                inverted_indexing_df.term == term, "docs_id"
            ].to_list()[0]
            term_docs_ids = ast.literal_eval(term_docs_ids)
            for doc_id in term_docs_ids:
                tf[0].setdefault(doc_id, {})
                doc_preprocessed_content = preprocessed_df.loc[
                    preprocessed_df.index == doc_id, "lemmatizer"
                ].to_list()[0]
                doc_preprocessed_terms = doc_preprocessed_content.split("/")

                tf[0][doc_id][term] = 1 + math.log(
                    (doc_preprocessed_terms.count(term)), 10
                )
        except Exception as e:
            print(e)

        if show_logs:
            if i % int(inverted_indexing_df.shape[0] / 20) == 0:
                print(
                    "Computed tf for {}/{} terms!".format(i, len(inverted_indexing_df))
                )

    return tf


def get_tf_idf(inverted_indexing_df, preprocessed_df, docs_count, show_logs=False):
    # used a list to store the idf values in order to
    # be able to work with multiple threads
    idf = []
    tf = []
    idf_thread = Thread(
        target=get_idf, args=(idf, inverted_indexing_df, docs_count, show_logs)
    )
    tf_thread = Thread(
        target=get_tf, args=(tf, inverted_indexing_df, preprocessed_df, show_logs)
    )

    idf_thread.start()
    if show_logs:
        print("Computing idf...")

    tf_thread.start()
    if show_logs:
        print("Computing tf...")

    idf_thread.join()
    tf_thread.join()

    idf = idf[0]
    tf = tf[0]
    vector_doc_tf_idf = np.zeros((docs_count, len(inverted_indexing_df.term)))

    if show_logs:
        print("Computing tf-idf...")

    for d, d_id in enumerate(preprocessed_df.index):
        for w, word in enumerate(inverted_indexing_df.term):
            vector_doc_tf_idf[d, w] = tf.get(d_id, {}).get(word, 0) * idf.get(word, 0)

    return vector_doc_tf_idf, idf


def ranking(vector_query, vector_doc_tf_idf, k):
    cosine_distances = []

    for i in range(vector_doc_tf_idf.shape[0]):
        try:
            z = spatial.distance.cosine(vector_doc_tf_idf[i], vector_query)
            cosine_distances.append(z.item())
        except Exception as e:
            print(e)

    cosine_distances = np.array(cosine_distances)

    top_matches_indices = np.argsort(cosine_distances, axis=0)[:k]
    return top_matches_indices, cosine_distances[top_matches_indices]


def store_output_to_json(
    q_input, matches_indices, matches_distances, preprocessed_df, show_logs=False
):
    data = {}
    for i, match_index in enumerate(matches_indices):
        data[f"num{i}"] = {}
        data[f"num{i}"]["Query"] = str(q_input)
        data[f"num{i}"]["Doc_ID"] = str(match_index)
        data[f"num{i}"]["distance"] = str(matches_distances[i])
        data[f"num{i}"]["title"] = str(preprocessed_df.iloc[match_index]["title"])

    if not os.path.exists("./output"):
        os.makedirs("./output")

    with open(f"output/Query-{q_input}.json", "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False)

    if show_logs:
        print(f"Output stored to output/Query-{q_input}.json")
