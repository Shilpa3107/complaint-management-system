from langchain_groq import ChatGroq
from app.core.config import settings

extraction_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=settings.GROQ_API_KEY,
)

reasoning_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=settings.GROQ_API_KEY,
)