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
movies_metadata = pd.read_csv (r'./../data/movies_metadata.csv')

# Home
@app.route('/')
def home():
    #choosing 10 random movieIds from collection
    random_ids = []
    for i in range(10):
        random_ids.append(random.choice(movies_metadata.loc[:,'id'].array))
    
    movie_selection = []
    for i in random_ids:
        movie_selection.append(movies_metadata.loc[movies_metadata['id'] == str(i), 'original_title'].array[0])   
    return render_template("home.html", 
                            movie_selection=movie_selection)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)