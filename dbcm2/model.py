import pygame
import state
from dispatch import *


class GameEngine(object):
    """
    Tracks game state.
    """

    def __init__(self, dispatch):
        self.dispatch = dispatch
        dispatch.subscribe([QUIT, STATE_CHANGE, TICK], self)
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = state.StateMachine()
        self.state_model = MenuModel()
        self.counter = 0

    def event_trigger(self, event):
        """
        Called by Dispatch.

        event (Event) = The event Dispatch notified.

        Responds to STATE_CHANGE and QUIT events.
        """
        if event.id == STATE_CHANGE:
            if event.state:
                self.change_state_model(self.state.push(event.state))
            else:
                if not self.state.pop():
                    self.dispatch.event_trigger(QuitEvent())
        elif event.id == QUIT:
            self.running = False

    def run(self):
        """
        The main game loop.

        Pump a tick event using the pygame.time.Clock() module to calculate
        time between ticks.
        """
        self.running = True
        self.dispatch.event_trigger(InitializeEvent())
        self.state.push(state.MENU)
        while self.running:
            self.dispatch.event_trigger(TickEvent(self.clock.tick()))

    def change_state_model(self, current_state):
        if current_state == state.MENU:
            self.state_model = MenuModel()


class MenuModel(object):
    """
    Tracks current state of the menu.
    """
    def __init__(self):
        self.options = ["Battle", "Breed", "Options", "Quit"]
        self.current = 0

    def up(self):
        if self.current:
            self.current += -1
        else:
            self.current = len(self.options) - 1

    def down(self):
        if self.current == len(self.options) - 1:
            self.current = 0
        else:
            self.current += 1

    def __repr__(self):
        return "MenuModel Current Option: " + self.options[self.current]