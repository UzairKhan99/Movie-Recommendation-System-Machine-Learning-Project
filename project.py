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


movies["genres"] = movies["genres"].apply(helper)
movies["keywords"] = movies["keywords"].apply(helper)
movies["cast"] = movies["cast"].apply(counter3)
movies["crew"] = movies["crew"].apply(fetch_director)
movies["overview"] = movies["overview"].apply(lambda x: x.split())
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["tags"] = (
    movies["overview"] + movies["keywords"] + movies["crew"] + movies["cast"]
)
new_df = movies[["movie_id", "title", "tags"]]
new_df["tags"] = new_df["tags"].apply(lambda x: "".join(x))
new_df["tags"].apply(lambda x: x.lower())
print(new_df.head(10))
