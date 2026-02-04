from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    """
    State that flows through the graph.
    Each node can read from and update this state.
    """
    user_question: str                            # Original user query
    country_name: str                             # Extracted country name
    fields_requested: list[str]                   # What information user wants
    extra_info: str                               # Some extra context or instructions
    api_data: dict                                # Raw data from REST Countries API
    final_answer: str                             # Generated response
    error: str                                    # Error message if any
    messages: Annotated[list, operator.add]       # Conversation history
    node_stage: str                               # Current node stage in the graph

# Schema for intent analysis result
class IntentAnalysisResult(TypedDict):
    country_name: str | None
    fields_requested: list[str]
    extra_info: str| None
    error: str | None

# Schema for final answer result
class FinalAnswerResult(TypedDict):
    final_answer: str