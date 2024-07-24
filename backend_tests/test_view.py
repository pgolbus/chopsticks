import pytest
from flask import Flask
from backend import Player
from backend.chopstick_view import ChopstickView

# Set up Flask app for testing
app = Flask(__name__)

@pytest.fixture
def app_context():
    with app.app_context():
        yield

def test_board_state(app_context):
    chopstick_view = ChopstickView()
    player1 = Player(left=2, right=3)
    player2 = Player(left=1, right=4)
    winner = -1

    with app.test_request_context():
        response = chopstick_view.board_state(player1, player2, winner)
        assert response.status_code == 200
        assert response.get_json() == {
            "player1_left": 2,
            "player1_right": 3,
            "player2_left": 1,
            "player2_right": 4,
            "winner": -1
        }

def test_get_hand(app_context):
    chopstick_view = ChopstickView()
    player = Player(left=2, right=3)

    with app.test_request_context():
        response = chopstick_view.get_hand(player, "left")
        assert response.status_code == 200
        assert response.get_json() == {
            "hand": 2
        }

def test_error(app_context):
    chopstick_view = ChopstickView()
    error_msg = "doesn't really matter..."

    with app.test_request_context():
        response = chopstick_view.error(error_msg)
        assert response.status_code == 400
        assert response.get_json() == {
            "error": error_msg
        }
