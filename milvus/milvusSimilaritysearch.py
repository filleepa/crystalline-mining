from tqdm import tqdm
from joblib import load
import numpy as np
from pymilvus import MilvusClient

client = MilvusClient(uri="http://localhost:19530/")

embeddings = load(r"C:\Users\Philippa\Documents\GitHub\crystalline-mining\textual_analysis\BERTopic_embeddings.npy")
model = load(r"C:\Users\Philippa\Documents\GitHub\crystalline-mining\textual_analysis\BERTopic_model.pkl")
texts = load(r"C:\Users\Philippa\Documents\GitHub\crystalline-mining\textual_analysis\Raw_texts.npy")

def split_text_by_bytes(text, max_bytes=60000):  # Leave buffer below 65535
    """Split text into chunks that fit within max_bytes"""
    chunks = []
    text_bytes = text.encode('utf-8')
    
    for i in range(0, len(text_bytes), max_bytes):
        chunk_bytes = text_bytes[i:i+max_bytes]
        chunk = chunk_bytes.decode('utf-8', errors='ignore')
        chunks.append(chunk)
    return chunks

data = []
for i, text in enumerate(texts):
    embedding = embeddings[i].tolist()
    
    # Check byte length (not character length)
    text_byte_length = len(bytes(text, "utf-8"))
    
    if text_byte_length > 60000:  # Leave buffer for safety
        # Split the text into chunks
        text_chunks = split_text_by_bytes(text, max_bytes=60000)
        
        # Create multiple entries with same embedding
        for chunk in text_chunks:
            data.append({
                "text": chunk,
                "embeddings": embedding  # Same embedding for all chunks
            })
    else:
        # Text fits, add as single entry
        data.append({
            "text": text,
            "embeddings": embedding
        })

client.insert("crystalline_papers", data)