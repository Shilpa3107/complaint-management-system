from langgraph.graph import StateGraph, END
from app.agents.state import ComplaintState
from app.agents.nodes import (
    extract_fields_node,
    validate_fields_node,
    route_after_validation,
    classify_severity_node,
    generate_clarification_node,
)

def build_complaint_graph():
    graph = StateGraph(ComplaintState)

    graph.add_node("extract", extract_fields_node)
    graph.add_node("validate", validate_fields_node)
    graph.add_node("classify_severity", classify_severity_node)
    graph.add_node("clarify", generate_clarification_node)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "validate")

    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "classify_severity": "classify_severity",
            "clarify": "clarify",
        },
    )

    graph.add_edge("classify_severity", END)
    graph.add_edge("clarify", END)

    return graph.compile()


complaint_graph = build_complaint_graph()