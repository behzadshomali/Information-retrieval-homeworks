import numpy as np
import pandas as pd
from recommendation_system.preprocess import genres
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from recommendation_system.user_based import similarity_between_users, normalization_top10

def make_description_for_user(ratings):
    """
    The description is about gender, job, and all movies that user have seen them
    with the rate.
    :param ratings
    :return: a description for every user in ratings dataset
    """
    user_description = {}
    for user_id in np.unique(ratings['user_id']):
        gender = ratings[ratings['user_id'] == user_id].user_gender.to_list()[0]
        job = ratings[ratings['user_id'] == user_id].user_occupation_text.to_list()[0]
        description = f"I am a {gender}, my job is {job}. "
        for user_ratings in np.unique(ratings['user_rating']):
            movie_name = ", ".join(
                ratings[ratings['user_id'] == user_id][ratings['user_rating'] == user_ratings]['movie_title'].to_list())
            if len(movie_name) > 2:
                description += f"I gave these films a score of {user_ratings}: {movie_name}. "
            else:
                description += f"I have not given a score of {user_ratings} to any film. "

        user_description[user_id] = description

    return user_description


def rating_to_not_seen_movie(numpy_user_movie, user_query, users_similarity, user_des_, user_query_label):
    rating_movie_user_query_not_seen = {}
    for film_id_user_query_not_seen in np.where(numpy_user_movie[user_query] == -1)[0]:
        result = 0
        sum = 0
        for user_id in user_des_[user_des_['label'] == user_query_label].index:
            if user_query == user_id:
                continue
            if film_id_user_query_not_seen in np.where(numpy_user_movie[user_id] != -1)[0]:
                result += users_similarity[(user_query, user_id)] * numpy_user_movie[user_id][film_id_user_query_not_seen]
                sum += users_similarity[(user_query, user_id)]

        if result != 0 or np.abs(sum) != 0:
            result_pre = result / np.abs(sum)
            print(f"{film_id_user_query_not_seen}: {result_pre}")
            rating_movie_user_query_not_seen[film_id_user_query_not_seen] = result_pre
        else:
            print(f"{film_id_user_query_not_seen}: 0")
            rating_movie_user_query_not_seen[film_id_user_query_not_seen] = 0

    return rating_movie_user_query_not_seen

def content_based(movies, ratings, user_query):
    # get and save true genre of film by id of genre in dataset
    ratings['genres'] = ratings['movie_genres'].apply(genres)
    movies['genres'] = movies['movie_genres'].apply(genres)

    # convert boolean to string for gender
    ratings['user_gender'] = ratings['user_gender'].replace([True, False], ['Men', 'Woman'])

    # make a description for user and save it to a dataframe
    user_description = make_description_for_user(ratings)
    user_des_ = pd.DataFrame.from_dict(user_description, orient='index',
                                       columns=['user_description'])
    user_des_['user_id'] = list(user_description.keys())

    # convert every description to a vector by TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_features=100)
    tfidf_vectorizer.fit(user_des_['user_description'])
    X = tfidf_vectorizer.transform(user_des_['user_description'])

    # users that similar to each other should be in one cluster
    kmeans = KMeans(n_clusters=100, random_state=0)
    kmeans.fit(X)

    # add number of cluster for each user in dataset
    user_des_['label'] = kmeans.labels_
    user_query_label = user_des_[user_des_['user_id'] == user_query]['label']

    user_movie = ratings.pivot(index='user_id', columns='movie_id', values='user_rating')
    user_movie = user_movie.fillna(-1)
    numpy_user_movie = user_movie.to_numpy()
    users_similarity = similarity_between_users(numpy_user_movie, user_query)

    # calculate rating to movies that user_query have not seen them
    rating_movie_user_query_not_seen = rating_to_not_seen_movie(numpy_user_movie, user_query,users_similarity, user_des_, user_query_label)

    # normalized ratings and get top 10 ratings
    result = normalization_top10(rating_movie_user_query_not_seen, user_movie, movies)

    return result
