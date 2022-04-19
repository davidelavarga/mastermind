import inject
import pytest
from fastapi.testclient import TestClient

from mastermind.adapters.data_storage.sql import SQLStorage
from mastermind.domain.actions.create_game import GameCreator
from mastermind.domain.actions.game_status import GameStatusManager
from mastermind.domain.actions.guess import GuessManager
from mastermind.domain.actions.surrender import Surrender
from mastermind.domain.ports import DataStorage
from mastermind.entrypoints.fastapi import app

client = TestClient(app)


@pytest.fixture
def injector() -> inject.Injector:
    inject.clear_and_configure(lambda binder: binder.bind(DataStorage, SQLStorage()))
    yield inject
    inject.clear()


@pytest.fixture
def create_game(injector) -> GameCreator:
    return GameCreator()


@pytest.fixture
def status_manager(injector) -> GameStatusManager:
    return GameStatusManager()


@pytest.fixture
def guess_manager(injector) -> GuessManager:
    return GuessManager()


@pytest.fixture
def surrender_manager(injector) -> Surrender:
    return Surrender()


def test_create_game_happy_path(create_game):
    response = client.post(
        "/games", headers={"Authorization": "1234"}, json={"codeLength": 0}
    )
    assert response.status_code == 201


def test_game_status_happy_path(status_manager):
    response = client.get("/games/1/status", headers={"Authorization": "1234"})
    assert response.status_code == 200


def test_guess_happy_path(guess_manager):
    response = client.get("/games/1/guesses", headers={"Authorization": "1234"})
    assert response.status_code == 201


def test_surrender_happy_path(surrender_manager):
    response = client.post("/games/3/surrender", headers={"Authorization": "1234"})
    assert response.status_code == 200
