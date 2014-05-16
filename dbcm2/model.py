import pygame
import state
from dispatch import *


class GameEngine(object):
    """
    Tracks game state.
    """

    def __init__(self, dispatch):
        self.dispatch = dispatch
        dispatch.subscribe([QUIT, STATE_CHANGE], self)
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = state.StateMachine()

    def event_trigger(self, event):
        """
        Called by Dispatch.

        event (Event) = The event Dispatch notified.

        Responds to STATE_CHANGE and QUIT events.
        """
        if event.id == STATE_CHANGE:
            if event.state:
                self.state.push(event.state)
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