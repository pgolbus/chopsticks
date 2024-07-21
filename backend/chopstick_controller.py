from dataclasses import dataclass
from typing import List, Optional
import logging

from .chopstick_model import ChopstickModel
# from .chopstick_view import ChopstickView

INVALID_HAND_ERROR_MSG = "Hand must be 'left' or 'right'"
INVALID_PLAYER_ERROR_MSG = "Player must be an integer, either 0 or 1."
WRONG_PLAYER_ERROR_MSG = "It is player {current_player}'s turn."

class ChopstickController:
    """
    Controller for the Chopstick game, managing game state and player actions.
    """

    model: Optional[ChopstickModel]
    current_player: Optional[int]

    def __init__(self) -> None:
        """
        Initialize the ChopstickController with a model instance,
        and set the current player to 0.
        """
        self.logger = logging.getLogger(__name__)
        self.model = ChopstickModel()
        self.current_player = 0
        self.logger.info("ChopstickController initialized with player 0 starting.")

    def change_player(self) -> None:
        """
        Change the current player to the next player.
        """
        self.current_player = (self.current_player + 1) % 2
        self.logger.info(f"Changed current player to {self.current_player}.")

    def check_win(self) -> bool:
        """
        Check if the current player has won the game.

        Check if the current player has won the game. Actually, after we move
        but before we check, we change players. That means we are actually
        checking if the current player has _lost_.

        Returns:
            bool: True if the current player has won, False otherwise.
        """
        player = self.model.get_player_hands(self.get_current_player())
        win = player.left + player.right == 0
        self.logger.info(f"Checked win condition for player {self.current_player}: {'win' if win else 'no win'}.")
        return win

    def get_winner(self) -> int:
        """
        Get the winner of the game.

        Returns:
            int: The winner (0 or 1) or -1 if no one has won.
        """
        if self.check_win():
            self.change_player()
            winner = self.get_current_player()
            self.logger.info(f"Player {winner} has won the game.")
            return winner
        self.logger.info("No player has won yet.")
        return -1

    def get_current_player(self) -> int:
        """
        Get the current player.

        Returns:
            int: The current player (0 or 1).
        """
        return self.current_player

    def validate_player(self, player: str) -> None:
        """
        Validate the player.

        Args:
            player (str): The player to validate.

        Raises:
            ValueError: If player is not an integer 0 or 1.
            ValueError: If it is not the current player's turn.
        """
        try:
            player = int(player)
        except ValueError:
            self.logger.error(INVALID_PLAYER_ERROR_MSG)
            raise ValueError(INVALID_PLAYER_ERROR_MSG)
        if player not in (0, 1):
            self.logger.error(INVALID_PLAYER_ERROR_MSG)
            raise ValueError(INVALID_PLAYER_ERROR_MSG)
        if player != self.get_current_player():
            display_player = self.get_current_player() + 1
            self.logger.error(WRONG_PLAYER_ERROR_MSG.format(current_player=display_player))
            raise ValueError(WRONG_PLAYER_ERROR_MSG.format(current_player=display_player))

    def validate_hand(self, hand: str) -> None:
        """
        Validate the hand.

        Args:
            hand (str): The hand to validate.

        Raises:
            ValueError: If hand is not "left" or "right".
        """
        if hand not in ("left", "right"):
            self.logger.error(INVALID_HAND_ERROR_MSG)
            raise ValueError(INVALID_HAND_ERROR_MSG)

    def move(self, player: str, from_hand: str, to_hand: str) -> int:
        """
        Execute a move in the game and check if the move results in a win.

        Args:
            player (str): The player making the move (should be "0" or "1").
            from_hand (str): The hand to move from (should be "left" or "right").
            to_hand (str): The hand to move to (should be "left" or "right").

        Returns:
            int: The winner (0 or 1) or -1 if no one has won.

        Raises:
            ValueError: If player is not "0" or "1".
            ValueError: If from_hand or to_hand are not "left" or "right".
        """
        self.logger.info(f"Player {player} is attempting to move from {from_hand} to {to_hand}.")
        self.validate_player(player)
        self.validate_hand(from_hand)
        self.validate_hand(to_hand)
        self.model.move(self.get_current_player(), from_hand, to_hand)
        self.change_player()
        winner = self.get_winner()
        self.logger.info(f"Move completed. Current winner: {winner if winner != -1 else 'none'}.")
        return winner

    def swap(self, player: str, hand: str, fingers: str) -> None:
        """
        Execute a swap of fingers between hands.

        Args:
            player (str): The player making the swap (should be "0" or "1").
            hand (str): The hand to swap from (should be "left" or "right").
            fingers (str): The number of fingers to swap (should be a string representing an integer).

        Raises:
            ValueError: If player is not "0" or "1".
            ValueError: If hand is not "left" or "right".
        """
        self.logger.info(f"Player {player} is attempting to swap {fingers} fingers from {hand}.")
        self.validate_player(player)
        self.validate_hand(hand)
        self.model.swap(player, hand, fingers)
        self.change_player()
        self.logger.info(f"Swap completed for player {player}.")
