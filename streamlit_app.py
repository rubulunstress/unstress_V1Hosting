import streamlit as st
from retriever import load_vectorstore, search_answer
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in your .env file.")
    st.stop()

# Initialize the vector store
vectorstore = load_vectorstore()

# Set up the prompt templates (same as in Flask app)
rag_prompt = PromptTemplate(
    input_variables=["input", "context"],
    template="""You are an emotionally intelligent AI designed to help Indian corporate professionals provide a safe environment for chatting. Then refine the retrieved answer to feel like a caring, emotionally aware friend is speaking — warm, simple, grounded. Without adding too much of your own.

Input Information:
- User message: {input}
- Retrieved answer: {context}

Your Core Tasks:
1. Understand the emotional need behind the user's message (e.g., are they tired, anxious, guilty, overwhelmed?)
2. Based on this need, refine the retrieved output for serving emotion without changing its core meaning

❌ Important DON'Ts:
- DO NOT add your own therapeutic advice beyond what was retrieved
- DO NOT overexplain — keep it light and emotionally attuned

🧠 Style Guidelines:
1. Use casual, clear English with gentle Hinglish phrases when natural
2. Keep responses short, crisp, clear and relevant
3. Use relatable corporate imagery if helpful (e.g., "feels like back-to-back meetings in your head")

Remember: Make your response feel seen, soft, and safe.

Now, provide your response for:
User message: {input}
Retrieved answer: {context}

Your response:"""
)

direct_prompt = PromptTemplate(
    input_variables=["input"],
    template="""
You are an emotionally intelligent AI designed to help Indian corporate professionals. The user has shared something with you, and you need to provide a warm, empathetic response.

Your task:
Understand the emotional need behind the user's message (e.g., are they tired, anxious, guilty, overwhelmed?)
Provide a caring, supportive response that makes them feel seen and understood.

🧠 Style Guide:
Use casual, clear English (optionally with gentle Hinglish phrases if needed)
Keep it short, crisp, clear and relevant
Use metaphors or relatable corporate imagery if helpful
Make it feel seen, soft, and safe

User message: {input}

Your response:
"""
)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.8, openai_api_key=OPENAI_API_KEY)

# Set page config
st.set_page_config(page_title="Therapy Chat", layout="centered")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat title
st.title("Therapy Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Get RAG result with threshold
                rag_result = search_answer(vectorstore, prompt, threshold=0.83)
                
                # Generate final response
                if rag_result:
                    final_prompt = rag_prompt.format(input=prompt, context=rag_result["answer"])
                else:
                    final_prompt = direct_prompt.format(input=prompt)
                
                response = llm.invoke(final_prompt).content
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}") 