from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

class RecomendadorNetflix:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(df['description'])
        self.indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    def recomendar(self, titulo: str, n=5):
        if titulo not in self.indices:
            return []
        idx = self.indices[titulo]
        cosine_sim = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[-n-1:-1][::-1]
        return self.df.iloc[similar_indices][['title', 'description']].to_dict(orient="records")