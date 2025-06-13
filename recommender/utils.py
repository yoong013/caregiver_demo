# recommender/utils.py
import pandas as pd
from langchain.docstore.document import Document
# from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load Excel into pandas
def load_caregivers(path="caregivers.csv"):
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        text = (
            f"Name: {row.Name}\n"
            f"Skills: {row.Skills}\n"
            f"Experience: {row.Experience}\n"
            f"Location: {row.Location}\n"
            f"Notes: {row.Notes}"
        )
        metadata = row.to_dict()
        docs.append(Document(page_content=text, metadata=metadata))
    return docs

# 2. Build FAISS index (in-memory)
def build_vectorstore(docs, persist_path=None):
    # embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedder)
    # Optional: persist to disk
    # if persist_path:
    #     vectorstore.save_local(persist_path)
    return vectorstore