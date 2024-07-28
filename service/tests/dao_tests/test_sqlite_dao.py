import sqlite3
import pytest

from chopsticks.dao.sqlite_dao import SQLiteDAO
from chopsticks import Player


@pytest.fixture
def sqlite_dao():
    """Fixture to create a SQLiteDAO instance with a mocked database path."""
    return SQLiteDAO('dummy_path.db')

@pytest.fixture
def mocked_conn(mocker):
    """Fixture to mock sqlite3 connection and cursor."""
    # Mock the cursor
    mock_cursor = mocker.MagicMock()

    # Mock the connection and configure it to return the mock cursor
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Configure the connection to work as a context manager
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None

    # Mock sqlite3.connect to return the mock connection
    mocker.patch('sqlite3.connect', return_value=mock_conn)

    return mock_conn, mock_cursor

def normalize_sql(sql):
    """Helper function to normalize SQL statements for comparison."""
    return ' '.join(sql.strip().split())

def test_init_creates_tables(sqlite_dao, mocked_conn):

    _, cursor = mocked_conn
    sqlite_dao.init()

    # Ensure connect was called correctly
    sqlite3.connect.assert_called_once_with('dummy_path.db')

    # Check if cursor.execute was called correctly
    normalized_executed_sql_queries = [normalize_sql(call[0][0]) for call in cursor.execute.call_args_list]

    normalized_expected_sql_queries = [normalize_sql(sql) for sql in [
        '''DROP TABLE IF EXISTS players''',
        '''CREATE TABLE players (
                          player_id INTEGER PRIMARY KEY,
                          left_hand INTEGER,
                          right_hand INTEGER)''',
        '''Insert into players (player_id, left_hand, right_hand) values
                          (0, 1, 1),
                          (1, 1, 1)'''
    ]]

    # Check if the expected and executed SQL queries match in both content and order
    for expected, actual in zip(normalized_expected_sql_queries, normalized_executed_sql_queries):
        assert expected == actual, f"Expected SQL '{expected}' does not match executed SQL '{actual}'"

    # Ensure the number of executed queries matches the number of expected queries
    assert len(normalized_expected_sql_queries) == len(
        normalized_executed_sql_queries), "Number of executed queries does not match the number of expected queries."

def test_get_player(sqlite_dao, mocked_conn):
    # Extract the mocked cursor from the fixture
    _, cursor_mock = mocked_conn

    # Setting up the return value for fetchone to simulate database response
    cursor_mock.fetchone.return_value = (1, 1)

    # Call the method to retrieve player hands
    player = sqlite_dao.get_player(1)

    # Assert the Player object is correctly instantiated and its attributes are correctly set
    assert isinstance(player, Player), "The returned object is not an instance of Player"
    assert player.left == 1, "Player left hand count does not match expected value"
    assert player.right == 1, "Player right hand count does not match expected value"

    # Ensure the SQL query was executed correctly
    cursor_mock.execute.assert_called_once_with(
        'SELECT left_hand, right_hand FROM players WHERE player_id = ?', (1,))

def test_set_player_hands(sqlite_dao, mocked_conn):
    conn_mock, cursor_mock = mocked_conn

    # Call the method to set left hand for player 1
    sqlite_dao.set_player_hand(1, "left", 4)
    # Call the method to set right hand for player 0
    sqlite_dao.set_player_hand(0, "right", 2)

    # Check if the correct SQL update commands were executed in the correct order
    expected_calls = [
        (('UPDATE players SET left_hand = ? WHERE player_id = ?', (4, 1)),),
        (('UPDATE players SET right_hand = ? WHERE player_id = ?', (2, 0)),)
    ]

    # Retrieve the actual calls made to cursor.execute()
    actual_calls = cursor_mock.execute.call_args_list

    # Compare expected calls with actual calls
    assert actual_calls == expected_calls, "Database operations were not called in the expected order"

    # Ensure the transaction was committed to the database twice
    assert conn_mock.commit.call_count == 2, "Database commit was not called twice as expected"
