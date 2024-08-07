import pytest

from backend import Player
from backend.chopstick_controller import ChopstickController
from backend.chopstick_controller import INVALID_PLAYER_ERROR_MSG, \
    WRONG_PLAYER_ERROR_MSG


@pytest.fixture
def mock_model(mocker):
    mock_model = mocker.patch("backend.chopstick_controller.ChopstickModel")
    return mock_model

@pytest.fixture
def mock_view(mocker):
    mock_view = mocker.patch("backend.chopstick_controller.ChopstickView")
    return mock_view

def test_change_player():
    chopstick_controller = ChopstickController()
    assert chopstick_controller.current_player == 0
    chopstick_controller.change_player()
    assert chopstick_controller.current_player == 1
    chopstick_controller.change_player()
    assert chopstick_controller.current_player == 0

def test_get_current_player(mock_view):
    chopstick_controller = ChopstickController()
    assert chopstick_controller.get_current_player(False) == 0
    chopstick_controller.change_player()
    assert chopstick_controller.get_current_player(False) == 1
    chopstick_controller.change_player()
    assert chopstick_controller.get_current_player(False) == 0
    chopstick_controller.get_current_player()
    mock_view.assert_has_calls(mock_view.call.get_player(0))

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

def test_valid_player():
    chopstick_controller = ChopstickController()
    chopstick_controller.validate_player("0")
    chopstick_controller.change_player()
    chopstick_controller.validate_player("1")

def test_move_wrong_player():
    chopstick_controller = ChopstickController()
    with pytest.raises(ValueError, match=WRONG_PLAYER_ERROR_MSG.format(current_player="1")):
        chopstick_controller.validate_player("1")
    chopstick_controller.change_player()
    with pytest.raises(ValueError, match=WRONG_PLAYER_ERROR_MSG.format(current_player="2")):
        chopstick_controller.validate_player("0")

def test_move_invalid_player():
    chopstick_controller = ChopstickController()
    with pytest.raises(ValueError, match=INVALID_PLAYER_ERROR_MSG):
        chopstick_controller.validate_player("one")
    with pytest.raises(ValueError, match=INVALID_PLAYER_ERROR_MSG):
        chopstick_controller.validate_player("3")

# def test_move(mock_model, mock_view):
#     chopstick_controller = ChopstickController()
#     chopstick_controller.move("0", "left", "left")
#     mock_model.assert_has_calls(mock_model.call.move(0, "left", "left"))
#     player1 = Player(1, 1)
#     player2 = Player(1, 1)
#     winner = 1
#     mock_view.assert_has_calls(mock_view.call.move_result(player1, player2, winner))
#     assert chopstick_controller.current_player == 1

# def test_swap(mock_model, mock_view):
#    chopstick_controller = ChopstickController()
#    chopstick_controller.swap("0", "left", "2")
#    mock_model.assert_has_calls(mock_model.call.swap(0, "left", 2))
