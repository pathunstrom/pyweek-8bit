import pygame
import state
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
        self.active = False

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
        self.active = True

    def handle_input(self):
        """
        Handle allowed events.
        """

        current_state = self.model.state.peek()
        if current_state == state.PLAY:
            self.handle_play()
        elif current_state == state.MENU:
            self.handle_menu()
        elif current_state == state.HELP:
            self.handle_help()
        else:
            raise state.StateError(current_state)

    def handle_play(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(StateChangeEvent())
                elif event.key == pygame.K_F1:
                    self.dispatch.event_trigger(StateChangeEvent(state.HELP))
                else:
                    self.dispatch.event_trigger(
                        KeyEvent(event.key, event.unicode, DOWN))
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

    def handle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(StateChangeEvent())
                elif event.key == pygame.K_SPACE:
                    self.dispatch.event_trigger(StateChangeEvent(state.PLAY))
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

    def handle_help(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE,
                                 pygame.K_SPACE,
                                 pygame.K_RETURN]:
                    self.dispatch.event_trigger(StateChangeEvent())
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

