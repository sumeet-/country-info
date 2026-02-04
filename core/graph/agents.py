from langchain.agents.middleware import ModelFallbackMiddleware

from core.graph.state import IntentAnalysisResult, FinalAnswerResult
from langchain.agents import create_agent
from core.prompt import FINAL_ANSWER_SYSTEM_PROMPT, INTENT_SYSTEM_PROMPT
from services.gemini import llm_gemini_3_flash_preview
from services.groq import llm_groq_qwen3_32b, llm_groq_openai_gpt_oss_20b

# Agent for intent identification
intent_analyzer_agent = create_agent(
    llm_groq_qwen3_32b,
    system_prompt=INTENT_SYSTEM_PROMPT,
    response_format=IntentAnalysisResult,
    middleware=[ModelFallbackMiddleware(llm_gemini_3_flash_preview)]
)

# Agent to synthesize final answer
final_answer_synthesis_agent = create_agent(
    llm_groq_openai_gpt_oss_20b,
    system_prompt=FINAL_ANSWER_SYSTEM_PROMPT,
    response_format=FinalAnswerResult,
    middleware=[ModelFallbackMiddleware(llm_gemini_3_flash_preview)]
)
