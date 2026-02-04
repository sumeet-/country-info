from langgraph.graph import StateGraph, END
from core.graph.nodes import (
    identify_intent, get_country_info, synthesize_final_answer, handle_error,
    should_continue_to_api, should_continue_to_synthesis
)
from core.graph.state import AgentState

def build_graph():
    builder = StateGraph(AgentState)
    
    builder.add_node("intent", identify_intent)
    builder.add_node("api_data", get_country_info)
    builder.add_node("synthesis", synthesize_final_answer)
    builder.add_node("handle_error", handle_error)

    builder.set_entry_point("intent")

    builder.add_conditional_edges(
        "intent",
        should_continue_to_api,
        {
            "api_data": "api_data",
            "handle_error": "handle_error"
        }
    )
    builder.add_conditional_edges(
        "api_data",
        should_continue_to_synthesis,
        {
            "synthesis": "synthesis",
            "handle_error": "handle_error"
        }
    )

    builder.add_edge("synthesis", END)
    builder.add_edge("handle_error", END)

    return builder.compile()

graph = build_graph()


def run_graph(question: str) -> AgentState:
    initial_state = {
        "user_question": question,
        "country_name": "",
        "fields_requested": [],
        "extra_info": "",
        "api_data": {},
        "final_answer": "",
        "error": "",
        "messages": []
    }
    result = graph.invoke(initial_state)

    return result["final_answer"]
   