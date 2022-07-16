import json
import time
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch


class ElasticSearchManagement:
    def __init__(self):
        self.es_client = Elasticsearch(hosts="http://localhost:9200/")

    def populate_index(self, path: str, index_name: str):
        """
        Populate an index from a CSV file.
        :param path: The path to the CSV file.
        :param index_name: Name of the index to which documents should be written.
        """

        df = pd.read_csv(path).replace({np.nan: None})
        df = df.iloc[155:]
        for doc in df.apply(lambda x: x.to_dict(), axis=1):
            try:
                print(doc)
                self.es_client.index(index=index_name, body=json.dumps(doc))
            except:
                print("connection timed out. wait. 10 sec")
                time.sleep(10)
                print(doc)
                self.es_client.index(index=index_name, body=json.dumps(doc))


print("start...")
es_connection = ElasticSearchManagement()
es_connection.populate_index(index_name="audiobooks",
                             path="data/total_audio_books.csv")
