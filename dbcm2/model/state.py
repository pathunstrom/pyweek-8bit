MENU = 1
BATTLE_RESOLUTION = 11
BATTLE_MENU = 12
BATTLE_ANIMATION = 13
BREED_MENU = 21
OPTIONS = 91


class StateMachine(object):
    """
    Manages a stack based state machine.
    """

    def __init__(self):
        self.stack = []

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """

        try:
            return self.stack[-1]
        except IndexError:
            return None

    def pop(self):
        """
        Returns the current state and removes it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.stack.pop()
            self.time = 0
            return len(self.stack) > 0
        except IndexError:
            return None

    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the new state.
        """
        self.stack.append(state)
        return state


class StateError(Exception):
    """
    Error when a game module encounters a state it can't handle.
    """

    def __init__(self, state):
        self.state = state

    def __str__(self):
        return repr(self.state)