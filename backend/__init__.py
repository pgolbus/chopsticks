from dataclasses import dataclass


FINGERS = 5


@dataclass
class Player:
    left: int
    right: int