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
movies_dislike = []
random_ids = []

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
# Home
@app.route('/')
def home():
    global movies_like
    global movies_dislike
    global random_ids

    #choosing 10 random movie ids from collection
    if len(random_ids) <= 10:
        for i in range(10 - len(random_ids)):
            random_id(random_ids)
    
    return render_template("home.html", 
                            random_ids = random_ids,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like)

@app.route('/like', methods=['POST', 'GET'])
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

    return render_template("home.html",
                            random_ids = random_ids,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like,
                            movies_dislike = movies_dislike)

@app.route('/recommendation')
def recommendation():
    global movies_like
    global movies_dislike
    global random_ids

    movies_like = []
    movies_dislike = []
    recommendation = ['35023', '51955', '397552', '58995']
    
    return render_template("recommendation.html", 
                            recommendation = recommendation,
                            get_title = get_title,
                            get_date = get_date,
                            get_overview = get_overview,
                            movies_like = movies_like)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)