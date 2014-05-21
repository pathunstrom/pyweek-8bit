# Event Type IDs
QUIT = 0
TICK = 1
INIT_GAME = 2
INIT_SCREEN = 3
KEY = 4
STATE_CHANGE = 5

class InitializeEvent(object):

    def __init__(self):
        self.id = INIT_GAME

    def __repr__(self):
        return "Event: InitializeEvent"


class KeyEvent(object):

    def __init__(self, key, name, direction):
        self.id = KEY
        self.key = key
        self.unicode = name
        self.direction = direction

    def __repr__(self):
        return "Event: KeyEvent, Key: {}, Direction: {}".format(
            self.unicode, self.direction)


class QuitEvent(object):

    def __init__(self):
        self.id = QUIT

    def __repr__(self):
        return "Event: QuitEvent"


class ScreenInitializedEvent(object):

    def __init__(self):
        self.id = INIT_SCREEN

    def __repr__(self):
        return "Event: ScreenInitializedEvent"


class StateChangeEvent(object):

    def __init__(self, state=None):
        self.id = STATE_CHANGE
        self.state = state

    def __repr__(self):
        state = self.state
        return "Event: StateChangeEvent, Push: {}".format(state)


class TickEvent(object):

    def __init__(self):
        self.id = TICK

    def __repr__(self):
        return "Event: TickEvent, Time: {}ms".format(self.time)


class Dispatch(object):
    """Dispatcher class."""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, events, subscriber):
        for event in events:
            try:
                if not subscriber in self._subscribers[event]:
                    self._subscribers[event].update([subscriber])
            except KeyError:
                self._subscribers[event] = set([subscriber])

    def event_trigger(self, event):
        if event.id in self._subscribers:
            for subscriber in self._subscribers[event.id]:
                if event.id != TICK:
                    print("{} notified of {}.".format(subscriber, event))
                subscriber.event_trigger(event)