from langgraph.graph import StateGraph, END
from app.agents.state import CopilotState
from app.agents.nodes import copilot_answer_node


def build_copilot_graph():
    graph = StateGraph(CopilotState)
    graph.add_node("answer", copilot_answer_node)
    graph.set_entry_point("answer")
    graph.add_edge("answer", END)
    return graph.compile()


copilot_graph = build_copilot_graph()