from pydantic import BaseModel, Field


class NewGameRequest(BaseModel):
    code_len: int = Field(alias="codeLength")


class NewGameResponse(BaseModel):
    game_id: int = Field(alias="gameId")
    supported_colors: str = Field(alias="supportedColors")


class Pegs(BaseModel):
    black: int
    white: int


class GameStatusResponse(BaseModel):
    game_id: int = Field(alias="gameId")
    is_solved: bool = Field(alias="isSolved")
    last_guess: str = Field(alias="lastGuess")
    pegs: Pegs


class GuessRequest(BaseModel):
    guess: str
