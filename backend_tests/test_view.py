from backend import Player

from backend.chopstick_view import ChopstickView


def test_move_result():
    chopstick_view = ChopstickView()
    player1 = Player(left=2, right=3)
    player2 = Player(left=1, right=4)
    winner = -1
    assert chopstick_view.move_result(player1, player2, winner) == {
        "player1_left": 2,
        "player1_right": 3,
        "player2_left": 1,
        "player2_right": 4,
        "winner": -1,
        "status": 200
    }

def test_get_player():
    chopstick_view = ChopstickView()
    player = 0
    assert chopstick_view.get_player(player) == {
        "player": 0,
        "status": 200
    }

def test_error():
    chopstick_view = ChopstickView()
    error_msg = "doesn't really matter..."
    assert chopstick_view.error(error_msg) == {
        "error": error_msg,
        "status": 400
    }