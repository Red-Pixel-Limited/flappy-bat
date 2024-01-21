from db.repository import *


def test():
    repo = Repository(db_file_name='db/players.db')
    
    # error = repo.register_user('test', 'password')
    # if error:
    #     print('Error while register new user: ' + error.name)
    #     return
    # print('User registered successfully')

    print('Validating user...')
    error = repo.validate_user('test', 'password')
    if error:
        print('Error validating user: ' + error.name)
        return
    print('User validated successfully')

    repo.update_settings(player=Player('test', 10, settings=Settings(volume=90)))
    player = repo.get_player('test')
    print(player)

test()