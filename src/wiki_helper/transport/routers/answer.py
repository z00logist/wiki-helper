from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


answer_router = APIRouter(prefix="/inference")


class AnswerRequest(BaseModel):
    question: str


@answer_router.post("/answer")
def handle_answer(request: AnswerRequest, request_meta: Request) -> StreamingResponse:
    qna_system = request_meta.app.state.system
    query = request.question

    return StreamingResponse(qna_system.answer(query), media_type="text/plain")
