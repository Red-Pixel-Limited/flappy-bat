class Settings:
    def __init__(self, volume):
        self.volume = volume

    def sound_on(self) -> bool:
        return self.volume > 0

    def __str__(self):
        return f'Settings(volume={self.volume})'    


class Player:
    def __init__(self, username, scores, settings):
        self.username = username
        self.scores = scores
        self.settings = settings
    
    def __str__(self):
        return f'Player(username={self.username}, settings={self.settings})'
