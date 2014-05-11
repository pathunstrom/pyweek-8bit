from os.path import exists, expanduser, join
from os import mkdir as mkdir
import model, control

game_path = join(expanduser('~'), 'pyweek8bit')
print(game_path)
if not exists(game_path):
#   create default configuration file
    print("Game path does not exist.")
    print("Setting up game path.")
    try:
        mkdir(game_path)
    except OSError:
        print("Something when wrong")