import os
import faiss
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document

class HybridRetriever:
    def __init__(self, faiss_index_path=None, tfidf_vectorizer_path=None, documents=None):
        self.faiss_index = None
        self.tfidf_vectorizer = None
        self.documents = documents or []
        self.openai_embeddings = OpenAIEmbeddings()

        if faiss_index_path and os.path.exists(faiss_index_path):
            self._load_faiss_index(faiss_index_path)
        
        if tfidf_vectorizer_path and os.path.exists(tfidf_vectorizer_path):
            self._load_tfidf_vectorizer(tfidf_vectorizer_path)

    def _load_faiss_index(self, faiss_index_path):
        with open(faiss_index_path, "rb") as f:
            self.faiss_index = pickle.load(f)

    def _load_tfidf_vectorizer(self, tfidf_vectorizer_path):
        with open(tfidf_vectorizer_path, "rb") as f:
            self.tfidf_vectorizer = pickle.load(f)

    def _build_faiss_index(self, texts):
        embeddings = self.openai_embeddings.embed_documents(texts)
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings, dtype=np.float32))
        self.faiss_index = index

    def _build_tfidf_vectorizer(self, texts):
        vectorizer = TfidfVectorizer()
        vectorizer.fit(texts)
        self.tfidf_vectorizer = vectorizer

    def save_faiss_index(self, faiss_index_path):
        with open(faiss_index_path, "wb") as f:
            pickle.dump(self.faiss_index, f)

    def save_tfidf_vectorizer(self, tfidf_vectorizer_path):
        with open(tfidf_vectorizer_path, "wb") as f:
            pickle.dump(self.tfidf_vectorizer, f)

    def build_indexes(self, texts):
        self._build_faiss_index(texts)
        self._build_tfidf_vectorizer(texts)

    def retrieve(self, query, top_k=5):
        faiss_results = self._retrieve_faiss(query, top_k)
        tfidf_results = self._retrieve_tfidf(query, top_k)
        combined_results = self._combine_results(faiss_results, tfidf_results)
        return combined_results

    def _retrieve_faiss(self, query, top_k):
        if self.faiss_index is None:
            return []
        query_embedding = self.openai_embeddings.embed_query(query)
        D, I = self.faiss_index.search(np.array([query_embedding], dtype=np.float32), top_k)
        return [self.documents[i] for i in I[0] if i < len(self.documents)]

    def _retrieve_tfidf(self, query, top_k):
        if self.tfidf_vectorizer is None:
            return []
        query_vec = self.tfidf_vectorizer.transform([query])
        doc_vecs = self.tfidf_vectorizer.transform([doc.page_content for doc in self.documents])
        scores = (doc_vecs * query_vec.T).toarray()
        ranked_indices = np.argsort(scores.flatten())[::-1]
        return [self.documents[i] for i in ranked_indices[:top_k] if i < len(self.documents)]

    def _combine_results(self, faiss_results, tfidf_results):
        seen = set()
        combined = []
        for doc in faiss_results + tfidf_results:
            if doc.page_content not in seen:
                combined.append(doc)
                seen.add(doc.page_content)
        return combined
