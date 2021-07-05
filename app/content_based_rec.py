import numpy as np
import pandas as pd
import sklearn
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import difflib

<<<<<<< HEAD

print("Start import")
=======
id_array = []

>>>>>>> a09a59ce8adc253a91de9388ff9a783121e2eb85
credits = pd.read_csv (r'./data/credits.csv', low_memory=False)
keywords = pd.read_csv (r'./data/keywords.csv', low_memory=False)
metadata = pd.read_csv (r'./data/movies_metadata.csv', low_memory=False)
print("Import finished")


# Remove all rows where the id contains a "-", because some corrupted entries were found, where the date column slipped into the id column
print("Start metadata clear")
metadata = metadata[~metadata.id.str.contains("-")]
print("Finish metadata clear")


# Convert IDs to int. Required for merging
print("Start conversion to IDs - int")
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
metadata['id'] = metadata['id'].astype('int')
print("Conversion to IDs - int finished")



# Merge keywords and credits into your main metadata dataframe
print("Merging start")
metadata = metadata.merge(credits, on='id')
metadata = metadata.merge(keywords, on='id')
print("Merging finished")

# Parse the stringified features into their corresponding python objects
print("Feature casting start")
features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    metadata[feature] = metadata[feature].apply(literal_eval)
print("Feature casting finished")

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []


# Define new director, cast, genres and keywords features that are in a suitable form.
print("Start get director")
metadata['director'] = metadata['crew'].apply(get_director)
print("Finished get director")

print("Start get feature list")
features = ['cast', 'keywords', 'genres']
for feature in features:
    metadata[feature] = metadata[feature].apply(get_list)
print("Finished get feature list")

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

# Apply clean_data function to your features.
features = ['cast', 'keywords', 'director', 'genres']
print("Start clean data")
for feature in features:
    metadata[feature] = metadata[feature].apply(clean_data)
print("Finished clean data")

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

# Create a new soup feature
print("Start create soup")
metadata['soup'] = metadata.apply(create_soup, axis=1)
print("Finished create soup")

# create count matrix with CountVectorizer
print("Start Count Vectorizer")
count = CountVectorizer(stop_words='english')
print("Finished Count Vectorizer")
print("Start Count Matrix")
count_matrix = count.fit_transform(metadata['soup'])
print("Finished Count Matrix")

# Compute the Cosine Similarity matrix based on the count_matrix
print("Start cosine Sim")
cosine_sim = cosine_similarity(count_matrix, count_matrix)
#cosine_sim = pd.read_csv(r'./data/cosine_sim.csv')
#cosine_sim = cosine_sim.to_numpy()
print("Finished Cosine Sim")
print("start exporting")
pd.DataFrame(cosine_sim).to_csv(r'./cosine_sim3', compression='gzip')

# Reset index of your main DataFrame and construct reverse mapping as before
print("Start Reset Index")
metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata['id'])
print("Finished reset index")

def get_recommendations(id, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[id]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return metadata['title'].iloc[movie_indices]

def get_close_movie_ids(input_title):
    global id_array
    id_array = []
    possible_titles = difflib.get_close_matches(input_title, metadata['original_title'].tolist(), 4)
    for i in possible_titles:
        id_array.append(metadata.loc[metadata['original_title'] == str(i), 'id'].array[0])
    return id_array
    
def get_chosen_movie_id(input_id_array_pos):
    global id_array
    chosen_id = id_array[input_id_array_pos]
    return chosen_id  




