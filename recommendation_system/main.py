from recommendation_system.preprocess import preprocess_data
from recommendation_system.user_based import user_based_recommender
from recommendation_system.item_based import item_based_recommend, item_based, get_user_not_rating, top10
from recommendation_system.content_based import content_based
from threading import Thread


ratings, movies = preprocess_data("data/ratings.parquet.gzip", "data/movies.parquet.gzip")

# user based recommendation
result = user_based_recommender(0, ratings, movies)
print(result)

# item based recommendation
user_movie = ratings.pivot(index='user_id',columns='movie_id',values='user_rating')
user_movie = user_movie.fillna("?")
numpy_user_movie = user_movie.to_numpy().copy()


movies_similarity = item_based(ratings)

user_query_not_ratings = get_user_not_rating(0, numpy_user_movie)
n = 300
count = 0
result = {}
threads = []
for i in range(0, len(user_query_not_ratings), n):
    t = Thread(target=item_based_recommend, args=(0, result, user_query_not_ratings[i:i + n],))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

top10_movies = top10(result, user_movie, movies)
print(top10_movies)

# Content based recommendation
result = content_based(movies, ratings, 10)
print(result)