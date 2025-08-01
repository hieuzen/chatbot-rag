import os
import glob
import faiss
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

TXT_FOLDER = "rag/txt_files"
VECTOR_PATH = "rag/vectorstore.pkl"

def load_documents():
    texts = []
    for filepath in glob.glob(f"{TXT_FOLDER}/*.txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            chunks = [content[i:i+500] for i in range(0, len(content), 500)]
            texts.extend(chunks)
    return texts

def build_vectorstore():
    documents = load_documents()
    vectorizer = TfidfVectorizer().fit(documents)
    vectors = vectorizer.transform(documents).toarray()
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(np.array(vectors).astype(np.float32))
    with open(VECTOR_PATH, "wb") as f:
        pickle.dump((index, documents, vectorizer), f)

def load_vectorstore():
    if not os.path.exists(VECTOR_PATH):
        build_vectorstore()
    with open(VECTOR_PATH, "rb") as f:
        return pickle.load(f)

index, documents, vectorizer = load_vectorstore()

def get_rag_response(query):
    query_vec = vectorizer.transform([query]).toarray().astype(np.float32)
    D, I = index.search(query_vec, k=3)
    results = [documents[i] for i in I[0]]
    return "\n".join(results)