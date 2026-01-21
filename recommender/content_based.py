import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_movies():
    df = pd.read_csv("data/tmdb_5000_movies.csv")
    df = df[["title", "overview"]]
    df["overview"] = df["overview"].fillna("")
    return df

def recommend(movie_title, top_n=5):
    movies = load_movies()

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies["overview"])

    similarity = cosine_similarity(tfidf_matrix)

    if movie_title not in movies["title"].values:
        return []

    index = movies[movies["title"] == movie_title].index[0]
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    return [movies.iloc[i[0]]["title"] for i in scores[1: top_n + 1]]
