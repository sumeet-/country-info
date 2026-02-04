import logging

from langgraph.graph import StateGraph, END

from core.graph.enum import Node
from core.graph.nodes import (
    identify_intent, get_country_info, synthesize_final_answer, handle_error,
    should_continue_to_api, should_continue_to_synthesis
)
from core.graph.state import AgentState


logger = logging.getLogger(__name__)

class GraphSingleton:
    _instance = None
    _graph = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphSingleton, cls).__new__(cls)
        return cls._instance

    def get_graph(self) -> StateGraph:
        if self._graph is None:
            self._graph = build_graph()
        return self._graph


def safe_node(node_func, node_stage):
    """
    Decorator to wrap node functions in a try-except block.
    If an exception occurs, it updates the state with an error message
    and routes to the error handling node.
    """
    def wrapper(state: AgentState) -> dict:
        try:
            data = node_func(state)
            data.update(node_stage=node_stage)
            return data
        except Exception as e:
            return {
                "error": f"Error in {node_stage}: {str(e)}",
                "messages": [f"Error in {node_stage}: {str(e)}"],
                "node_stage": node_stage
            }
    return wrapper


def build_graph():
    logger.info("Building graph")
    builder = StateGraph(AgentState)
    
    builder.add_node(Node.INTENT, safe_node(identify_intent, Node.INTENT))
    builder.add_node(Node.API_DATA, safe_node(get_country_info, Node.API_DATA))
    builder.add_node(Node.SYNTHESIS, safe_node(synthesize_final_answer, Node.SYNTHESIS))
    builder.add_node(Node.HANDLE_ERROR, safe_node(handle_error, Node.HANDLE_ERROR))

    builder.set_entry_point(Node.INTENT)

    builder.add_conditional_edges(
        Node.INTENT,
        should_continue_to_api,
        {
            Node.API_DATA: Node.API_DATA,
            Node.HANDLE_ERROR: Node.HANDLE_ERROR
        }
    )
    builder.add_conditional_edges(
        Node.API_DATA,
        should_continue_to_synthesis,
        {
            Node.SYNTHESIS: Node.SYNTHESIS,
            Node.HANDLE_ERROR: Node.HANDLE_ERROR
        }
    )

    builder.add_edge(Node.SYNTHESIS, END)
    builder.add_edge(Node.HANDLE_ERROR, END)

    return builder.compile()


def run_graph(question: str) -> AgentState:
    logger.info(f"Running graph for {question}")
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
    result = GraphSingleton().get_graph().invoke(initial_state)

    return result["final_answer"]
