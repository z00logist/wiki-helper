from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import BaseModel

from wiki_helper.qna.system import RagSystemError


deletion_router = APIRouter(prefix="/deletion")


class DeleteResponse(BaseModel):
    result: bool


@deletion_router.post("/delete", response_model=DeleteResponse)
def handle_delete(request_meta: Request) -> DeleteResponse:
    qna_system = request_meta.app.state.system
    try:
        qna_system.delete()
    except RagSystemError:
        return DeleteResponse(result=False)

    return DeleteResponse(result=True)
