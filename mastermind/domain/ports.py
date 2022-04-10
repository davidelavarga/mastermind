from abc import ABC, abstractmethod

from mastermind.domain.models.status import GameStatus


class DataStorage(ABC):
    @abstractmethod
    def initialize_game(self, code: str) -> int:
        """Store a new game code"""
        pass

    @abstractmethod
    def get_secret_code(self, game_id: int) -> str:
        """Get the secret code of the given game id"""
        pass

    @abstractmethod
    def get_status(self, game_id: int) -> GameStatus:
        """Get the current status of the given game"""
        pass

    @abstractmethod
    def store_guess(
        self, game_id: int, guess: str, black_pegs: int, white_pegs: int
    ) -> int:
        """Store the given guess for the given game"""
        pass

    @abstractmethod
    def is_game_solved(self, game_id: int) -> bool:
        """True if given game solved, False otherwise"""
        pass

    @abstractmethod
    def resolve_game(self, game_id: int):
        """Resolve the game"""
        pass

    @abstractmethod
    def surrender(self, game_id: int):
        """Set the game as finished and return the secret code"""
        pass
