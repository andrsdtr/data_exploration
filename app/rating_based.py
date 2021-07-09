import pandas as pd
import collections
import copy

#importing data
ratings = pd.read_csv (r'./data/ratings.csv')
movies = pd.read_csv (r'./data/movies.csv')

#creating table with movieId total count of ratings for each movie id
rating_info = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
rating_info['count'] = pd.DataFrame(ratings.groupby('movieId')['rating'].count())

#creating pivot table
rating_pivot = pd.pivot_table(ratings, index='userId', columns='movieId', values='rating')


import difflib
metadata = pd.read_csv (r'./data/movies_metadata.csv', low_memory=False)
def get_close_movie_ids(input_title):
    global id_array
    id_array = []
    possible_titles = difflib.get_close_matches(input_title, metadata['original_title'].tolist(), 4)
    for i in possible_titles:
        id_array.append(metadata.loc[metadata['original_title'] == str(i), 'id'].array[0])
    return id_array


#main algorithm function
def recommendation(movie_id):
    #calculating correlation to other users
    correlation = rating_pivot.corrwith(rating_pivot[movie_id])
    #creating table
    corr_movie = pd.DataFrame(correlation, columns=['correlation'])
    #dropping movies non values => no correlation
    corr_movie.dropna(inplace=True)
    #adding total count of ratings for each movie to the table
    corr_movie = corr_movie.join(rating_info['count'])
    #listing movies by correlation score and just using movies with more then the 90th percentile of the total count of ratings per movie
    cutoff = rating_info['count'].quantile(0.90)
    corr_movie = corr_movie[corr_movie['count']>cutoff].sort_values('correlation', ascending=False)
    #deleting movie that the recommendation is based on from recommendation list
    if movie_id in corr_movie.index:
        corr_movie = corr_movie.drop([movie_id])
    #changing index to ranking and movieId to column
    corr_movie['movieId'] = corr_movie.index
    corr_movie = corr_movie.set_index(pd.Index(list(range(len(corr_movie)))))
    return corr_movie

rec_count = None
def multi_recommendation(movie_ids):
    #function to get recommendation as an array of titles for multiple inputs  

    rec_movies_list = []
    rec_movies_dict = {}
    for i in movie_ids:
        global rec_count
        rec = recommendation(int(i))
        #skip if no correlating movies
        if rec.empty:
            continue
        #adding top 5 recommended movies to array 
        for k in range(5):
            rec_movies_list.append((rec.iloc[k].array[2]))
        #counting top recommended movies
        rec_count = collections.Counter(rec_movies_list)
        #adding top 5 recommended movies to array 
        for k in range(5):
            rec_movies_dict[rec.iloc[k][2]] = rec.iloc[k][0]
   
    #creating new score: count*correlation
    rec_movies_final = copy.deepcopy(rec_count) 
    for k in rec_count:
        rec_movies_final.update({k: rec_count.get(k) * rec_movies_dict.get(k) - rec_count.get(k)})
    
    return sorted(rec_movies_final, key=rec_movies_final.get, reverse=True)[:10]