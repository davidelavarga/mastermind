import os
from functools import lru_cache
from pathlib import Path

import yaml


class ConfigLoader:
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or os.getenv("CONFIG_PATH")
        if self.config_path is None:
            raise ValueError(
                "config_path is None or CONFIG_PATH env variable is undefined"
            )

    def __load_config(self):
        if not os.path.exists(self.config_path):
            raise OSError(f"{self.config_path} file not found")

        with open(self.config_path, "r") as ymlfile:
            cfg_file = yaml.safe_load(ymlfile)

        return cfg_file

    def as_dict(self):
        return self.__load_config()


@lru_cache()
def get_config(path: str = None) -> dict:
    return ConfigLoader(path).as_dict()
