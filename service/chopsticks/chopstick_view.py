import logging

from flask import make_response, jsonify

from . import Player


class ChopstickView:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def board_state(self, player1: Player, player2: Player, winner: int = 1):
        """
        Create a response for the move result.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
            winner (int): The winner of the game.

        Returns:
            Response: A Flask response object containing the move result.
        """
        response_data = {
            "player1_left": player1.left,
            "player1_right": player1.right,
            "player2_left": player2.left,
            "player2_right": player2.right,
            "winner": winner
        }
        self.logger.info(f"Move result returned: {response_data}")
        return make_response(jsonify(response_data), 200)

    def get_player(self, player: int):
        """
        Create a response for getting the current player.

        Args:
            player (int): The current player.

        Returns:
            Response: A Flask response object containing the current player.
        """
        response_data = {
            "player": player
        }
        self.logger.info(f"Get player returned: {response_data}")
        return make_response(jsonify(response_data), 200)

    def get_hand(self, player: Player, hand: str):
        """
        Create a response for getting the value of a specific hand.

        Args:
            player (Player): The player.
            hand (str): The hand to get the value of.

        Returns:
            Response: A Flask response object containing the value of the hand.
        """
        response_data = {
            "hand": getattr(player, hand)
        }
        self.logger.info(f"Get hand returned: {response_data}")
        return make_response(jsonify(response_data), 200)

    def error(self, message: str):
        """
        Create an error response.

        Args:
            message (str): The error message.

        Returns:
            Response: A Flask response object containing the error message.
        """
        self.logger.error(message)
        response_data = {
            "error": message
        }
        self.logger.info(f"Error returned: {message}")
        return make_response(jsonify(response_data), 400)
