from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import BaseModel

answer_router = APIRouter(prefix="/inference")


class AnswerRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@answer_router.post("/answer", response_model=AnswerResponse)
def handle_answer(request: AnswerRequest, request_meta: Request) -> AnswerResponse:
    qna_system = request_meta.app.state.system
    answer = qna_system.answer(request.question)

    return AnswerResponse(answer=answer)
