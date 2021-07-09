#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, session
import numpy as np
from numpy.lib.type_check import nan_to_num
import pandas as pd
import random

from rating_based import multi_recommendation
from rating_based import get_close_movie_ids
#import content_based_rec

app = Flask(__name__)

#ratings_small = pd.read_csv (r'./../data/ratings_small.csv')
#credits = pd.read_csv (r'./../data/credits.csv')
#keywords = pd.read_csv (r'./../data/keywords.csv')
#links = pd.read_csv (r'./../data/links.csv')
#links_small = pd.read_csv (r'./../data/links_small.csv')
movies = pd.read_csv (r'./data/movies.csv')
movies_metadata = pd.read_csv (r'./data/movies_metadata.csv')
movies_like = []
movies_dislike = []
random_ids = []
search_array = ''

#function to create random movie ids
def random_id(ids): 
    global movies_like
    global movies_dislike
    global random_ids
    id = random.choice(movies.loc[:,'movieId'].array)
    if id in movies_like or id in movies_dislike or id in random_ids:
        return 'repeat'
    elif id not in movies_like or id not in movies_dislike or id not in random_ids:
        random_ids.append(id)

#functions to get movie from dataset 1 (used for rating)
def get_title(id):
    return movies.loc[movies['movieId'] == int(id), 'title'].array[0][:-6]
def get_date(id):
    return movies.loc[movies['movieId'] == int(id), 'title'].array[0][-6:]
def get_overview(id):
    return movies.loc[movies['movieId'] == int(id), 'genres'].array[0]

#functions to get movie from dataset 2 (used for rating)
def get_title_meta(id):
    return movies_metadata.loc[movies_metadata['id'] == str(id), 'original_title'].array[0]
def get_date_meta(id):
    return movies_metadata.loc[movies_metadata['id'] == str(id), 'release_date'].array[0]
def get_overview_meta(id):
    if movies_metadata.loc[movies_metadata['id'] == str(id), 'overview'].array[0] == '':
        return 'no overview available'
    else:
        return movies_metadata.loc[movies_metadata  ['id'] == str(id), 'overview'].array[0]

#homepage
@app.route('/', methods=['POST', 'GET'])
def start():
    return render_template("start.html")

#pick movies page                           
@app.route('/pick')
def home():
    global movies_like
    global movies_dislike
    global random_ids

    #choosing 10 random movie ids from collection
    if len(random_ids) <= 10:
        for i in range(10 - len(random_ids)):
            random_id(random_ids)
    
    return render_template("pick.html", 
                            random_ids = random_ids,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like)

#process picked movies
@app.route('/pick', methods=['POST', 'GET'])
def picked_movies():
    global movies_like
    global movies_dislike
    global random_ids 
    
    #handling like or dislike button press
    if request.method == 'POST':
        if request.form.get("like"):
            movies_like.append(int(request.form['like']))
            if int(request.form['like']) in random_ids:
                random_ids.remove(int(request.form['like']))
            random_id(random_ids)
        elif request.form.get("dislike"):
            movies_dislike.append(int(request.form['dislike']))
            if int(request.form['dislike']) in random_ids:
                random_ids.remove(int(request.form['dislike']))
            random_id(random_ids)

    return render_template("pick.html",
                            random_ids = random_ids,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like,
                            movies_dislike = movies_dislike)

#recommendation page
@app.route('/recommendation', methods=['POST', 'GET'])
def recommendation():
    global movies_like
    global movies_dislike
    global random_ids
    global search_array

    liste = []
    for i in movies_like:
        liste.append(int(i))

    recommendation = multi_recommendation(liste)
    movies_like = []
    movies_dislike = []
    
    #get movie search title
    if request.method == 'POST':
        movie_search_title = request.form.get("search")
        print(request.form.get("search"))
        search_array = get_close_movie_ids(movie_search_title)
    
    #get search possibilities
    #content_based_rec.get_close_movie_ids(movie_search_title)

    #get movie search id
    #if request.method == 'POST':
    #    movie_search_id = request.form.get("search")                # <---  !!!!!!!!!!! change to id form

    #get chosen movie id
    #content_based_rec.get_choose_movie_id(movie_search_id)

    #get recommendation
    #content_based_rec.get_recommendation(content_based_rec.chosen_id, content_based_rec.cosine_sim)

    return render_template("recommendation.html", 
                            recommendation = recommendation,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like)

#search a movie page
@app.route('/search')
def search():
    hide = "" 
    return render_template("search.html",
                            hide = hide)

#search results page
@app.route('/search', methods=['POST', 'GET'])
def search_result():
    global search_array
    search_input = request.form.get('search')
    search_array = get_close_movie_ids(search_input)
    hide = "hide"
    return render_template("search.html",
                            get_title = get_title_meta,
                            get_date = get_date_meta,
                            get_overview = get_overview_meta,
                            search_array = search_array,
                            hide = hide)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)