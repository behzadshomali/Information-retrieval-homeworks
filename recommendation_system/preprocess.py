import pandas as pd
import numpy as np

def preprocess_data(path1, path2):
    """
    There are two datasets, names are movies and ratings.
    because our datasets are .gzip after we read data, some columns are equal b'somthing',
    first we must delete it and if it is digit must be changed to numeric.
    :param path1: String, dataset path
    :param path2: String, dataset path
    :return: two datasets
    """
    ratings = pd.read_parquet(f"{path1}")
    movies = pd.read_parquet(f"{path2}")

    # remove {b''} from dataset and change id from string to int

    # Ratings dataset
    object_cols = ['movie_id', 'movie_title', 'user_id', 'user_occupation_text', 'user_zip_code']
    for clm in object_cols:
        ratings[f"{clm}"] = ratings[f"{clm}"].apply(lambda x: x.decode('utf-8'))

    ratings['movie_id'] = pd.to_numeric(ratings['movie_id'])
    ratings['user_id'] = pd.to_numeric(ratings['user_id'])

    # Movies dataset
    object_cols = ['movie_id', 'movie_title']
    for clm in object_cols:
        movies[f"{clm}"] = movies[f"{clm}"].apply(lambda x: x.decode('utf-8'))

    movies['movie_id'] = pd.to_numeric(movies['movie_id'])

    return ratings, movies