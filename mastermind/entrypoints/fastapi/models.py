from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class NewGameRequest(BaseModel):
    code_len: int = Field(alias="codeLength")


class NewGameResponse(BaseModel):
    game_id: int = Field(alias="gameId")
    supported_colors: str = Field(alias="supportedColors")
