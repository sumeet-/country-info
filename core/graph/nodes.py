import logging

from langchain_core.messages import HumanMessage

from services.rest_countries import fetch_country_data

from core.graph.enum import Node
from core.graph.state import AgentState
from core.graph.agents import intent_analyzer_agent, final_answer_synthesis_agent
from core.prompt import get_intent_human_message, get_synthesize_human_message


logger = logging.getLogger(__name__)

def identify_intent(state: AgentState) -> dict:
    """
    INTENT ANALYSIS NODE
    
    Uses LLM to extract:
    - Country name from the question
    - Specific fields of information requested by the user
    - Any other specific instructions or context
    """
    logger.info("Identifying intent...")
    messages = [
        HumanMessage(content=get_intent_human_message(state["user_question"]))
    ]
    
    response = intent_analyzer_agent.invoke({
        "messages": messages
    })
        # Parse LLM response
    intent_data = response.get("structured_response", {})
    logger.info(f"Intent analysis result: {intent_data}")
    return {
        "country_name": intent_data.get("country_name"),
        "fields_requested": intent_data.get("fields_requested", []),
        "extra_info": intent_data.get("extra_info", ""),
        "messages": [f"Intent analyzed: {intent_data}"],
        "error": intent_data.get("error"),
    }

# Node to fetch data from REST Countries API
def get_country_info(state: AgentState) -> dict:
    """
    TOOL CALLING NODE
    Fetches data from REST Countries API based on identified country name.
    """
    country = state.get("country_name")
    logger.info(f"Getting country info for {country}")
    # Clean up country name for API
    country_clean = country.strip()
    data = fetch_country_data(country_name=country_clean)

    return {
        "api_data": data,
        "messages": [f"Fetched data for {country_clean}"],
    }

# Node to synthesize final answer
def synthesize_final_answer(state: AgentState) -> dict:
    """
    ANSWER SYNTHESIS NODE
    Uses LLM to create a natural language answer from the API data
    """
    logger.info("Synthesizing final answer from API data")
    messages = [
        HumanMessage(
            content=get_synthesize_human_message(
                state["user_question"],
                state["fields_requested"],
                state["extra_info"],
                state["api_data"],
            )
        )
    ]
    response = final_answer_synthesis_agent.invoke({
        "messages": messages
    })
    structured_response = response.get("structured_response", {})
    final_answer = structured_response.get("final_answer", "")
    logger.info(f"Final synthesized answer: {final_answer}")
    return {
        "final_answer": final_answer,
        "messages": ["Final answer synthesized."],
        "node_stage": Node.SYNTHESIS
    }

# Node to handle errors
def handle_error(state: AgentState) -> dict:
    """
    ERROR HANDLER NODE
    Generates user-friendly error messages
    """
    logger.info(f"❌ Handling error: {state.get('error')}")

    error = state.get("error", "An unknown error occurred")

    if "timeout" in error.lower():
        final_answer = ("The service is currently slow to respond."
                        " Please try again in a moment.")
    elif "parse" in error.lower():
        final_answer = ("I had trouble understanding your question. "
                        "Could you rephrase it?")
    elif state["node_stage"] == Node.API_DATA and not state["api_data"]:
        final_answer = (f"Error fetching data for '{state.get('country_name')}'. "
                        f"Please check the country name and try again.")
    else:
        final_answer = error

    return {
        "final_answer": final_answer,
        "messages": ["Error handled"]
    }

# Conditional edges
def should_continue_to_api(state: AgentState):
    """
    Decide if we should call the API or handle an error
    """
    logger.info("Checking if should continue to API...")

    if state.get("error"):
        return Node.HANDLE_ERROR
    
    if not state.get("country_name"):
        return Node.HANDLE_ERROR
    logger.info(f"Continuing to API call for country: {state.get('country_name')}")
    return Node.API_DATA

def should_continue_to_synthesis(state: AgentState):
    """
    Decide if we should synthesize an answer or handle an error
    """
    logger.info("Checking if should continue to synthesis...")
    if state.get("error"):
        return Node.HANDLE_ERROR
    
    if not state.get("api_data"):
        return Node.HANDLE_ERROR
    logger.info(f"Continuing to synthesis for country: {state.get('country_name')}")
    return Node.SYNTHESIS
