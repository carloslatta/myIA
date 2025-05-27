# semantic_search.py - Integración de búsqueda semántica con sentence-transformers
from sentence_transformers import SentenceTransformer
import numpy as np
import torch

class SemanticSearch:
    def __init__(self):
        self.model = None
        self.embeddings = {}
        self.initialized = False
        
    def initialize(self):
        try:
            print("🔄 Cargando modelo de búsqueda semántica...")
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.initialized = True
            print("✅ Modelo semántico cargado")
        except Exception as e:
            print(f"❌ Error al cargar modelo semántico: {e}")
            self.initialized = False
        
    def get_embedding(self, text):
        if not self.initialized:
            self.initialize()
        return self.model.encode(text)
        
    def semantic_similarity(self, text1, text2):
        if not self.initialized:
            return 0.0
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

semantic_search = SemanticSearch()