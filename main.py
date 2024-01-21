from flappy_bird import FlappyBird
from db.repository import Repository
from player import *

player = None
repository = Repository(db_file_name='db/players.db')



def play_game():
    FlappyBird(player=player, repository=repository).display_menu()
