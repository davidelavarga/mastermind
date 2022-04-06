from abc import ABC, abstractmethod


class DataManager(ABC):
    @abstractmethod
    def initialize(self, code: str):
        """Store the game code"""
        pass

    @abstractmethod
    def get_status(self):
        """Get the current status of the game"""
        pass

    @abstractmethod
    def create_guess(self, guess: str):
        """Store the given guess for the current game"""
        pass
