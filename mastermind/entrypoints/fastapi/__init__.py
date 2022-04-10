import logging
import os
from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from mastermind.bootstrap import configure_inject
from mastermind.domain.actions.create_game import GameCreator
from mastermind.domain.actions.game_status import GameStatusManager
from mastermind.domain.actions.guess import GuessManager
from mastermind.domain.models.exceptions import InputException
from mastermind.entrypoints.fastapi.models import (
    GameStatusResponse,
    GuessRequest,
    GuessResponse,
    NewGameRequest,
    NewGameResponse,
)

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


@app.exception_handler(InputException)
async def color_not_supported_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST.value,
        content={
            "status": f"{HTTPStatus.BAD_REQUEST.name}",
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


@app.get(
    "/games/{game_id}/status",
    response_model=GameStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get status of the game",
)
async def game_status(game_id: int, api_key: APIKey = Depends(verify_api_key)):
    game_status = GameStatusManager()(game_id)
    return GameStatusResponse(
        **{
            "gameId": game_id,
            "isSolved": game_status.solved,
            "lastGuess": game_status.guess_code,
            "pegs": {"black": game_status.black_pegs, "white": game_status.white_pegs},
        }
    )


@app.post(
    "/games/{game_id}/guesses",
    response_model=GameStatusResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Make a guess and get black and white pegs",
)
async def guess(
    game_id: int, request: GuessRequest, api_key: APIKey = Depends(verify_api_key)
):
    game_status = GuessManager()(game_id, request.guess)
    return GameStatusResponse(
        **{
            "gameId": game_id,
            "isSolved": game_status.solved,
            "lastGuess": game_status.guess_code,
            "pegs": {"black": game_status.black_pegs, "white": game_status.white_pegs},
        }
    )


@app.get(
    "/games/{game_id}/guesses",
    response_model=List[GuessResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Make a guess and get black and white pegs",
)
async def get_guess(game_id: int, api_key: APIKey = Depends(verify_api_key)):
    guesses = GuessManager().get_guesses(game_id)
    return [
        GuessResponse(
            **{
                "guessId": g.id,
                "guessCode": g.code,
                "pegs": {"black": g.black_pegs, "white": g.white_pegs},
            }
        )
        for g in guesses
    ]
