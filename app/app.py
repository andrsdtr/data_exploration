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
global movies_like
movies_like = []
# Home
@app.route('/')

def home():
    #choosing 10 random movieIds from collection
    global movies_like
    random_ids = []
    for i in range(10):
        random_ids.append(random.choice(movies_metadata.loc[:,'id'].array))
    
    def get_title(id):
        return movies_metadata.loc[movies_metadata['id'] == str(id), 'title'].array[0]
    def get_date(id):
        return movies_metadata.loc[movies_metadata['id'] == str(id), 'release_date'].array[0]
    def like(id):
        movies_like.append(id)
        print(id, movies_like)
        return ""
    
    return render_template("home.html", 
                            random_ids = random_ids,
                            get_title = get_title,
                            get_date = get_date,
                            like = like,
                            movies_like = movies_like)

#def picked_movies():
#    if request.form.get("like"):
#        movies_like.append(id)
#
#    
#    return render_template("home.html", 
#                            random_ids = random_ids,
#                            get_title = get_title,
#                            get_date = get_date,
#                            like = like,
#                            movies_like = movies_like)
#


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)