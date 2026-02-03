from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY

groq_llm = ChatGroq(model="qwen/qwen3-32b",
                    temperature=0,
                    api_key=GROQ_API_KEY)
