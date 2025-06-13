import pandas as pd
from langchain.docstore.document import Document
# 1. Load CSV into pandas
def load_caregivers(path="caregivers.csv"):
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        text = (
            f"Name: {row.Name}"
            f"Skills: {row.Skills}"
            f"Experience: {row.Experience}"
            f"Location: {row.Location}"
            f"Notes: {row.Notes}"
        )
        metadata = row.to_dict()
        docs.append(Document(page_content=text, metadata=metadata))
    return docs

# 2. Build FAISS index (in-memory)
def build_vectorstore(docs, persist_path=None):
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedder)
    # Optional: persist to disk
    # if persist_path:
    #     vectorstore.save_local(persist_path)
    return vectorstore