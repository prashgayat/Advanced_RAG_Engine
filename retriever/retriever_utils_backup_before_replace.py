# retriever/retriever_utils.py

import os
import faiss
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

class HybridRetriever:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2"):
        self.vectorizer = TfidfVectorizer()
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.faiss_index = None
        self.embeddings = None
        self.text_chunks = []

    def build_index(self, chunks: List[str]):
        self.text_chunks = chunks

        # TF-IDF for keyword search
        self.vectorizer.fit(chunks)

        # Embeddings for FAISS
        self.embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
        dimension = self.embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(self.embeddings)

    def save_index(self, path: str):
        faiss.write_index(self.faiss_index, os.path.join(path, "faiss.index"))
        with open(os.path.join(path, "retriever_data.pkl"), "wb") as f:
            pickle.dump({
                "chunks": self.text_chunks,
                "vectorizer": self.vectorizer
            }, f)

    def load_index(self, path: str):
        self.faiss_index = faiss.read_index(os.path.join(path, "faiss.index"))
        with open(os.path.join(path, "retriever_data.pkl"), "rb") as f:
            data = pickle.load(f)
            self.text_chunks = data["chunks"]
            self.vectorizer = data["vectorizer"]
            self.embeddings = self.embedding_model.encode(self.text_chunks)

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        # Semantic
        query_vector = self.embedding_model.encode([query])
        _, faiss_indices = self.faiss_index.search(query_vector, top_k)
        semantic_results = [(self.text_chunks[i], 1.0) for i in faiss_indices[0]]

        # Keyword
        tfidf_vec = self.vectorizer.transform([query])
        tfidf_scores = np.dot(tfidf_vec, self.vectorizer.transform(self.text_chunks).T).toarray().flatten()
        keyword_indices = tfidf_scores.argsort()[::-1][:top_k]
        keyword_results = [(self.text_chunks[i], tfidf_scores[i]) for i in keyword_indices]

        return semantic_results + keyword_results
