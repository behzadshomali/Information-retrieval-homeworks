import pandas as pd
from preprocessing import preprocess_pipeline, invert_indexing
from threading import Thread
import time
from utils import *

if __name__ == "__main__":
    parser = init_parser()
    args = parser.parse_args()

    if args.raw_data_path is not None:
        df = load_data(args.raw_data_path)
        df["preprocessed"] = ""

    if args.preprocessed_data_path is not None:
        preprocessed_df = pd.read_excel(args.preprocessed_data_path)
    else:
        since = time.time()
        threads = []
        outputs = []
        for splitted_df in chunks(df, args.threads):
            if args.verbose:
                print(f"The shape of the splitted DataFrame is {splitted_df.shape}")

            output = []
            thread = Thread(
                target=preprocess_pipeline,
                args=(
                    splitted_df,
                    output,
                    args.normalize,
                    args.remove_stop_words,
                    args.remove_punctuations,
                    args.lemmatize,
                    args.stemmer,
                    args.verbose,
                ),
            )

            thread.start()
            threads.append(thread)
            outputs.append(output)

        for thread in threads:
            thread.join()

        end = time.time()
        print(
            f"Time taken for performing preprocessing: {(end - since) / 60:.2f} minutes!"
        )

        preprocessed_df = pd.concat(output_df[0] for output_df in outputs)
        preprocessed_df.to_excel("preprocessed_data.xlsx")

    if args.indexed_data_path is not None:
        inverted_index = pd.read_excel(args.indexed_data_path)
    else:
        since = time.time()
        inverted_index = invert_indexing(preprocessed_df, args.verbose)
        end = time.time()
        print(f"Time taken for performing invert indexing: {(end - since):.3f} seconds")

        inverted_indexing_df = pd.DataFrame(
            inverted_index.items(), columns=["term", "docs_id"]
        )
        inverted_indexing_df.to_excel("inverted_indexing.xlsx")

    get_query(preprocessed_df, inverted_index, args)
