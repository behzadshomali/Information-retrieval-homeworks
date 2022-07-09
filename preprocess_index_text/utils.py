from argparse import ArgumentParser
import pandas as pd
from math import ceil
from pprint import pprint
from preprocessing import preprocess_pipeline


def init_parser():
    parser = ArgumentParser(description="Text preprocessing & indexing")

    parser.add_argument(
        "--raw-data-path",
        type=str,
        default=None,
        help="specify the address of the raw data file",
    )

    parser.add_argument(
        "--preprocessed-data-path",
        type=str,
        default=None,
        help="specify the address of the preprocessed data file",
    )

    parser.add_argument(
        "--indexed-data-path",
        type=str,
        default=None,
        help="specify the address of the indexed data file",
    )

    parser.add_argument(
        "--threads", default=4, type=int, help="specify the number of threads to use",
    )

    parser.add_argument(
        "--normalize",
        default=True,
        type=bool,
        help="specify whether to normalize the text",
    )

    parser.add_argument(
        "--remove-stop-words",
        default=True,
        type=bool,
        help="specify whether to remove stop words",
    )

    parser.add_argument(
        "--remove-punctuations",
        default=True,
        type=bool,
        help="specify whether to remove punctuations",
    )

    parser.add_argument(
        "--lemmatize",
        default=True,
        type=bool,
        help="specify whether to lemmatize the text",
    )

    parser.add_argument(
        "--stemmer", default=True, type=bool, help="specify whether to stem the text",
    )

    parser.add_argument(
        "--verbose",
        default=False,
        type=bool,
        help="specify whether to print the workflow progress",
    )
    return parser


def load_data(path):
    df = pd.read_excel(path)

    selected_cols = ["title", "content"]
    df_selected = df[selected_cols]
    df_selected = df_selected.dropna(axis=0, subset=["content"])
    df_selected["index"] = df_selected.index

    return df_selected


def chunks(df, n):
    """
    Split a DataFrame into n chunks
    so multiple threads can work on the
    DataFrame simultaneously
    """
    step_size = int(ceil(df.shape[0] / n))
    for i in range(0, df.shape[0], step_size):
        yield df.iloc[i : i + step_size]


def retrieve_documents(preprocessed_df, inverted_index, query):
    docs_titles = []
    docs_index = inverted_index.get(query, [])
    for doc_index in docs_index:
        docs_titles.append(preprocessed_df.loc[doc_index, "title"])

    return docs_titles


def get_query(preprocessed_df, inverted_index, args):
    query = input("Enter your query: ").strip()
    while query != "":
        # the end condition is when the
        # user enters an empty string
        output = []
        query_df = pd.DataFrame({"content": [query], "preprocessed": [""],})
        preprocess_pipeline(
            query_df,
            output,
            args.normalize,
            args.remove_stop_words,
            args.remove_punctuations,
            args.lemmatize,
            args.stemmer,
            args.verbose,
        )
        processed_query = output[0]["preprocessed"][0]
        print(f"Processed query: {processed_query}")

        docs_titles = retrieve_documents(preprocessed_df, inverted_index, query)
        pprint(docs_titles)
        print(f"Retrieved {len(docs_titles)} documents")

        query = input("\nEnter your query: ").strip()

