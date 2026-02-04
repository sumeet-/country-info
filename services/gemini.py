from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY

llm_gemini_3_flash_preview = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0,
    api_key=GEMINI_API_KEY,
)