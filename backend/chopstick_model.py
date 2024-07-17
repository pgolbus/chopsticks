from typing import List, Optional
from . import Player

FINGERS = 5

EMPTY_HAND_ERROR_MSG = "Cannot move from / to an empty hand."

class ChopstickModel:

    players: Optional[List[Player]]

    def __init__(self):
        """
        Initialize the ChopstickModel with two players,
        each having one chopstick in each hand.
        """
        self.players = [Player(1, 1), Player(1, 1)]

    def get_player_hands(self, player: int) -> Player:
        """
        Retrieve the player based on the given identifier.

        Args:
            player (int): The index of the player in the array of players.

        Returns:
            Player: The player corresponding to the identifier.
        """
        return self.players[player]

    def move(self, player: int, hand_from: str, hand_to: str) -> None:
        """
        Perform a move by transferring chopsticks from one hand of the
        current player to one hand of the opponent.

        Args:
            player (int): The index of the current player (0 or 1).
            hand_from (str): The hand of the current player to transfer from.
                             Expected values are "left" or "right".
            hand_to (str): The hand of the opponent to transfer to.
                           Expected values are "left" or "right".

        Raises:
            ValueError: If the hand_from or hand_to is empty.
        """
        from_player = self.players[player]
        to_player = self.players[(player + 1) % 2]

        if hand_from == "left":
            if from_player.left == 0:
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            add = from_player.left
        else:
            if from_player.right == 0:
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            add = from_player.right

        if hand_to == "left":
            if to_player.left == 0:
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            to_player.left += add
            to_player.left %= FINGERS
        else:
            if to_player.right == 0:
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            to_player.right += add
            to_player.right %= FINGERS

    def swap(self, player: int, starting_hand: str, fingers_to_swap: int) -> None:
        """
        Swap the given number of fingers between the two hands of the given
        player.

        Args:
            player (int): The index of the current player (0 or 1).
            starting_hand (str): The hand to start with.
                                 Expected values are "left" or "right".
            fingers_to_swap (int): The number of fingers to swap (1 to 4).

        Raises:
            ValueError: If an empty hand is involved, or if fingers_to_swap is
                        not between 1 and 4, or if trying to swap more fingers
                        than available in the starting hand.
        """
        if self.players[player].left == 0 or self.players[player].right == 0:
            raise ValueError(EMPTY_HAND_ERROR_MSG)
        if fingers_to_swap < 1 or fingers_to_swap > 4:
            raise ValueError("Can only swap 1 to 4 fingers.")
        too_many_error_msg = "Cannot swap all / more fingers than you have."
        if starting_hand == "left":
            if self.players[player].left < fingers_to_swap or \
               self.players[player].left - fingers_to_swap < 1:
                raise ValueError(too_many_error_msg)
            self.players[player].left -= fingers_to_swap
            self.players[player].right += fingers_to_swap
            self.players[player].right %= FINGERS
        else:
            if self.players[player].right < fingers_to_swap or \
               self.players[player].right - fingers_to_swap < 1:
                raise ValueError(too_many_error_msg)
            self.players[player].left += fingers_to_swap
            self.players[player].right -= fingers_to_swap
            self.players[player].left %= FINGERS
