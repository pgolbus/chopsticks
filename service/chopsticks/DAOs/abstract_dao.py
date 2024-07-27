# chopsticks/DAOs/abstract_dao.py
from abc import ABC, abstractmethod

class AbstractDAO(ABC):

    @abstractmethod
    def init(self, create: bool = False):
        """Initialize the data store."""
        pass

    @abstractmethod
    def get_player_hands(self, player: int):
        """Retrieve player hands based on player ID."""
        pass

    @abstractmethod
    def set_player_hands(self, player: int, left: int, right: int):
        """Set player hands based on player ID."""
        pass
