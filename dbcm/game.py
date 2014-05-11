import model
import control

main_running = True
game_running = True


def main_loop():
    print("Welcome to DBCM.")
    print("This is a text version to test the mechanics.")
    while main_running:
        command = raw_input("> ")
        control.terminal.main_handler(command)


def game_loop():
    global game_running
    game_running = True
    print("The game has begun.")
    print("The commands are strike, grapple, block.")
    while game_running:
        command = raw_input("> ").lower()
        control.terminal.game_handler(command)


if __name__ == "__main__":
    main_loop()