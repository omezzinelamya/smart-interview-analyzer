import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(context, question):
    """
    Ask Gemini a question based on the interview transcript context.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Based on the interview transcript below, answer the question.\n"
        f"Transcript: {context}\n"
        f"Question: {question}"
    )
    response = model.generate_content(prompt)
    return response.text

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from modules.gemini_utils import embed_text

class LocalEmbeddingWrapper:
    def embed_documents(self, texts):
        return [embed_text(t) for t in texts]
    def embed_query(self, text):
        return embed_text(text)

embedding_instance = LocalEmbeddingWrapper()

def match_candidate(transcript: str, job_requirements: str) -> str:
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    transcript_chunks = splitter.split_text(transcript)

    # Create vectorstore with chunks and local embeddings
    vectorstore = Chroma.from_texts(transcript_chunks, embedding=embedding_instance)
 
    # Embed job requirements query
    job_embedding = embed_text(job_requirements)

    # Search top 5 relevant chunks
    results = vectorstore.similarity_search_by_vector(job_embedding, k=5)

    match_count = len(results)
    score = min(100, match_count * 20)

    if score > 70:
        assessment = "Strong match! The candidate fits well with the job requirements."
    elif score > 40:
        assessment = "Moderate match. Candidate may meet some requirements."
    else:
        assessment = "Weak match. Candidate may not be the best fit."

    return f"Score: {score}/100\n{assessment}"
