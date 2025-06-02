# ======================= retriever.py =======================
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in your .env file.")

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def load_vectorstore(persist_directory="./chroma_therapy"):
    return Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def search_answer(vectorstore, query, threshold=0.83):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    results = retriever.get_relevant_documents(query)

    if not results:
        return None

    # Embed the query and the retrieved doc to calculate similarity
    query_vector = embedding_model.embed_query(query)
    doc_vector = embedding_model.embed_query(results[0].page_content)
    similarity = cosine_similarity(query_vector, doc_vector)
    
    print(f"\nSimilarity score: {similarity:.4f}")

    if similarity >= threshold:
        return {
            "answer": results[0].metadata["answer"],
            "similarity": round(float(similarity), 4),
            "retrieved_question": results[0].page_content
        }
    else:
        return None

if __name__ == "__main__":
    vs = load_vectorstore()
    while True:
        user_input = input("\nEnter your query (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        result = search_answer(vs, user_input)
        if result:
            print("\nAnswer:", result)
        else:
            print("\nNo answer found (similarity too low)")