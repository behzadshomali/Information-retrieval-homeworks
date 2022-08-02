def make_description_for_user(ratings):
    user_description = {}
    for user_id in np.unique(ratings['user_id']):
        gender = ratings[ratings['user_id'] == user_id].user_gender.to_list()[0]
        job = ratings[ratings['user_id'] == user_id].user_occupation_text.to_list()[0]
        desctription = f"I am a {gender}, my job is {job}. "
        for user_ratings in np.unique(ratings['user_rating']):
            movie_name = ", ".join(
                ratings[ratings['user_id'] == user_id][ratings['user_rating'] == user_ratings]['movie_title'].to_list())
            if len(movie_name) > 2:
                desctription += f"I gave these films a score of {user_ratings}: {movie_name}. "
            else:
                desctription += f"I have not given a score of {user_ratings} to any film. "

        user_description[user_id] = desctription

    return user_description