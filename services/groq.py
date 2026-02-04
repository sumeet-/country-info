from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY

llm_groq_openai_gpt_oss_20b = ChatGroq(model="openai/gpt-oss-20b",
                                       temperature=0,
                                       api_key=GROQ_API_KEY)

llm_groq_qwen3_32b = ChatGroq(model="qwen/qwen3-32b",
                              temperature=0,
                              api_key=GROQ_API_KEY)
