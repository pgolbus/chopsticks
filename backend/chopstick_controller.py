from dataclasses import dataclass
from typing import List, Optional

from .chopstick_model import ChopstickModel

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
        self.model = ChopstickModel()
        self.current_player = 0

    def change_player(self) -> None:
        """
        Change the current player to the next player.
        """
        self.current_player = (self.current_player + 1) % 2

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
        if player.left + player.right == 0:
            return True
        return False

    def get_winner(self) -> int:
        """
        Get the winner of the game.

        Returns:
            int: The winner (0 or 1) or -1 if no one has won
        """
        if self.check_win():
            self.change_player()
            return self.get_current_player()
        return -1

    # @app.route("/get_current_player")
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
            raise ValueError(INVALID_PLAYER_ERROR_MSG)
        if player not in (0, 1):
            raise ValueError(INVALID_PLAYER_ERROR_MSG)
        if player != self.get_current_player():
            display_player = self.get_current_player() + 1
            raise ValueError(WRONG_PLAYER_ERROR_MSG.format(
                current_player=display_player
            ))

    def validate_hand(self, hand: str) -> None:
        """
        Validate the hand.

        Args:
            hand (str): The hand to validate.

        Raises:
            ValueError: If hand is not "left" or "right".
        """
        if hand not in ("left", "right"):
            raise ValueError(INVALID_HAND_ERROR_MSG)

    # @app.route("/get_move/<move1>/<move2>")
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
        self.validate_player(player)
        if from_hand not in ("left", "right") or to_hand not in ("left", "right"):
            raise ValueError(INVALID_HAND_ERROR_MSG)
        self.model.move(self.get_current_player(), from_hand, to_hand)
        self.change_player()
        return self.get_winner()

    #@app.route("/swap/<player>/<hand>/<fingers>")
    def swap(self, player: str, hand: str, fingers: str) -> None:
        self.validate_player(player)
        self.validate_hand(hand)
        self.model.swap(player, hand, fingers)
        self.change_player()
