from core.graph.state import IntentAnalysisResult, FinalAnswerResult
from langchain.agents import create_agent
from core.prompt import FINAL_ANSWER_SYSTEM_PROMPT, INTENT_SYSTEM_PROMPT
from services.groq import groq_llm

# Agent for intent identification
intent_analyzer_agent = create_agent(
    groq_llm,
    system_prompt=INTENT_SYSTEM_PROMPT,
    response_format=IntentAnalysisResult,
)

# Agent to synthesize final answer
final_answer_synthesis_agent = create_agent(
    groq_llm,
    system_prompt=FINAL_ANSWER_SYSTEM_PROMPT,
    response_format=FinalAnswerResult
)
