from enum import StrEnum


class LiftKey(StrEnum):
    Space = 'Space'
    Up = 'Up Arrow'
    W = 'W'


class Settings:
    def __init__(self, volume, lift_key: LiftKey):
        self.volume = volume
        self.lift_key = lift_key

    def sound_on(self) -> bool:
        return self.volume > 0

    def __str__(self):
        return f'Settings(volume={self.volume}, lift_key={self.lift_key})'


class Player:
    def __init__(self, username, scores, settings):
        self.username = username
        self.scores = scores
        self.settings = settings

    def __str__(self):
        return f'Player(username={self.username}, settings={self.settings})'
