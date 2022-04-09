from abc import ABC, abstractmethod


class DataStorage(ABC):
    @abstractmethod
    def initialize_game(self, code: str):
        """Store a new game code"""
        pass

    @abstractmethod
    def get_status(self):
        """Get the current status of the given game"""
        pass

    @abstractmethod
    def store_guess(self, guess: str):
        """Store the given guess for the given game"""
        pass

    @abstractmethod
    def is_game_solved(self, game_id: int):
        """True if given game solved, False otherwise"""
        pass

    @abstractmethod
    def resolve_game(self, game_id: int):
        """Resolve the game"""
        pass
