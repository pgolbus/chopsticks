from dataclasses import dataclass
from typing import List, Optional

from . import FINGERS, Player
from .chopstick_model import ChopstickModel

@dataclass
class hand:
    player: int
    hand: str

class ChopstickController:

    hands = Optional[List[hand]]
    model = Optional[ChopstickModel]
    current_player = Optional[int]


    def __init__(self) -> None:
        self.hands = [
            hand(player=0, hand="left"),
            hand(player=0, hand="right"),
            hand(player=1, hand="left"),
            hand(player=1, hand="right")
        ]
        self.model = ChopstickModel()
        self.current_player = 0

    def change_player(self) -> None:
        self.current_player = (self.current_player + 1) % 2

