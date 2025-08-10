from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from modules.gemini_utils import embed_text

class LocalEmbeddingWrapper:
    """Wraps the local embed_text function for langchain compatibility."""
    def embed_documents(self, texts):
        # texts is a list of strings; return list of vector lists
        return [embed_text(t) for t in texts]
    
    def embed_query(self, text):
        # single query embedding
        return embed_text(text)

def create_vectorstore_from_transcript(transcript):
    """
    Split transcript into chunks, embed them locally, and store in a Chroma vector DB.
    """
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(transcript)

    # Use local embeddings wrapper
    local_embeddings = LocalEmbeddingWrapper()

    # Create Chroma vectorstore using local embeddings
    vectorstore = Chroma.from_texts(chunks, embedding=local_embeddings)
    return vectorstore
def query_vectorstore(vectorstore, query, k=3):
    """
    Search the vectorstore for the most relevant chunks for the query.
    Returns concatenated text of top k documents.
    """
    docs = vectorstore.similarity_search(query, k=k)
    return " ".join([doc.page_content for doc in docs])
