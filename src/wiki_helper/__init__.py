from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from wiki_helper.configuration import Configuration
from wiki_helper.logger import setup_logger
from wiki_helper.qna import build_system
from wiki_helper.transport.routers.answer import answer_router
from wiki_helper.transport.routers.delete import deletion_router
from wiki_helper.transport.routers.train import train_router


async def error_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error.", "error": str(exc)},
    )


def initialize_service(configuration: Configuration) -> FastAPI:
    service = FastAPI()

    service.state.configuration = configuration
    service.state.system = build_system(configuration)

    service.include_router(router=answer_router)
    service.include_router(router=train_router)
    service.include_router(router=deletion_router)

    service.add_middleware(
        CORSMiddleware,
        allow_origins=["https://en.wikipedia.org"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    service.add_exception_handler(Exception, error_handler)

    logger = setup_logger()

    logger.info("Service initialized successfully.")

    return service
