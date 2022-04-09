import logging

import inject

from mastermind.domain.ports import DataStorage


class GameStatusManager:
    @inject.autoparams()
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage

    def __call__(self, game_id: int):
        logging.info(f"Getting game {game_id} status ...")

        status = self.data_storage.get_status(game_id)

        logging.debug(f"Game {game_id} status: {status}")
        return status
