import pandas as pd
from preprocessing import preprocess_pipeline, invert_indexing
from threading import Thread
import time
from math import ceil
from pprint import pprint

def load_data(path):
    df = pd.read_excel(path)

    selected_cols = ['title', 'content']
    df_selected = df[selected_cols]
    df_selected['index'] = df_selected.index

    return df_selected

def remove_null(data):

    df = data.dropna(axis=0, subset=['content'])
    df.to_excel('final_books_without_null.xlsx')

    return df

def chunks(df, n):
    step_size = int(ceil(df.shape[0] / n))
    for i in range(0, df.shape[0], step_size):
        yield df.iloc[i:i + step_size]

def retrieve_documents(preprocessed_df, inverted_index, query):
    docs_titles = []
    docs_index =  inverted_index.get(query, [])
    for doc_index in docs_index:
        docs_titles.append(preprocessed_df.loc[doc_index, 'title'])

    return docs_titles

def get_query(preprocessed_df, method, inverted_index):
    query = input('Enter your query: ').strip()
    while query != '':
        output = []
        query_df = pd.DataFrame(
            {
                'content': [query],
                'stop_word': [''],
                'lemmatizer': [''],
                'stemmer': [''],
            }
        )

        preprocess_pipeline(query_df, output, True, True, True, True, True)
        processed_query = output[0][method][0]
        print(f'Processed query: {processed_query}')

        docs_titles = retrieve_documents(preprocessed_df, inverted_index, query)
        pprint(docs_titles)
        print(f'Retrieved {len(docs_titles)} documents')

        query = input('\nEnter your query: ').strip()


# df = load_data('final_books_without_null.xlsx')
# df['stop_word'] = ''
# df['lemmatizer'] = ''
# df['stemmer'] = ''

# since = time.time()

n = 5 # number of threads
# threads = []
# outputs = []
# for splitted_df in chunks(df, n):
#     print(splitted_df.shape)
#     output = []
#     thread = Thread(target=preprocess_pipeline, args=(splitted_df, output, True, True, True, True, True))
#     thread.start()
#     threads.append(thread)
#     outputs.append(output)

# for thread in threads:
#     thread.join()

# end = time.time()
# print(f'Time taken for performing preprocessing: {(end - since) / 60:.2f} minutes')

# preprocessed_df = pd.concat(output_df[0] for output_df in outputs)
# preprocessed_df.to_excel("preprocessed_data.xlsx")

preprocessed_df = pd.read_excel('preprocessed_data.xlsx')
since = time.time()

method = 'lemmatizer'
inverted_index = invert_indexing(preprocessed_df, method)

end = time.time()
print(f'Time taken for performing invert indexing: {(end - since):.3f} seconds')

inverted_indexing_df = pd.DataFrame(inverted_index.items(), columns=['term', 'docs_id'])
inverted_indexing_df.to_excel("inverted_indexing.xlsx")



get_query(preprocessed_df, method, inverted_index)