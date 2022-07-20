from recommendation_system.preprocess import preprocess_data
from recommendation_system.user_based import user_based_recommender

ratings, movies = preprocess_data("data/ratings.parquet.gzip", "data/movies.parquet.gzip")

result = user_based_recommender(10, ratings, movies)

print(result)