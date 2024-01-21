import os
import hashlib
import hmac
import sqlite3
from enum import Enum
from player import *
from typing import Tuple


class DbError(Enum):
    UserAlreadyExists = 1
    UserDoesNotExist = 2
    PasswordDoesNotMatch = 3


class Repository:
    def __init__(self, db_file_name='players.db'):
        self.db_file_name = db_file_name

    def register_user(self, username, password) -> DbError:
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            if cursor.execute('SELECT * FROM players WHERE username=?', (username,)).fetchone():
                return DbError.UserAlreadyExists
            salt = os.urandom(16)
            hashed_password = self.__hash_password(password, salt)
            cursor.execute('INSERT INTO players (username, password, salt) VALUES (?, ?, ?)',
                           (username, hashed_password, salt))
            conn.commit()
            return None
        finally:
            conn.close()

    def validate_user(self, username, password) -> DbError:
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            player = cursor.execute(
                'SELECT * FROM players WHERE username=?', (username,)).fetchone()
            if player is None:
                return DbError.UserDoesNotExist
            hashed_db_password = player[1]
            salt = player[2]
            if not hmac.compare_digest(hashed_db_password, self.__hash_password(password, salt)):
                return DbError.PasswordDoesNotMatch
            return None
        finally:
            conn.close()

    def get_player(self, username) -> Player:
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            record = cursor.execute(
                'SELECT p.username, p.scores, s.volume FROM players p INNER JOIN settings s ON s.id = p.settings_id WHERE p.username=?', (username,)).fetchone()
            if record:
                username = record[0]
                scores = record[1]
                volume = record[2]
                return Player(username, scores, Settings(volume))
            return None
        finally:
            conn.close()

    def update_settings(self, player: Player):
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            id = cursor.execute(
                'SELECT settings_id FROM players WHERE username=?', (player.username,)).fetchone()[0]
            if id == 1:
                cursor.execute(
                    'INSERT INTO settings (volume) VALUES (?)', (player.settings.volume,))
                cursor.execute('UPDATE players SET settings_id=? WHERE username=?', (cursor.lastrowid, player.username))
            else:
                cursor.execute('UPDATE settings SET volume=? WHERE id=?', (player.settings.volume, id))
            conn.commit()
        finally:
            conn.close()

    def get_top_20_players(self) -> list[Tuple[str, int]]:
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            records = cursor.execute(
                'SELECT username, scores FROM players ORDER BY scores DESC LIMIT 20').fetchall()
            return list(map(lambda record: (record[0], record[1]), records))
        finally:
            conn.close()

    def __hash_password(self, password, salt) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
