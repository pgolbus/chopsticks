from dataclasses import dataclass
from typing import List, Optional
from . import FINGERS, Player
from .chopstick_model import ChopstickModel

OUT_OF_RANGE_ERROR_MSG = "Value must be an integer from 0 to 3 (inclusive)."

@dataclass
class Hand:
    player: int
    hand: str

class ChopstickController:
    """
    Controller for the Chopstick game, managing game state and player actions.
    """

    hands: Optional[List[Hand]]
    model: Optional[ChopstickModel]
    current_player: Optional[int]

    def __init__(self) -> None:
        """
        Initialize the ChopstickController with default hands, a model instance,
        and set the current player to 0.
        """
        self.hands = [
            Hand(player=0, hand="left"),
            Hand(player=0, hand="right"),
            Hand(player=1, hand="left"),
            Hand(player=1, hand="right")
        ]
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

        Returns:
            bool: True if the current player has won, False otherwise.
        """
        player = self.model.get_player_hands(self.current_player)
        if player.left + player.right == 0:
            return True
        return False

    # @app.route('/get_move/<move1>/<move2>')
    def move(self, player: str, move1: str, move2: str) -> bool:
        """
        Execute a move in the game and check if the move results in a win.

        Args:
            player (str): The player making the move (should be "0" or "1").
            move1 (str): The first move (integer from 0 to 3 as a string).
            move2 (str): The second move (integer from 0 to 3 as a string).

        Returns:
            bool: True if the move results in a win, False otherwise.

        Raises:
            ValueError: If player is not an integer 0 or 1.
            ValueError: If it is not the current player's turn.
            ValueError: If move1 or move2 are not integers in the range 0 to 3.
        """
        try:
            player = int(player)
        except ValueError:
            raise ValueError("Player must be an integer 0 or 1.")
        if player != self.current_player:
            raise ValueError(f"It is player {self.current_player}'s turn.")
        try:
            move1 = int(move1)
            move2 = int(move2)
        except ValueError:
            raise ValueError(OUT_OF_RANGE_ERROR_MSG)
        if move1 not in range(4) or move2 not in range(4):
            raise ValueError(OUT_OF_RANGE_ERROR_MSG)
        move1_hand = self.hands[move1].hand
        move2_hand = self.hands[move2].hand
        self.model.move(self.current_player, move1_hand, move2_hand)
        self.change_player()
        return self.check_win()


    #@app.route('/swap/<player>/<hand>/<fingers>')
    def swap(self, player: int, hand: str, fingers: int) -> None:
        if player not in (0, 1) or hand not in ("left", "right") or \
           fingers not in range(1, 5):
            raise ValueError
        if self.current_player != player:
            raise ValueError
        self.model.swap(player, hand, fingers)
