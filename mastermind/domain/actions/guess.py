import logging

import inject

from mastermind.domain.models.black_pegs import BlackPegs
from mastermind.domain.models.code import CodeBuilder
from mastermind.domain.models.exceptions import BadGuessLength, GameAlreadySolvedError
from mastermind.domain.models.status import GameStatus
from mastermind.domain.models.white_pegs import WhitePegs
from mastermind.domain.ports import DataStorage


class GuessManager:
    @inject.autoparams()
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage

    def __call__(self, game_id: str, guess_code: str):
        logging.info("Guessing ...")

        logging.debug(f"Checking if {game_id} is already solved...")
        self._check_solved_code(game_id)

        logging.debug(f"Getting {game_id} secret code from data storage...")
        secret_code = self.data_storage.get_secret_code(game_id)

        logging.debug(f"Checking {guess_code} length...")
        self._check_valid_guess_len(len(guess_code), len(secret_code))

        code = CodeBuilder(secret_code)()
        guess = CodeBuilder(guess_code)()

        logging.info(f"Counting black and white pegs for {game_id} game...")
        black_pegs = BlackPegs(code, guess).count()
        white_pegs = WhitePegs(code, guess).count()

        logging.debug(f"Storing {guess.raw} in data storage...")
        guess_id = self.data_storage.store_guess(
            game_id, guess.raw, black_pegs, white_pegs
        )
        logging.debug(f"Stored {guess.raw} in data storage with id {guess_id}...")

        is_solved = black_pegs == len(code.raw)
        if is_solved:
            self.data_storage.resolve_game(game_id)
            logging.info(
                f"Game {game_id} with secret code {code.raw} has been resolved!"
            )

        return GameStatus(
            solved=is_solved,
            black_pegs=black_pegs,
            white_pegs=white_pegs,
            guess_code=guess.raw,
        )

    def _check_solved_code(self, game_id: int):
        if self.data_storage.is_game_solved(game_id):
            raise GameAlreadySolvedError(f"Game {game_id} is already solved")

    @staticmethod
    def _check_valid_guess_len(guess_len: int, code_len: int):
        if guess_len != code_len:
            raise BadGuessLength(
                f"Guess code length ({guess_len}) should be {code_len}"
            )
