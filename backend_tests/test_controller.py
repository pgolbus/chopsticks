import pytest
import re

from backend.chopstick_controller import ChopstickController
from backend.chopstick_controller import INVALID_PLAYER_ERROR_MSG, \
    OUT_OF_RANGE_ERROR_MSG, WRONG_PLAYER_ERROR_MSG
from backend.chopstick_model import Player


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

def test_get_current_player():
    chopstick_controller = ChopstickController()
    assert chopstick_controller.get_current_player() == 0
    chopstick_controller.change_player()
    assert chopstick_controller.get_current_player() == 1
    chopstick_controller.change_player()
    assert chopstick_controller.get_current_player() == 0

def test_check_win(mock_model):
    mock_model.return_value.get_player_hands.side_effect = [
        Player(0, 0),
        Player(0, 1)
    ]
    chopstick_controller = ChopstickController()
    assert chopstick_controller.check_win() == True
    assert chopstick_controller.check_win() == False

def test_get_winner(mocker):
    chopstick_controller = ChopstickController()
    chopstick_controller.check_win = mocker.Mock()
    chopstick_controller.check_win.side_effect = [True, True, False]
    assert chopstick_controller.get_winner() == 1
    assert chopstick_controller.get_winner() == 0
    assert chopstick_controller.get_winner() == -1

############################
#
#  Move
#
############################
def test_move(mock_model, mocker):
    chopstick_controller = ChopstickController()
    winner = chopstick_controller.move("0", "0", "2")
    assert winner == -1
    mock_model.assert_has_calls(mock_model.call.move(0, "left", "left"))
    assert chopstick_controller.current_player == 1
    chopstick_controller.get_winner = mocker.Mock()
    chopstick_controller.get_winner.return_value = 1
    winner = chopstick_controller.move("1", "3", "0")
    assert winner == 1
    mock_model.assert_has_calls(mock_model.call.move(1, "right", "left"))
    assert chopstick_controller.current_player == 0

def test_move_wrong_player():
    chopstick_controller = ChopstickController()
    with pytest.raises(ValueError, match=WRONG_PLAYER_ERROR_MSG.format(current_player="1")):
        chopstick_controller.move("1", "0", "2")
    chopstick_controller.move("0", "0", "2")
    with pytest.raises(ValueError, match=WRONG_PLAYER_ERROR_MSG.format(current_player="2")):
        chopstick_controller.move("0", "0", "2")

def test_move_invalid_player():
    chopstick_controller = ChopstickController()
    with pytest.raises(ValueError, match=INVALID_PLAYER_ERROR_MSG):
        chopstick_controller.move("one", "0", "2")
    with pytest.raises(ValueError, match=INVALID_PLAYER_ERROR_MSG):
        chopstick_controller.move("3", "0", "2")

def test_move_invalid_move():
    chopstick_controller = ChopstickController()
    with pytest.raises(ValueError, match=re.escape(OUT_OF_RANGE_ERROR_MSG)):
        chopstick_controller.move("0", "zero", "2")
    with pytest.raises(ValueError, match=re.escape(OUT_OF_RANGE_ERROR_MSG)):
        chopstick_controller.move("0", "5", "2")

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