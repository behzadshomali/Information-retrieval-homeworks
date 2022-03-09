import pandas as pd
from preprocessing import preprocess_pipeline, invert_indexing
from threading import Thread
import time
from math import ceil

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

# merged_output_df = pd.concat(output_df[0] for output_df in outputs)
# merged_output_df.to_excel("preprocessed_data.xlsx")

merged_output_df = pd.read_excel('preprocessed_data.xlsx')
since = time.time()

threads = []
outputs = []
for splitted_df in chunks(merged_output_df, n):
    print(splitted_df.shape)
    output = {}
    thread = Thread(target=invert_indexing, args=(splitted_df, 'stemmer', output))
    thread.start()
    threads.append(thread)
    outputs.append(output)

for thread in threads:
    thread.join()

end = time.time()
print(f'Time taken for performing invert indexing: {(end - since) / 60:.2f} minutes')

merged_inverted_indexing_df = pd.concat(pd.DataFrame(output_df.items()) for output_df in outputs)
merged_inverted_indexing_df.to_excel("inverted_indexing.xlsx")