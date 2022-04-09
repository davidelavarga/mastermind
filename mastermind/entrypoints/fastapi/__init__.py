import logging
import os
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from mastermind.bootstrap import configure_inject
from mastermind.domain.actions.create_game import GameCreator
from mastermind.entrypoints.fastapi.models import NewGameRequest, NewGameResponse

app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))

# Security
__API_KEYS = os.getenv("API_KEYS", "").split(",")
auth_header = APIKeyHeader(name="Authorization")


async def verify_api_key(api_key_header: str = Security(auth_header)):
    if api_key_header not in __API_KEYS:
        logging.error(f"Bad API key: {api_key_header}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail=f"{HTTPStatus.UNAUTHORIZED.name}. Bad API key provided",
        )


@app.on_event("startup")
async def startup_event():
    configure_inject()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={
            "status": f"{HTTPStatus.INTERNAL_SERVER_ERROR.name}",
            "ErrorMessage": f"{exc}",
        },
    )


@app.post(
    "/games",
    response_model=NewGameResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initialize a new game and get the game id and supported colors",
)
async def create_game(
    request: NewGameRequest, api_key: APIKey = Depends(verify_api_key)
):
    game_id, supported_colors = GameCreator()(request.code_len)
    return NewGameResponse(**{"gameId": game_id, "supportedColors": supported_colors})
