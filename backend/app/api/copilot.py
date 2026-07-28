from fastapi import APIRouter
from app.agents.copilot_graph import copilot_graph
from app.schemas.complaint import CopilotRequest, CopilotResponse

router = APIRouter(prefix="/copilot", tags=["copilot"])


@router.post("/", response_model=CopilotResponse)
def ask_copilot(payload: CopilotRequest):
    result = copilot_graph.invoke({
        "user_message": payload.user_message,
        "complaint_context": payload.complaint_context,
        "chat_history": [turn.model_dump() for turn in payload.chat_history],
    })
    return CopilotResponse(response=result["response"])