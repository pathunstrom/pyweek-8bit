import pygame
import dbcm2.model.state as state
from dbcm2.dispatch import *


class Controller(Dispatch):

    def __init__(self, dispatcher):
        super(Controller, self).__init__()
        self.dispatcher = dispatcher
        self.events = set()

    def subscribe(self, events, subscriber):
        super(Controller, self).subscribe(events, subscriber)
        self.events.update(events)
        print self.events
        self.dispatcher.subscribe(self.events, self)

    def event_trigger(self, event):
        super(Controller, self).event_trigger(event)


class PygameController(object):
    """
    Handles keyboard input.
    """

    def __init__(self, dispatcher, model):
        """
        dispatcher (Dispatch): Allows posting events to the Dispatch.
        model (GameEngine): a strong reference to the game Model.
        """

        self.dispatch = dispatcher.dispatcher
        dispatcher.subscribe([TICK, INIT_SCREEN], self)
        self.model = model
        self.active = False

    def event_trigger(self, event):
        """
        Receive event notifications.
        """

        if event.id == TICK:
            # Handle pygame event Queue and post messages to dispatch.
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
                if event.key == pygame.K_RETURN:
                    self.dispatch.event_trigger(
                        StateChangeEvent(state.BATTLE_RESOLUTION))
                elif event.key in [pygame.K_UP, pygame.K_LEFT]:
                    self.model.state_model.up()
                elif event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    self.model.state_model.down()
                elif event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(StateChangeEvent())
                else:
                    self.dispatch.event_trigger(
                        KeyEvent(event.key, event.unicode, pygame.KEYDOWN))
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

    def handle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(StateChangeEvent())
                elif event.key == pygame.K_RETURN:
                    self.menu_accept()
                elif event.key in (pygame.K_UP, pygame.K_LEFT):
                    self.model.state_model.up()
                elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
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
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

    def menu_accept(self):
        if self.model.state_model.selection == 0:
            print("Controller: Enter Battle Menu.")
            self.dispatch.event_trigger(
                StateChangeEvent(state.BATTLE_MENU))
        elif self.model.state_model.selection == 1:
            # self.model.state.push(state.BREED_MENU)
            pass
        elif self.model.state_model.selection == 2:
            # self.model.state.push(state.OPTIONS)
            pass
        else:
            self.dispatch.event_trigger(QuitEvent())