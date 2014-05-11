from os.path import exists, expanduser, join
from os import mkdir as mkdir
import model
import control
import ConfigParser
import game


game_path = join(expanduser('~'), 'pyweek8bit')
print(game_path)
config = ConfigParser.ConfigParser()
config_path = join(game_path, 'config.txt')

if not exists(game_path):
#   create default configuration file
    print("Game path does not exist.")
    print("Setting up game path.")
    try:
        mkdir(game_path)
    except OSError:
        print("Something when wrong")
    config.add_section("Display")
    config.set("Display", "type", "terminal")
    with open(config_path, 'wb') as config_file:
        config.write(config_file)

config.read(config_path)