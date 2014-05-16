# Event Type IDs
QUIT = 0
TICK = 1
INIT_GAME = 2
INIT_SCREEN = 3
KEY = 4

# Direction IDs
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


class QuitEvent(object):

    def __init__(self):
        self.id = QUIT

    def __repr__(self):
        return "Game quit."


class TickEvent(object):

    def __init__(self, time=0):
        self.id = TICK
        self.time = time

    def __repr__(self):
        return "Tick: {}ms".format(self.time)


class InitializeEvent(object):

    def __init__(self):
        self.id = INIT_GAME

    def __repr__(self):
        return "Game Initialized."


class KeyEvent(object):

    def __init__(self, key, name, direction):
        self.id = KEY
        self.key = key
        self.unicode = name
        self.direction = direction

    def __repr__(self):
        direction = "released" if self.direction == UP else "pressed"
        return "{}-key was {}.".format(self.unicode, direction)


class ScreenInitializedEvent(object):

    def __init__(self):
        self.id = INIT_SCREEN

    def __repr__(self):
        return "Screen Initialized."


class Dispatch(object):
    """Dispatcher class."""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, events, subscriber):
        for event in events:
            try:
                if not subscriber in self._subscribers[event]:
                    self._subscribers[event].append(subscriber)
            except KeyError:
                self._subscribers[event] = [subscriber]

    def event_trigger(self, event):
        if event.id != TICK:
            print(event)

        if event.id in self._subscribers:
            for subscriber in self._subscribers[event.id]:
                subscriber.event_trigger(event)