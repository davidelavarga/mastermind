import logging

import inject

from mastermind.domain.models.code import CodeBuilder
from mastermind.domain.ports import DataStorage


class GameCreator:
    @inject.autoparams()
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage

    def __call__(self, code_len: int = 4):
        logging.info("Creating new game ...")

        secret_code = CodeBuilder.generate(code_len)
        game_id = self.data_storage.initialize_game(secret_code)

        logging.info(f"Game {game_id} has been generated")
        return game_id, CodeBuilder.supported_colors
