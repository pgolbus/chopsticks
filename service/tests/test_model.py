import pytest

from chopsticks import Player
from chopsticks.chopstick_model import ChopstickModel, EMPTY_HAND_ERROR_MSG, SWAP_ERROR_MSG

@pytest.fixture
def mock_dao(mocker):
    mock_dao = mocker.MagicMock()
    mocker.patch('chopsticks.chopstick_model.get_dao', return_value=mock_dao)
    return mock_dao

def test_chopstick_model_init_game(mock_dao):
    # Instantiate the ChopstickModel with the mock DAO
    model = ChopstickModel(dao_id="mock")

    # Assert that init was called correctly on the DAO
    mock_dao.init.assert_called_once()

def test_get_winner():
    model = ChopstickModel()
    assert model.get_winner() == -1
    model.winner = 0
    assert model.get_winner() == 0
    model.winner = 1
    assert model.get_winner() == 1

def test_set_winner():
    model = ChopstickModel()
    model.set_winner(0)
    assert model.winner == 0
    model.set_winner(1)
    assert model.winner == 1

def test_get_current_player():
    model = ChopstickModel()
    assert model.get_current_player() == 0
    model.current_player = 1
    assert model.get_current_player() == 1

def test_change_player_player():
    model = ChopstickModel()
    assert model.current_player == 0
    model.change_player()
    assert model.current_player == 1
    model.change_player()
    assert model.current_player == 0

def test_get_player_hands(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.side_effect = [
        Player(1, 3),
        Player(1, 2),
    ]
    assert model.get_player_hands(0) == Player(1, 3)
    assert model.get_player_hands(1) == Player(1, 2)

def test_move(mock_dao):
    model = ChopstickModel()

    mock_dao.get_player.side_effect = [
        Player(1, 3),
        Player(1, 2),
        Player(2, 3),
        Player(4, 1),
    ]

    model.move(0, "left", "left")
    mock_dao.set_player_hand.assert_called_with(1, "left", 2)

    mock_dao.reset_mock()

    model.move(1, "left", "right")
    mock_dao.set_player_hand.assert_called_with(0, "right", 3)

def test_mod_move(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.side_effect = [
        Player(4, 3),
        Player(2, 2),
        Player(2, 3),
        Player(3, 1),
    ]
    model.move(0, "left", "left")
    mock_dao.set_player_hand.assert_called_with(1, "left", 1)

    mock_dao.reset_mock()

    model.move(1, "left", "left")
    mock_dao.set_player_hand.assert_called_with(0, "left", 0)

def test_swap_move(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.side_effect = [
        Player(2, 2),
        Player(1, 4),
    ]
    model.swap(0, "left", 1)
    expected_calls = [
        (0, "left", 1),
        (0, "right", 3)
    ]
    actual_calls = [args for args, _ in mock_dao.set_player_hand.call_args_list]
    assert actual_calls == expected_calls

    mock_dao.reset_mock()

    model.swap(1, "right", 2)
    expected_calls = [
        (1, "right", 2),
        (1, "left", 3)
    ]
    actual_calls = [args for args, _ in mock_dao.set_player_hand.call_args_list]
    assert actual_calls == expected_calls

def test_swap_mod_move(mock_dao):
    model = ChopstickModel()

    mock_dao.get_player.side_effect = [
        Player(4, 3),
        Player(4, 4),
    ]

    model.swap(0, "left", 3)
    expected_calls = [
        (0, "left", 1),
        (0, "right", 1)
    ]
    actual_calls = [args for args, _ in mock_dao.set_player_hand.call_args_list]
    assert actual_calls == expected_calls

    mock_dao.reset_mock()


    model.swap(1, "right", 2)
    expected_calls = [
        (1, "right", 2),
        (1, "left", 1)
    ]
    actual_calls = [args for args, _ in mock_dao.set_player_hand.call_args_list]
    assert actual_calls == expected_calls


def test_move_from_zero(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.return_value = Player(0, 3)
    with pytest.raises(ValueError,
                       match=EMPTY_HAND_ERROR_MSG):
        model.move(0, "left", "left")

def test_move_to_zero(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.return_value = Player(0, 3)
    with pytest.raises(ValueError,
                       match=EMPTY_HAND_ERROR_MSG):
        model.move(1, "left", "left")

def test_swap_to_zero(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.return_value = Player(0, 3)
    with pytest.raises(ValueError,
                       match=EMPTY_HAND_ERROR_MSG):
        model.swap(0, "right", 1)

def test_swap_from_zero(mock_dao):
    model = ChopstickModel()
    mock_dao.get_player.return_value = Player(0, 3)
    with pytest.raises(ValueError,
                       match=EMPTY_HAND_ERROR_MSG):
        model.swap(0, "left", 1)

def test_swap_too_many():
    model = ChopstickModel()
    with pytest.raises(ValueError,
                       match=SWAP_ERROR_MSG):
        model.swap(0, "left", 1)
    with pytest.raises(ValueError,
                       match=SWAP_ERROR_MSG):
        model.swap(0, "left", 2)