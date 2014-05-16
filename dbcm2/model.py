import pygame
from dispatch import *


class GameEngine(object):
    """
    Tracks game state.
    """

    def __init__(self, dispatch):
        self.dispatch = dispatch
        dispatch.subscribe([QUIT], self)
        self.clock = pygame.time.Clock()
        self.running = False

    def event_trigger(self, event):
        """
        Called by Dispatch.
        """
        if event.id == QUIT:
            self.running = False

    def run(self):
        """
        The main game loop.

        Pump a tick event using the pygame.time.Clock() module to calculate
        time between ticks.
        """
        self.running = True
        self.dispatch.event_trigger(InitializeEvent())
        while self.running:
            self.dispatch.event_trigger(TickEvent(self.clock.tick()))