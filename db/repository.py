import os
import hashlib
import hmac
import sqlite3
from enum import Enum


class DbError(Enum):
    UserAlreadyExists = 1
    UserDoesNotExist = 2
    PasswordDoesNotMatch = 3


class Repository:
    def __init__(self, db_file_name='gamers.db'):
        self.db_file_name = db_file_name

    def register_user(self, username, password) -> DbError:
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            if cursor.execute('SELECT * FROM gamers WHERE username=?', (username,)).fetchone():
                return DbError.UserAlreadyExists
            salt = os.urandom(16)
            hashed_password = self.__hash_password(password, salt)
            cursor.execute('INSERT INTO gamers (username, password, salt) VALUES (?, ?, ?)',
                           (username, hashed_password, salt))
            conn.commit()
            return None
        finally:
            conn.close()

    def validate_user(self, username, password) -> DbError:
        conn = sqlite3.connect(self.db_file_name)
        try:
            cursor = conn.cursor()
            gamer = cursor.execute(
                'SELECT * FROM gamers WHERE username=?', (username,)).fetchone()
            if gamer is None:
                return DbError.UserDoesNotExist
            hashed_db_password = gamer[1]
            salt = gamer[2]
            if not hmac.compare_digest(hashed_db_password, self.__hash_password(password, salt)):
                return DbError.PasswordDoesNotMatch
            return None
        finally:
            conn.close()

    def __hash_password(self, password, salt) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
