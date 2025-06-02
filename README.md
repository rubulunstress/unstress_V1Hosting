# Unstress Therapy Chat

An AI-powered mental health companion built with Streamlit and LangChain.

## Features
- Interactive chat interface
- AI-powered responses using RAG (Retrieval Augmented Generation)
- Professional and user-friendly design
- Secure API key management

## Setup Instructions

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run main.py
```

## Deployment
The application can be deployed on Streamlit Cloud or any other platform that supports Python applications.

### Streamlit Cloud Deployment
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set up your environment variables (OPENAI_API_KEY)
5. Deploy!

## Security Notes
- Never commit your `.env` file
- Keep your API keys secure
- The `.gitignore` file is configured to exclude sensitive information

## License
© 2024 Unstress. All rights reserved. 