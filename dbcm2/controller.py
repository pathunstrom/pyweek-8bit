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
            # Handle pygame event Queue and post messages to disaptch.
            self.handle_input(event)
        elif event.id == INIT_SCREEN:
            # Prepare pygame event queue.
            self.initialize()

    def initialize(self):
        """
        Limit SDL events to those we wish to handle.
        """

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.active = True

    def handle_input(self, event):
        """
        Handle allowed events.
        """

        current_state = self.model.state.peek()
        if current_state == state.BATTLE_MENU:
            self.handle_battle_menu()
        elif current_state == state.MENU:
            self.handle_menu()
        elif current_state == state.BATTLE_RESOLUTION:
            self.handle_skip()
        else:
            raise state.StateError(current_state)

    def handle_battle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(StateChangeEvent())
                elif event.key == pygame.K_RETURN:
                    self.dispatch.event_trigger(
                        StateChangeEvent(state.BATTLE_RESOLUTION))
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
                elif event.key == pygame.K_RETURN:
                    self.menu_accept()
                elif event.key == pygame.K_UP:
                    self.model.state_model.up()
                elif event.key == pygame.K_DOWN:
                    self.model.state_model.down()
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

    def handle_skip(self):
        # Clear the event queue to prevent phantom commands.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.KEYDOWN,
                                 pygame.K_ESCAPE,
                                 pygame.K_RETURN]:
                    self.dispatch.event_trigger(StateChangeEvent())

    def menu_accept(self):
        if self.model.state_model.current == 0:
            self.model.state.push(state.BATTLE_MENU)
        elif self.model.state_model.current == 1:
            # self.model.state.push(state.BREED_MENU)
            pass
        elif self.model.state_model.current == 2:
            # self.model.state.push(state.OPTIONS)
            pass
        else:
            self.dispatch.event_trigger(QuitEvent())