import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
credits = pd.read_csv("tmdb_5000_credits.csv")
movies = pd.read_csv("tmdb_5000_movies.csv")

# Merge on title
movies = movies.merge(credits, on="title", how="left")

# Keep only selected features
features = ["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]
movies = movies[features]

# Drop missing and duplicate rows
movies.dropna(inplace=True)
movies.drop_duplicates(inplace=True)


# Helper functions
def helper(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L


def counter3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
            break
    return L


def recommend(movie_title):
    movie_index = new_df[new_df["title"] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    return movies_list


# Apply functions to columns
movies["genres"] = movies["genres"].apply(helper)
movies["keywords"] = movies["keywords"].apply(helper)
movies["cast"] = movies["cast"].apply(counter3)
movies["crew"] = movies["crew"].apply(fetch_director)

# Convert overview into list of words
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Remove spaces in multi-word genres
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])

# Create 'tags' by combining lists
movies["tags"] = (
    movies["overview"] + movies["keywords"] + movies["crew"] + movies["cast"]
)
print(movies["tags"].head())

# Keep only relevant columns
new_df = movies[["movie_id", "title", "tags"]]

# Join lists into a single lowercase string
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())

# Initialize stemmer
ps = PorterStemmer()


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# Apply stemming
new_df["tags"] = new_df["tags"].apply(stem)

# Create CountVectorizer object
cv = CountVectorizer(max_features=5000, stop_words="english")

# Convert tags into vectors
vectors = cv.fit_transform(new_df["tags"]).toarray()

similarity = cosine_similarity(vectors).shape
sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x: x[1])
