BATTLE = 0
BREED = 1
OPTIONS = 2
QUIT = 3

class MainMenu(object):
    """
    Tracks current state of the menu.
    """
    def __init__(self):
        self.options = ["Battle", "Breed", "Options", "Quit"]
        self.selection = 0
        print("Main menu loaded.")

    def up(self):
        if self.selection:
            self.selection += -1
        else:
            self.selection = len(self.options) - 1

    def down(self):
        if self.selection == len(self.options) - 1:
            self.selection = 0
        else:
            self.selection += 1

    def __repr__(self):
        return "MenuModel Current Option: " + self.options[self.selection]