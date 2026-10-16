import os

from dotenv                import load_dotenv
from pinecone              import Pinecone
from langchain_pinecone    import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX   = os.getenv("PINECONE_INDEX")


pc = Pinecone(
    api_key = PINECONE_API_KEY
)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


index = pc.Index(PINECONE_INDEX)


vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)


retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 4
    }
)


