from db.repository import *


def test():
    repo = Repository(db_file_name='db/players.db')
    error = repo.register_user('test', 'password')
    if error:
        print('Error while register new user: ' + error.name)
        return
    print('User registered successfully')

    print('Validating user...')
    error = repo.validate_user('test', 'password')
    if error:
        print('Error validating user: ' + error.name)
        return
    print('User validated successfully')

    player = repo.get_top_20_players()
    print(player)

test()
