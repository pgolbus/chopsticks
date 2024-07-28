import pytest

from chopsticks.dao.passthrough_dao import PassthroughDAO
from chopsticks import Player


@pytest.fixture
def passthrough_dao():
    """Fixture to create a PassthroughADO instance."""
    return PassthroughDAO()

# Test initialization
def test_init_players(passthrough_dao):

    assert isinstance(passthrough_dao, PassthroughDAO), "PassthroughDAO is not an instance of PassthroughDAO"

# Test getting player hands
def test_get_player(passthrough_dao):
    assert passthrough_dao.get_player(0) == Player(1, 1)
    passthrough_dao.players[1].right = 3
    assert passthrough_dao.get_player(1) == Player(1, 3)

# Test setting player hands
def test_set_player(passthrough_dao):
    passthrough_dao.set_player_hand(0, "left", 2)
    assert passthrough_dao.players[0].left == 2
    passthrough_dao.set_player_hand(1, "right", 4)
    assert passthrough_dao.players[1].right == 4