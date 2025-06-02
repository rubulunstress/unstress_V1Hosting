import pandas as pd
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in your .env file.")

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


def load_qna_from_excel(file_path, sheet_name="transcripts&comments_pairs"):
    try:
        # Read Excel without header
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        qna_list = []
        for _, row in df.iterrows():
            # First column (index 0) contains 'I', second column (index 1) contains 'O'
            question = str(row[0]).strip()
            answer = str(row[1]).strip()
            qna_list.append({"question": question, "answer": answer})
        return qna_list
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return []


def store_qna_in_chroma(qna_data, persist_directory="./chroma_therapy"):
    if not qna_data:
        print("No data to store in Chroma")
        return None
        
    documents = [
        Document(
            page_content=qa["question"],
            metadata={"answer": qa["answer"]}
        )
        for qa in qna_data
    ]

    try:
        vectorstore = Chroma.from_documents(
            documents,
            embedding_model,
            persist_directory=persist_directory
        )
        print(f"Successfully stored {len(documents)} documents in Chroma")
        return vectorstore
    except Exception as e:
        print(f"Error storing documents in Chroma: {e}")
        return None


if __name__ == "__main__":
    # Make sure the Excel file exists
    excel_file = "Copy of Mental_Health.xlsx"
    if not os.path.exists(excel_file):
        print(f"Error: {excel_file} not found in current directory")
    else:
        print(f"Loading data from {excel_file}...")
        qna_data = load_qna_from_excel(excel_file)
        if qna_data:
            print(f"Loaded {len(qna_data)} Q&A pairs")
            vectorstore = store_qna_in_chroma(qna_data)
            if vectorstore:
                print("Vector store created successfully")
        else:
            print("No data was loaded from the Excel file") 