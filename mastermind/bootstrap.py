import os
import sys

import inject

from mastermind.domain.ports import DataStorage


def dev_config(binder):
    from mastermind.adapters.data_storage.sql import SQLStorage

    binder.bind(DataStorage, SQLStorage())


def configure_inject():
    env = os.environ.get("ENV", "dev")
    config_name = f"{env.lower()}_config"
    this_module = sys.modules[__name__]
    config_fn = getattr(this_module, config_name)
    inject.configure_once(config_fn)
