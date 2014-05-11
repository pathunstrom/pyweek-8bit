from dbcm import game


def main_handler(command):
    case = {'help': menu_help,
            'exit': quit_app,
            'new': new_game,}
    try:
        return case[command]()
    except KeyError:
        return bad_command()


def game_handler(command):
    case = {'help': game_help,
            'quit': quit_game,
            'strike': strike,
            'grapple': grapple,
            'block': block,
            'exit': quit_app,}
    try:
        return case[command]()
    except KeyError:
        return bad_command()


def bad_command():
    print("Command not recognized.")


def menu_help():
    print("Commands:\n")
    print("  help:\tDisplay this help.")
    print("  exit:\tQuit program.")


def game_help():
    print("Commands:\n")
    print("  help:\tDisplay this help.")
    print("  quit:\tReturn to the main menu.")
    print("  exit:\tQuit program.")
    print("  strike:\tChoose to strike.")
    print("  grapple:\tChoose to grapple.")
    print("  block:\tChoose to block.")


def quit_game():
    game.game_running = False
    print("Main menu.")


def quit_app():
    exit(0)


def new_game():
    game.game_loop()


def strike():
    print("You strike!")


def grapple():
    print("You grapple!")


def block():
    print("You block!")