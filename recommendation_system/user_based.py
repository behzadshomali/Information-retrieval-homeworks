import numpy as np
from numpy import linalg as LA

def get_ratings_avg(user_id):
    """
    Calculate the averages of the ratings for each user
    :param user_id: all movies that a user seen and not seen with ratings
    :return: float number
    """
    sum = 0
    count = 0
    for rating in user_id:
        if rating != "?":
          sum += rating
          count += 1
    return float("{0:.10f}".format(sum/count))

def smooth_user_ratings(user_movie):
    """
    :param user_movie: all ratings a user given a movie, if not given is equal '?'
    :return: a numpy array that is (user rating) - (average user ratings)
    """
    numpy_user_movie = user_movie.to_numpy().copy()

    for i, user_id in enumerate(numpy_user_movie):
        sim = get_ratings_avg(user_id)
        for j, user_ratings in enumerate(user_id):
            if user_ratings != '?':  # user has already watched it!
                numpy_user_movie[i][j] = float("{0:.10f}".format((sim - user_ratings)))


    return numpy_user_movie



def similarity_between_users(numpy_user_movie, user_query):
    users_similarity = {}
    for user_id, ratings in enumerate(numpy_user_movie):
        if user_id == user_query:
            continue
        user_choosen = []
        user_watch_film = []
        for i, x in enumerate(numpy_user_movie[user_query]):
            if numpy_user_movie[user_query][i] != '?' and numpy_user_movie[user_id][i] != '?':
                user_choosen.append(numpy_user_movie[user_query][i])
                user_watch_film.append(numpy_user_movie[user_id][i])

        if LA.norm(user_choosen) * LA.norm(user_watch_film) == 0:
            users_similarity[(user_query, (user_id))] = 0
        else:
            users_similarity[(user_query, (user_id))] = float("{0:.10f}".format(
                (np.dot(user_choosen, user_watch_film)) / (LA.norm(user_choosen) * LA.norm(user_watch_film))))

    return users_similarity

def normalization_top10(data, user_movie, movies):

    result = {}
    temp = sorted(data, key=data.get, reverse=True)

    min_data = data[temp[len(temp)-1]]
    max_data = data[temp[0]]

    for i, value in enumerate(temp):
        new_value = ( (data[value] - min_data) / (max_data - min_data) ) * (5 - 0) + 0
        movie_id = user_movie[user_movie.columns[value[1]]].name
        name_movie = movies[movies['movie_id'] == int(movie_id)]['movie_title'].to_list()[0]
        result[name_movie] = new_value
        if i == 10:
            break

    return result


def user_based_recommender(user_query, ratings, movies):
    """
    :param user_query: The user which we want ratings in movies that have not seen them.
    :param ratings: datasets
    :param movies: dataset
    :return: Top 10 ratings
    """
    result = {}

    # make a new dataset for the project cause it makes it easier for us.
    user_movie = ratings.pivot(index='user_id', columns='movie_id', values='user_rating')
    user_movie = user_movie.fillna("?")
    numpy_user_movie = smooth_user_ratings(user_movie)
    numpy_user = user_movie.to_numpy().copy()
    rating_avg_user_selcted = get_ratings_avg(numpy_user[user_query])

    users_similarity = similarity_between_users(numpy_user_movie, user_query)

    for film_id in range(0, len(user_movie.columns)):
        if numpy_user_movie[user_query][film_id] != '?':
            continue

        users_watched_film_id = {}
        for user_id, user_ratings in enumerate(numpy_user_movie):
            if numpy_user_movie[user_id][film_id] != '?':
                users_watched_film_id[user_id] = numpy_user_movie[user_id][film_id]

        t1 = 0
        t2 = 0
        for user in users_watched_film_id.keys():
            t1 += users_watched_film_id[user] * users_similarity[(user_query, (user))]
            t2 += users_watched_film_id[user]

        result[(user_query, film_id)] = rating_avg_user_selcted + t1 / np.abs(t2)

    return normalization_top10(result, user_movie, movies)

