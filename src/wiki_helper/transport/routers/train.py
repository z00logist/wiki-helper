from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import BaseModel
from yarl import URL

from wiki_helper.qna.system import RagSystemError

train_router = APIRouter(prefix="/training")


class TrainRequest(BaseModel):
    url: str


class TrainResponse(BaseModel):
    result: bool


@train_router.post("/train", response_model=TrainResponse)
def handle_train(request: TrainRequest, request_meta: Request) -> TrainResponse:
    qna_system = request_meta.app.state.system
    try:
        qna_system.train(URL(request.url))
    except RagSystemError:
        return TrainResponse(result=False)

    return TrainResponse(result=True)
