from core.graph.state import AgentState, IntentAnalysisResult
from langchain_core.messages import HumanMessage, SystemMessage
import json
from core.graph.agents import intent_analyzer_agent, final_answer_synthesis_agent
from services.rest_countries import fetch_country_data
from typing import Literal
from pprint import pprint
# Node to identify user intent


def identify_intent(state: AgentState) -> dict:
    """
    INTENT ANALYSIS NODE
    
    Uses LLM to extract:
    - Country name from the question
    - Specific fields of information requested by the user
    - Any other specific instructions or context
    """
    print("Identifying intent...")

    messages = [
        HumanMessage(content=state["user_question"])
    ]
    
    response = intent_analyzer_agent.invoke({
        "messages": messages
    })
    
    try:
        # Parse LLM response
        intent_data = response.get("structured_response", {})
        pprint(f"Intent analysis result: {intent_data}")
        return {
            "country_name": intent_data.get("country_name"),
            "fields_requested": intent_data.get("fields_requested", []),
            "extra_info": intent_data.get("extra_info", ""),
            "messages": [f"Intent analyzed: {intent_data}"]
        }
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse intent",
            "messages": ["Intent parsing error"]
        }
    
# Node to fetch data from REST Countries API
def get_api_data(state: AgentState) -> dict:
    """
    TOOL CALLING NODE
    Fetches data from REST Countries API based on identified country name.
    """
    try:
        country = state.get("country_name")

        if not country or not isinstance(country, str):
            return {"error": "No valid country name provided.", 
                    "messages": ["No valid country name provided."]}
        
        # Clean up country name for API
        country_clean = country.strip()
        print(f"Fetching data for country: '{country_clean}'")

        data = fetch_country_data(country_name=country_clean)

        if not data:
            raise ValueError(f"No data returned for country: {country_clean}")

        # pprint(f"Fetched data: {data}")
        return {
            "api_data": data,
            "messages": [f"Fetched data for {country_clean}"]
        }
    except Exception as e:
        # Optionally log the error and the country name for debugging
        print(f"API Error for country '{state.get('country_name')}': {str(e)}")
        return {
            "error": f"API Error: {str(e)}",
            "messages": [f"API Error: {str(e)}"]
        }

# Node to synthesize final answer
def synthesize_final_answer(state: AgentState) -> dict:
    """
    ANSWER SYNTHESIS NODE
    Uses LLM to create a natural language answer from the API data
    """
    print("Synthesizing final answer...")

    user_question = state["user_question"]
    api_data = state["api_data"]
    fields_requested = state["fields_requested"]
    extra_info = state.get("extra_info", "")

    user_prompt = f"""Question: {user_question}

        Fields requested: {', '.join(fields_requested)}
        Extra Information: {extra_info}

        Available data:
        {json.dumps(api_data, indent=2)}

        Please answer the question using this data.
    """
    messages = [
        HumanMessage(content=user_prompt)
    ]
    response = final_answer_synthesis_agent.invoke({
        "messages": messages
    })

    # pprint(f"Final answer response: {response.get("structured_response")}")
    return {
        "final_answer": response.get("structured_response", ""),
        "messages": ["Final answer synthesized."]
    }

# Node to handle errors
def handle_error(state: AgentState) -> dict:
    """
    ERROR HANDLER NODE
    Generates user-friendly error messages
    """
    print(f"❌ Handling error: {state.get('error')}")
    
    error = state.get("error", "An unknown error occurred")
    
    if "not found" in error.lower():
        final_answer = f"I couldn't find information about that country. Please check the spelling and try again."
    elif "timeout" in error.lower():
        final_answer = "The service is currently slow to respond. Please try again in a moment."
    elif "parse" in error.lower():
        final_answer = "I had trouble understanding your question. Could you rephrase it?"
    else:
        final_answer = f"I encountered an error: {error}. Please try again."
    
    return {
        "final_answer": final_answer,
        "messages": ["Error handled"]
    }

# Conditional edges
def should_continue_to_api(state: AgentState) -> Literal["api_data", "handle_error"]:
    """
    Decide if we should call the API or handle an error
    """
    if state.get("error"):
        return "handle_error"
    
    if not state.get("country_name"):
        return "handle_error"
    
    return "api_data"

def should_continue_to_synthesis(state: AgentState) -> Literal["synthesis", "handle_error"]:
    """
    Decide if we should synthesize an answer or handle an error
    """
    if state.get("error"):
        return "handle_error"
    
    if not state.get("api_data"):
        return "handle_error"
    
    return "synthesis"