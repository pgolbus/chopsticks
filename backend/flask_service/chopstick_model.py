import logging
from typing import List, Optional

from . import Player

FINGERS = 5


EMPTY_HAND_ERROR_MSG = "Cannot move from / to an empty hand."
SWAP_ERROR_MSG = "Cannot swap all / more fingers than you have."

class ChopstickModel:

    players: Optional[List[Player]]

    def __init__(self):
        """
        Initialize the ChopstickModel with two players,
        each having one chopstick in each hand.
        """
        self.logger = logging.getLogger(__name__)
        self.init_game()

    def init_game(self) -> None:
        """
        Initialize the game.
        """
        self.players = [Player(1, 1), Player(1, 1)]
        self.current_player = 0
        self.winner = -1
        self.logger.info("Initialized ChopstickModel with two players.")

    def get_winner(self) -> int:
        """
        Retrieve the winner of the game.

        Returns:
            int: The index of the winner (0 or 1) or -1 if the game is not over.
        """
        return self.winner

    def set_winner(self, winner: int) -> None:
        """
        Set the winner of the game.

        Args:
            winner (int): The index of the winner (0 or 1).
        """
        self.winner = winner
        self.logger.info(f"Player {winner} has won the game.")

    def get_current_player(self) -> int:
        """
        Retrieve the current player.

        Returns:
            int: The index of the current player (0 or 1).
        """
        return self.current_player

    def change_player(self) -> None:
        """
        Change the current player to the other player.
        """
        self.current_player = (self.current_player + 1) % 2
        self.logger.info(f"Changed current player to {self.current_player}.")

    def get_player_hands(self, player: int) -> Player:
        """
        Retrieve the player based on the given identifier.

        Args:
            player (int): The index of the player in the array of players.

        Returns:
            Player: The player corresponding to the identifier.
        """
        self.logger.debug(f"Retrieving hands for player {player}.")
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
        self.logger.info(f"Player {player} moving from {hand_from} to {hand_to}.")
        from_player = self.players[player]
        to_player = self.players[(player + 1) % 2]

        if hand_from == "left":
            if from_player.left == 0:
                self.logger.error(EMPTY_HAND_ERROR_MSG)
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            add = from_player.left
        else:
            if from_player.right == 0:
                self.logger.error(EMPTY_HAND_ERROR_MSG)
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            add = from_player.right

        if hand_to == "left":
            if to_player.left == 0:
                self.logger.error(EMPTY_HAND_ERROR_MSG)
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            to_player.left += add
            to_player.left %= FINGERS
        else:
            if to_player.right == 0:
                self.logger.error(EMPTY_HAND_ERROR_MSG)
                raise ValueError(EMPTY_HAND_ERROR_MSG)
            to_player.right += add
            to_player.right %= FINGERS

        self.logger.debug(f"Move completed: Player {player} ({hand_from}) to Player {(player + 1) % 2} ({hand_to}).")

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
        self.logger.info(f"Player {player} swapping {fingers_to_swap} fingers from {starting_hand}.")
        if self.players[player].left == 0 or self.players[player].right == 0:
            self.logger.error(EMPTY_HAND_ERROR_MSG)
            raise ValueError(EMPTY_HAND_ERROR_MSG)
        if starting_hand == "left":
            if self.players[player].left < fingers_to_swap or \
               self.players[player].left - fingers_to_swap < 1:
                self.logger.error(SWAP_ERROR_MSG)
                raise ValueError(SWAP_ERROR_MSG)
            self.players[player].left -= fingers_to_swap
            self.players[player].right += fingers_to_swap
            self.players[player].right %= FINGERS
        else:
            if self.players[player].right < fingers_to_swap or \
               self.players[player].right - fingers_to_swap < 1:
                self.logger.error(SWAP_ERROR_MSG)
                raise ValueError(SWAP_ERROR_MSG)
            self.players[player].left += fingers_to_swap
            self.players[player].right -= fingers_to_swap
            self.players[player].left %= FINGERS

        self.logger.debug(f"Swap completed: Player {player} swapped {fingers_to_swap} fingers from {starting_hand}.")