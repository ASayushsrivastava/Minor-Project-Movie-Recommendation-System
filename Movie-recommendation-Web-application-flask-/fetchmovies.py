import pandas as pd
import pickle as pkl
import requests
import numpy as np
import os
import kagglehub

# Download the latest dataset using kagglehub
path = kagglehub.dataset_download("asaniczka/tmdb-movies-dataset-2023-930k-movies/versions/384")
print("Path to dataset files:", path)

# Load the downloaded CSV file
tmdb_file = os.path.join(path, "TMDB_movie_dataset_v11.csv")
df = pd.read_csv(tmdb_file)

# Load the pre-trained listOf5.pkl model
movie_list = os.path.join(path, 'listOf5.pkl')
with open(movie_list, 'rb') as f:
    rlist = pkl.load(f)
rlist = np.array(rlist)

# Getting the title list of the movies
names = df["original_title"]

# Function to search movies
def searchMovies(substring):
    substring = substring.lower()
    search_movies = []
    count = 0
    for s in names:
        if count > 4:
            break
        if substring in s.lower():
            count += 1
            search_movies.append(s)
    return search_movies

# Fetch movie posters with error handling and placeholder fallback
def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f3a53ed2114253e84e595cf3c79549d9")
        response.raise_for_status()
        data = response.json()
        
        # Check if 'poster_path' is available and valid
        if 'poster_path' in data and data['poster_path']:
            return f'https://image.tmdb.org/t/p/w500{data["poster_path"]}'
        else:
            print(f"No poster path available for movie ID {movie_id}")
            # Return a placeholder image URL (ensure placeholder.jpg exists in static folder)
            return "/static/images/placeholder.jpg"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        # Use placeholder image in case of error
        return "/static/images/placeholder.jpg"

# Recommend 5 movies based on title with improved error handling
def reccomendMovies(title):
    try:
        movie_index = np.where(names == title)[0][0]
    except IndexError:
        print(f"Movie title '{title}' not found.")
        return [], [], []  # Return empty lists if title not found

    # Retrieve recommended movies and their details
    rmovies = rlist[movie_index]
    rmovie_titles = list(df.loc[rmovies, 'original_title'].values)
    movie_ids = df.loc[rmovies, 'id'].values.tolist()
    poster_urls = [fetch_poster(id) for id in movie_ids]

    return rmovie_titles, poster_urls, movie_ids
