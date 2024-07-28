import logging
from typing import Any, List

from chopsticks import Player
from chopsticks.dao import AbstractDAO


class PassthroughDAO(AbstractDAO):

    def __init__(self, *args: Any, **kwargs: Any):
        self.logger = logging.getLogger(__name__)
        self.players: List[Player] = []
        self.init()

    def init(self, *args: Any, **kwargs: Any):
        """Initialize the data store."""
        self.logger.debug("Initializing passthrough DAO")
        self.players = [Player(1, 1), Player(1, 1)]
        self.logger.debug("Passthrough DAO initialized with two players.")

    def get_player(self, player: int) -> Player:
        """Retrieve player hands based on player ID."""
        player_data = self.players[player]
        self.logger.debug(f"Retrieved hands for player {player}: {player_data}")
        return player_data

    def set_player_hand(self, player: int, hand: str, fingers: int) -> None:
        """Set player's hand

        Args:
            player (int): Player index (0 or 1)
            hand (str): Hand to set ("left" or "right")
            fingers (int): Number of fingers to set (0 to 4)
        """
        self.logger.debug(f"Setting {hand} hand of player {player} to {fingers}.")

        # Validate that the 'hand' parameter is either 'left' or 'right'
        if hand not in ['left', 'right']:
            self.logger.error("Invalid hand specified. Hand must be 'left' or 'right'.")
            raise ValueError("Hand must be 'left' or 'right'")

        # Set the appropriate hand using setattr
        setattr(self.players[player], hand, fingers)

        self.logger.debug(f"Player {player}'s {hand} hand: {getattr(self.players[player], hand)}")
