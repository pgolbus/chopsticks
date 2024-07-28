from typing import Any
from abc import ABC, abstractmethod

from chopsticks import Player

class AbstractDAO(ABC):

    @abstractmethod
    def init(self, *args: Any, **kwargs: Any):
        """Initialize the data store."""
        raise NotImplementedError

    @abstractmethod
    def get_player(self, player: int) -> Player:
        """Retrieve player hands based on player ID."""
        raise NotImplementedError

    @abstractmethod
    def set_player_hand(self, player: int, hand: str, fingers: int) -> None:
        """Set player's hand

        Args:
            player (int): Player index (0 or 1)
            hand (str): Hand to set ("left" or "right")
            fingers (int): Number of fingers to set (0 to 4)
        """
        raise NotImplementedError
