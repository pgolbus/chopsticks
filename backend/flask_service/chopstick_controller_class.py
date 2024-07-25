import logging

from flask import Blueprint, Response
from flask.views import MethodView

from .chopstick_model import ChopstickModel
from .chopstick_view import ChopstickView


bp = Blueprint('chopstick', __name__)


INVALID_HAND_ERROR_MSG = "Hand must be 'left' or 'right'"
INVALID_PLAYER_ERROR_MSG = "Player must be an integer, either 0 or 1."
WRONG_PLAYER_ERROR_MSG = "It is player {current_player}'s turn."

class ChopstickController(MethodView):
    """
    Controller for the Chopstick game, managing game state and player actions.
    """

    model: ChopstickModel
    view: ChopstickView
    current_player: int

    def __init__(self) -> None:
        """
        Initialize the ChopstickController with a model and view instance,
        and set the current player to 0.
        """
        self.logger = logging.getLogger(__name__)
        self.model = ChopstickModel()
        self.view = ChopstickView()
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
        player = self.model.get_player_hands(self.get_current_player(False))
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
            winner = self.get_current_player(False)
            self.logger.info(f"Player {winner} has won the game.")
            return winner
        self.logger.info("No player has won yet.")
        return -1

    #@bp.route("/get_current_player", methods=["GET"])
    def get_current_player(self, response=True) -> int:
        """
        Get the current player.

        Args:
            response (bool, optional): If True, get the current player from the view. Defaults to True.

        Returns:
            int: The current player (0 or 1), or
            Flask response object if response is True.
        """
        if response:
            return self.view.get_player(self.current_player)
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
        if player != self.get_current_player(False):
            display_player = self.get_current_player(False) + 1
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

    #@bp.route("/move/<player>/<from_hand>/<to_hand>", methods=["GET"])
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
        try:
            self.logger.info(f"Player {player} is attempting to move from {from_hand} to {to_hand}.")
            self.validate_player(player)
            self.validate_hand(from_hand)
            self.validate_hand(to_hand)
            self.model.move(self.get_current_player(False), from_hand, to_hand)
            self.logger.info(f"Move completed")
            return self.end_move()
        except ValueError as e:
            self.logger.error(e)
            self.view.error(str(e))

    #@bp.route("/swap/<player>/<hand>/<fingers>", methods=["GET"])
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
        try:
            self.logger.info(f"Player {player} is attempting to swap {fingers} fingers from {hand}.")
            self.validate_player(player)
            self.validate_hand(hand)
            self.model.swap(player, hand, fingers)
            self.logger.info(f"Swap completed for player {player}.")
            return self.end_move()
        except ValueError as e:
            self.logger.error(e)
            self.view.error(str(e))

    def end_move(self) -> Response:
        """
        Get the result of the last move and display it using the view.

        Returns:
            flask.Response: The response object containing the move result.
        """
        self.change_player()
        winner = self.get_winner()
        player1 = self.model.get_player_hands(0)
        player2 = self.model.get_player_hands(1)
        return self.view.move_result(player1, player2, winner)


# Register the view functions
controller_view = ChopstickController.as_view('chopstick_controller')
bp.add_url_rule("/get_current_player", view_func=controller_view, methods=["GET"], endpoint="get_current_player")
bp.add_url_rule('/move/<player>/<from_hand>/<to_hand>', view_func=controller_view, methods=['GET'])
bp.add_url_rule("/swap/<player>/<hand>/<fingers>", view_func=controller_view, methods=["GET"])