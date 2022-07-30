import pandas as pd
import numpy as np
from numpy import linalg as LA
from threading import Thread
import json


def similarity_between_movie(movies_similarity, s1_1, s1_2, film_id2, numpy_user_movie):
    for film_id1 in range(s1_1, s1_2):
        if film_id1 == film_id2:
            continue
        if (film_id1,film_id2) in movies_similarity.keys() or (film_id2, film_id1) in movies_similarity.keys():
            continue
        movies_similarity[(film_id1,film_id2)] = float("{0:.10f}".format(np.dot(numpy_user_movie[: ,film_id1], numpy_user_movie[: ,film_id2]) /
                                                        (LA.norm(numpy_user_movie[: ,film_id1]) * LA.norm(numpy_user_movie[: ,film_id2]))))
    return movies_similarity

def save_similarity_to_json(movies_similarity):
    with open("movies_similarity.json", "w") as f:
        k = movies_similarity.keys()
        v = movies_similarity.values()
        k1 = [str(i) for i in k]
        json.dump(json.dumps(dict(zip(*[k1, v]))), f)

def load_similarity_to_json():
    with open("/content/gdrive/MyDrive/IR_project/movies_similarity.json", 'r') as f:
        data = json.load(f)
        dic = json.loads(data)
        k = dic.keys()
        v = dic.values()
        k1 = [eval(i) for i in k]
        movies_similarity = dict(zip(*[k1, v]))

    return movies_similarity


def get_user_ratings(user_query, numpy_user_movie):
    user_query_ratings = {}
    for film_id, user_ratings in enumerate(numpy_user_movie[user_query]):

        if user_ratings != '?':
            user_query_ratings[film_id] = user_ratings
    return user_query_ratings

def get_user_not_rating(user_query, numpy_user_movie):
    user_query_not_ratings = []
    for film_id, user_ratings in enumerate(numpy_user_movie[user_query]):

        if user_ratings == '?':
            user_query_not_ratings.append(film_id)
    return user_query_not_ratings


def item_based(ratings):
    user_movie = ratings.pivot(index='user_id', columns='movie_id', values='user_rating')
    user_movie = user_movie.fillna(0)
    numpy_user_movie = user_movie.to_numpy().copy()

    movies_similarity = {}
    threads = []
    # use parallelism because your data is huge
    for film_id2 in range(0, len(user_movie.columns)):
        for i in range(0, 3706, 218):
            t = Thread(target=similarity_between_movie, args=(movies_similarity, numpy_user_movie, i, i + 218, film_id2))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        if film_id2 % 200 == 0:
            print(f"film_id: {film_id2} is done.")

    # save data
    # save_similarity_to_json(movies_similarity)

    # load data
    # movies_similarity = load_similarity_to_json()

    return movies_similarity

def item_based_recommend(user_query, result, user_query_not_ratings, movies_similarity, numpy_user_movie):
    user_query_ratings = get_user_ratings(user_query, numpy_user_movie)

    for not_rating in user_query_not_ratings:
        sum_similarity = 0
        multiply_rate_sim = 0

        for key in movies_similarity.keys():
            if key[0] == not_rating:
                if key[1] in user_query_ratings.keys():
                    sum_similarity += movies_similarity[key]
                    multiply_rate_sim += user_query_ratings[key[1]] * movies_similarity[key]
            elif key[1] == not_rating:
                if key[0] in user_query_ratings.keys():
                    sum_similarity += movies_similarity[key]
                    multiply_rate_sim += user_query_ratings[key[0]] * movies_similarity[key]
        if sum_similarity != 0:
            result[not_rating] = multiply_rate_sim / sum_similarity
        else:
            result[not_rating] = 0
        if len(result) % 50 == 0:
            print(f"len(result) : {len(result)}")
    print(f"done.")
    return result


def top10(data, user_movie, movies):
    result = {}
    temp = sorted(data, key=data.get, reverse=True)

    for i, value in enumerate(temp):

        movie_id = user_movie[user_movie.columns[value]].name
        name_movie = movies[movies['movie_id'] == int(movie_id)]['movie_title'].to_list()[0]
        result[name_movie] = data[value]
        if i == 10:
            break

    return result

