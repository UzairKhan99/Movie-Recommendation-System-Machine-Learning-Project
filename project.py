import numpy as np
import pandas as pd
import ast

credits = pd.read_csv("tmdb_5000_credits.csv")
movies = pd.read_csv("tmdb_5000_movies.csv")

movies = movies.merge(credits, on="title", how="left")
features = ["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]
movies = movies[features]
movies.dropna(inplace=True)
movies.duplicated().sum()
print(movies.iloc[0].genres)


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
    return

def Fetch_director()


movies["genres"] = movies["genres"].apply(helper)

movies["keywords"] = movies["keywords"].apply(helper)
movies["cast"] = movies["cast"].apply(counter3)
print(movies.head())
