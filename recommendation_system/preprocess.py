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

def genres(data):
    """
    convert numbet to a true genre
    :param data: movies
    :return: movies dataset with a extra column that has the generes in string
    """
    genres = []

    for genre in data:
        if genre == 0:
            genres.append("Action")
        elif genre == 1:
            genres.append("Adventure")
        elif genre == 2:
            genres.append("Animation")
        elif genre == 3:
            genres.append("Children")
        elif genre == 4:
            genres.append("Comedy")
        elif genre == 5:
            genres.append("Crime")
        elif genre == 6:
            genres.append("Documentary")
        elif genre == 7:
            genres.append("Drama")
        elif genre == 8:
            genres.append("Fantasy")
        elif genre == 9:
            genres.append("Film-Noir")
        elif genre == 10:
            genres.append("Horror")
        elif genre == 11:
            genres.append("Musical")
        elif genre == 12:
            genres.append("Mystery")
        elif genre == 13:
            genres.append("Romance")
        elif genre == 14:
            genres.append("Sci-Fi")
        elif genre == 15:
            genres.append("Thriller")
        elif genre == 16:
            genres.append("War")
        elif genre == 17:
            genres.append("Western")

    return np.asarray(genres)



