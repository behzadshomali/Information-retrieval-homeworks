import pandas as pd
import numpy as np
from utils import *
from preprocessing import preprocess_pipeline


if __name__ == "__main__":
    parser = init_parser()
    args = parser.parse_args()

    inverted_indexing_df_path = args.inverted_indexing_dataframe_path
    inverted_indexing_df = pd.read_excel(inverted_indexing_df_path)
    preprocessed_df_path = args.preprocessed_dataframe_path
    preprocessed_df = pd.read_excel(preprocessed_df_path)

    docs_count = preprocessed_df.shape[0]

    if args.verbose:
        print("Total number of docs:", docs_count)

    vector_doc_tf_idf, idf = get_tf_idf(
        inverted_indexing_df, preprocessed_df, docs_count, args.verbose
    )

    q_input = input("Enter your query: ")
    while q_input != "":
        query = preprocess_pipeline(q_input)
        vector_query_tf_idf = get_tf_idf_query(
            query, inverted_indexing_df, preprocessed_df, idf, args.verbose
        )

        matches_indices, matches_distances = ranking(
            vector_query_tf_idf, vector_doc_tf_idf, args.k
        )

        print(f"{args.k} most relevant docs for the input query are as follows:",)
        for i, match_index in enumerate(matches_indices):
            print(
                f"Doc_ID: {match_index:5d}, distance: {matches_distances[i]:.5f}/ {preprocessed_df.iloc[match_index]['title']}"
            )

        store_output_to_json(
            q_input, matches_indices, matches_distances, preprocessed_df, args.verbose
        )

        q_input = input("Enter your query: ")

