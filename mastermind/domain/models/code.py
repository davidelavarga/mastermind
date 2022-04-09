import logging
import random
from dataclasses import dataclass
from typing import Dict, Set

from mastermind.domain.models.exceptions import ColorNotSupportedError
from mastermind.utils.config_loader import get_config


# TODO inherit from UserDict
@dataclass(frozen=True)
class Code:
    pegs: Dict[str, Set[int]]
    raw: str

    def __str__(self) -> str:
        return self.raw


class CodeBuilder:
    supported_colors = get_config()["supported_colors"]

    def __init__(self, code: str) -> None:
        self.code = code.upper()
        self._check_colors()

    def _check_colors(self):
        for c in self.code:
            if c not in self.supported_colors:
                raise ColorNotSupportedError(
                    f"{c} is not in supported colors ({self.supported_colors})"
                )

    def _find(self, code, ch):
        return {i for i, ltr in enumerate(code) if ltr == ch}

    def __call__(self) -> Code:
        pegs = {color: self._find(self.code, color) for color in self.code}
        return Code(pegs=pegs, raw=self.code)

    @classmethod
    def generate(cls, code_len: int) -> str:
        logging.debug("Generating new random code ...")
        return "".join(random.choices(cls.supported_colors, k=code_len))
