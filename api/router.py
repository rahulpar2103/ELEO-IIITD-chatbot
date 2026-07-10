from fastapi import APIRouter

from api.schemas import ChatRequest, ChatResponse
from api.rate_limiter import check_rate_limit
from api.chat_service import invoke_graph

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    check_rate_limit(req.session_id)
    response = invoke_graph(req.message, req.session_id)
    return ChatResponse(response=response)
