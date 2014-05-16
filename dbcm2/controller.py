import pygame
import model
from dispatch import *


class UserInput(object):
    """
    Handles keyboard input.
    """

    def __init__(self, dispatcher, model):
        """
        dispatcher (Dispatch): Allows posting events to the Dispatch.
        model (GameEngine): a strong reference to the game Model.
        """

        self.dispatch = dispatcher
        dispatcher.subscribe([TICK, INIT_SCREEN], self)
        self.model = model

    def event_trigger(self, event):
        """
        Receive event notifications.
        """

        if event.id == TICK:
            self.handle_input()  # Handle pygame event Queue and post messages to disaptch.
        elif event.id == INIT_SCREEN:
            self.initialize()  # Prepare pygame event queue.

    def initialize(self):
        """
        Limit SDL events to those we wish to handle.
        """

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    def handle_input(self):
        """
        Handle allowed events.
        """

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(QuitEvent())
                else:
                    self.dispatch.event_trigger(
                        KeyEvent(event.key, event.unicode, DOWN))
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())