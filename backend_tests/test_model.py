import pytest

from backend.chopstick_model import ChopstickModel, Player


# TODO: I should probably not re-write the error msg multiple times


def test_init_board():
    model = ChopstickModel()
    assert model.players[0].left == 1
    assert model.players[0].right == 1
    assert model.players[1].left == 1
    assert model.players[1].right == 1

def test_get_player_hands():
    model = ChopstickModel()
    model.players[0].left = 0
    model.players[0].right = 3
    model.players[1].left = 1
    model.players[1].right = 2
    assert model.get_player_hands(0) == Player(0, 3)
    assert model.get_player_hands(1) == Player(1, 2)

def test_move():
    model = ChopstickModel()
    model.move(0, "left", "left")
    assert model.players[1].left == 2
    model.move(1, "left", "right")
    assert model.players[0].right == 3

def test_mod_move():
    model = ChopstickModel()
    model.players[0].left = 4
    model.players[1].left = 2
    model.move(0, "left", "left")
    assert model.players[1].left == 1
    model.move(1, "left", "left")
    assert model.players[0].left == 0

def test_swap_move():
    model = ChopstickModel()
    model.players[0].left = 2
    model.players[0].right = 2
    model.players[1].left = 1
    model.players[1].right = 4
    model.swap(0, "left", 1)
    assert model.players[0].left == 1
    assert model.players[0].right == 3
    model.swap(1, "right", 2)
    assert model.players[1].left == 3
    assert model.players[1].right == 2

def test_swap_mod_move():
    model = ChopstickModel()
    model.players[0].left = 4
    model.players[0].right = 3
    model.players[1].left = 4
    model.players[1].right = 4
    model.swap(0, "left", 3)
    assert model.players[0].left == 1
    assert model.players[0].right == 1
    model.swap(1, "right", 2)
    assert model.players[1].left == 1
    assert model.players[1].right == 2

def test_move_from_zero():
    model = ChopstickModel()
    model.players[0].left = 0
    with pytest.raises(ValueError,
                       match="Cannot move from / to an empty hand."):
        model.move(0, "left", "left")

def test_move_to_zero():
    model = ChopstickModel()
    model.players[0].left = 0
    with pytest.raises(ValueError,
                       match="Cannot move from / to an empty hand."):
        model.move(1, "left", "left")

def test_swap_to_zero():
    model = ChopstickModel()
    model.players[0].left = 0
    with pytest.raises(ValueError,
                       match="Cannot move from / to an empty hand."):
        model.swap(0, "right", 1)

def test_swap_from_zero():
    model = ChopstickModel()
    model.players[0].left = 0
    with pytest.raises(ValueError,
                       match="Cannot move from / to an empty hand."):
        model.swap(0, "left", 1)

def test_swap_too_many():
    model = ChopstickModel()
    with pytest.raises(ValueError,
                       match="Cannot swap all / more fingers than you have."):
        model.swap(0, "left", 1)
    with pytest.raises(ValueError,
                       match="Cannot swap all / more fingers than you have."):
        model.swap(0, "left", 2)