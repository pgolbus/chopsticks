import pytest

from backend.chopstick_controller import ChopstickController


def test_change_player():
    chopstick_controller = ChopstickController()
    assert chopstick_controller.current_player == 0
    chopstick_controller.change_player()
    assert chopstick_controller.current_player == 1
    chopstick_controller.change_player()
    assert chopstick_controller.current_player == 0

def test_get_first_move():
    assert True

def test_get_second_move():
    assert True

def test_move():
    assert True

def test_swap():
    assert True

def test_raise_swap_out_of_bounds():
    assert True

def test_check_winner():
    assert True