# chopsticks/DAOs/sqlite_dao.py
import sqlite3

from service.chopsticks.DAOs.abstract_dao import AbstractDAO
from service.chopsticks import Player


class SQLiteDAO(AbstractDAO):

    def __init__(self, db_path):
        self.db_path = db_path

    def init(self, create: bool = False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if create:
                cursor.execute('DROP TABLE IF EXISTS players')
            cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                              player_id INTEGER PRIMARY KEY,
                              left_hand INTEGER,
                              right_hand INTEGER)''')
            cursor.execute('''Insert into players (player_id, left_hand, right_hand) values
                            (0, 1, 1),
                            (1, 1, 1)''')
            conn.commit()

    def get_player_hands(self, player: int) -> Player:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT left_hand, right_hand FROM players WHERE player_id = ?', (player,))
            row = cursor.fetchone()
            if row:
                return Player(*row)
            return None

    def set_player_hands(self, player: int, left: int, right: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE players SET left_hand = ?, right_hand = ? WHERE player_id = ?', (left, right, player))
            conn.commit()
