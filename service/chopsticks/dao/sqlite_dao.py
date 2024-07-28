import logging
import sqlite3

from chopsticks.dao.abstract_dao import AbstractDAO
from chopsticks import Player


class SQLiteDAO(AbstractDAO):
    """Data access object for managing player data in an SQLite database.

    Provides methods to initialize the database, retrieve player data, and update player data.

    Attributes:
        db_path (str): The file path to the SQLite database.
    """

    def __init__(self, sqlite_db_path: str = "chopsticks.db"):
        """Initialize the SQLiteDAO with the path to the SQLite database file.

        Args:
            db_path (str): Path to the database file. Defaults to 'chopsticks.db'.
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = sqlite_db_path
        self.logger.debug(f"SQLiteDAO initialized with database path: {sqlite_db_path}")

    def init(self):
        """Initializes the database by creating the players table and inserting initial player data."""
        self.logger.info("Initializing the database...")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS players')
            self.logger.debug("Dropped existing players table.")
            cursor.execute('''CREATE TABLE players (
                              player_id INTEGER PRIMARY KEY,
                              left_hand INTEGER,
                              right_hand INTEGER)''')
            self.logger.debug("Created new players table.")
            cursor.execute('''Insert into players (player_id, left_hand, right_hand) values
                            (0, 1, 1),
                            (1, 1, 1)''')
            self.logger.debug("Inserted initial player data.")
            conn.commit()
            self.logger.info("Database initialization complete.")

    def get_player(self, player: int) -> Player:
        """Retrieves a player's data from the database.

        Args:
            player (int): The player ID to retrieve data for.

        Returns:
            Player: A Player object with the retrieved hand data or None if not found.
        """
        self.logger.debug(f"Retrieving data for player {player}...")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT left_hand, right_hand FROM players WHERE player_id = ?', (player,))
            row = cursor.fetchone()
            if row:
                self.logger.debug(f"Data retrieved for player {player}: {row}")
                return Player(*row)
            else:
                self.logger.warning(f"No data found for player {player}.")
                return None

    def set_player_hand(self, player: int, hand: str, fingers: int):
        """Updates a player's hand data in the database.

        Args:
            player (int): The player ID.
            hand (str): Which hand to update ('left' or 'right').
            fingers (int): The number of fingers to set for the specified hand.

        Raises:
            ValueError: If the 'hand' parameter is not 'left' or 'right'.
        """
        self.logger.debug(f"Updating {hand} hand of player {player} to {fingers} fingers.")
        if hand not in ['left', 'right']:
            self.logger.error("Invalid hand specified. Hand must be 'left' or 'right'.")
            raise ValueError("Hand must be 'left' or 'right'")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE players SET {hand}_hand = ? WHERE player_id = ?', (fingers, player))
            conn.commit()
            self.logger.info(f"Player {player}'s {hand} hand updated to {fingers} fingers.")
