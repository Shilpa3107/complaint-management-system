from langgraph.graph import StateGraph, END
from app.agents.state import UnifiedCopilotState
from app.agents.nodes import (
    classify_intent_node,
    route_by_intent,
    extract_fields_node,
    validate_fields_node,
    route_after_validation,
    classify_severity_node,
    generate_clarification_node,
    duplicate_check_node,
    root_cause_node,
    edit_complaint_node,
    copilot_answer_node,
)


def build_unified_graph():
    graph = StateGraph(UnifiedCopilotState)

    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("extract", extract_fields_node)
    graph.add_node("validate", validate_fields_node)
    graph.add_node("classify_severity", classify_severity_node)
    graph.add_node("clarify", generate_clarification_node)
    graph.add_node("duplicate_check", duplicate_check_node)
    graph.add_node("root_cause", root_cause_node)
    graph.add_node("edit_complaint", edit_complaint_node)
    graph.add_node("answer_question", copilot_answer_node)

    graph.set_entry_point("classify_intent")

    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "extract": "extract",
            "edit_complaint": "edit_complaint",
            "answer_question": "answer_question",
        },
    )

    graph.add_edge("extract", "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {"classify_severity": "classify_severity", "clarify": "clarify"},
    )
    graph.add_edge("classify_severity", "duplicate_check")
    graph.add_edge("duplicate_check", "root_cause")
    graph.add_edge("root_cause", END)
    graph.add_edge("clarify", END)

    graph.add_edge("edit_complaint", END)
    graph.add_edge("answer_question", END)

    return graph.compile()


unified_copilot_graph = build_unified_graph()