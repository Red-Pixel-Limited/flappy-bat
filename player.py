
class Sound:
    def __init__(self, volume, muted):
        self.volume = volume
        self.muted = muted
    
    def __str__(self):
        return f'Sound(volume={self.volume}, muted={self.muted})'


class Settings:
    def __init__(self, sound):
        self.sound = sound

    def __str__(self):
        return f'Settings(sound={self.sound})'    


class Player:
    def __init__(self, username, scores, settings):
        self.username = username
        self.scores = scores
        self.settings = settings
    
    def __str__(self):
        return f'Player(username={self.username}, settings={self.settings})'
