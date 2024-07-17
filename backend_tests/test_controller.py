import pytest

from backend import Player
from backend.chopstick_controller import ChopstickController


@pytest.fixture
def mock_model(mocker):
    mock_model = mocker.patch("backend.chopstick_controller.ChopstickModel")
    return mock_model


def test_change_player():
    chopstick_controller = ChopstickController()
    assert chopstick_controller.current_player == 0
    chopstick_controller.change_player()
    assert chopstick_controller.current_player == 1
    chopstick_controller.change_player()
    assert chopstick_controller.current_player == 0

def test_check_winner(mock_model):
    mock_model.return_value.get_player_hands.side_effect = [
        Player(0, 0),
        Player(0, 1)
    ]
    chopstick_controller = ChopstickController()
    assert chopstick_controller.check_win() == True
    assert chopstick_controller.check_win() == False

############################
#
#  Move
#
############################
def test_move(mock_model):
    chopstick_controller = ChopstickController()
    chopstick_controller.move("0", "0", "2")
    mock_model.assert_has_calls(mock_model.call.move(0, "left", "left"))
    assert chopstick_controller.current_player == 1
    chopstick_controller.move("1", "3", "0")
    mock_model.assert_has_calls(mock_model.call.move(1, "right", "left"))
    assert chopstick_controller.current_player == 0

def test_move_wrong_player():
    assert True

def test_move_invalid_player():
    assert True

def test_move_out_of_bounds():
    assert True

def test_move_invalid_move():
    assert True

############################
#
#  Swap
#
############################
def test_swap(mock_model):
    # chopstick_controller = ChopstickController()
    # chopstick_controller.swap("0", "2")
    assert True

def test_swap_wrong_player():
    assert True

def test_swap_invalid_player():
    assert True

def test_swap_out_of_bounds():
    assert True

def test_swap_invalid_swap():
    assert True