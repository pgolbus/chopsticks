import logging
from typing import Any, Dict

from . import Player


class ChopstickView:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def move_result(self, player1: Player, player2: Player, winner: int) -> Dict[str, int]:
        return {
            "player1_left": player1.left,
            "player1_right": player1.right,
            "player2_left": player2.left,
            "player2_right": player2.right,
            "winner": winner,
            "status": 200
        }

    def get_player(self, player: int) -> Dict[str, int]:
        return {
            "player": player,
            "status": 200
        }

    def error(self, message: str) -> Dict[str, Any]:
        return {
            "error": message,
            "status": 400
        }