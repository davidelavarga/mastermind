import logging

import inject

from mastermind.domain.models.exceptions import GameAlreadySolvedError
from mastermind.domain.ports import DataStorage


class Surrender:
    @inject.autoparams()
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage

    def __call__(self, game_id: int):
        logging.info(f"Surrender for game {game_id} ...")

        logging.debug(f"Checking if {game_id} is already solved...")
        self._check_solved_code(game_id)

        self.data_storage.surrender(game_id)
        secret_code = self.data_storage.get_secret_code(game_id)

        logging.debug(f"Game {game_id} has been surrendered")
        return secret_code

    def _check_solved_code(self, game_id: int):
        if self.data_storage.is_game_solved(game_id):
            raise GameAlreadySolvedError(f"Game {game_id} is already solved")
