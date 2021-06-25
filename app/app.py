#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, session
import numpy as np
import pandas as pd
import random

app = Flask(__name__)

#ratings_small = pd.read_csv (r'./../data/ratings_small.csv')
#credits = pd.read_csv (r'./../data/credits.csv')
#keywords = pd.read_csv (r'./../data/keywords.csv')
#links = pd.read_csv (r'./../data/links.csv')
#links_small = pd.read_csv (r'./../data/links_small.csv')
movies_metadata = pd.read_csv (r'./movies_metadata.csv')
movies_like = []
movie_search = []
movies_dislike = []
random_ids = []
movie_search = ''

#function to create random movie ids
def random_id(ids): 
    global movies_like
    global movies_dislike
    global random_ids
    id = random.choice(movies_metadata.loc[:,'id'].array)
    if id in movies_like or id in movies_dislike or id in random_ids:
        return 'repeat'
    elif id not in movies_like or id not in movies_dislike or id not in random_ids:
        random_ids.append(id)
#functions to get movie metadata
def get_title(id):
    return movies_metadata.loc[movies_metadata['id'] == str(id), 'title'].array[0]
def get_date(id):
    return movies_metadata.loc[movies_metadata['id'] == str(id), 'release_date'].array[0]
def get_overview(id):
    return movies_metadata.loc[movies_metadata['id'] == str(id), 'overview'].array[0]

#homepage
@app.route('/')
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
            movies_like.append(request.form['like'])
            if request.form['like'] in random_ids:
                random_ids.remove(request.form['like'])
            random_id(random_ids)
        elif request.form.get("dislike"):
            movies_dislike.append(request.form['dislike'])
            if request.form['dislike'] in random_ids:
                random_ids.remove(request.form['dislike'])
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
    global movie_search

    movies_like = []
    movies_dislike = []
    recommendation = ['35023', '51955', '397552', '58995']
    
    #get movie search
    if request.method == 'POST':
        movie_search = request.form.get("search")

    return render_template("recommendation.html", 
                            recommendation = recommendation,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like,
                            movie_search = movie_search)

#search a movie page
@app.route('/search')
def search():    
    return render_template("search.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)