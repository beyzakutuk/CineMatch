# recommender/content_based.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, data_path="data/combined_titles.csv"):
        self.df = pd.read_csv(data_path)
        self.df.dropna(subset=["description"], inplace=True)

        # İçerik: açıklama + tür
        self.df["content"] = self.df["description"] + " " + self.df["listed_in"]

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["content"])

    def recommend_by_title(self, input_title, n=5):
        input_title = input_title.strip().lower()
        matches = self.df[self.df['title'].str.lower() == input_title]

        if matches.empty:
            return []

        idx = matches.index[0]
        cosine_similarities = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_similarities.argsort()[-n-1:-1][::-1]

        recommended = self.df.iloc[similar_indices][['show_id', 'title', 'platform', 'listed_in']]
        return recommended.to_dict(orient="records")
