from random import randint
import pygame
import dbcm2.model.state as state
from dbcm2.dispatch import *


class ControlDispatch(Dispatch):

    def __init__(self, dispatcher):
        super(ControlDispatch, self).__init__()
        self.dispatcher = dispatcher
        self.events = set()

    def subscribe(self, events, subscriber):
        super(ControlDispatch, self).subscribe(events, subscriber)
        self.events.update(events)
        print self.events
        self.dispatcher.subscribe(self.events, self)

    def event_trigger(self, event):
        super(ControlDispatch, self).event_trigger(event)


class Controller(object):
    """
    A parent class for all controllers.
    """

    def __init__(self, dispatcher, model, events=(TICK,)):
        """
        dispatcher (Dispatch): Allows posting events to the Dispatch.
        model (GameEngine): a strong reference to the game Model.
        """

        try:
            self.dispatch = dispatcher.dispatcher
        except AttributeError:
            self.dispatch = dispatcher
        dispatcher.subscribe(events, self)
        self.model = model

    def event_trigger(self, event):
        """
        Receive event notifications. Default version returns true regardless.
        Subclass and modify.
        """
        return True

class PygameController(Controller):
    """
    Handles keyboard input.
    """

    def __init__(self, dispatcher, model):
        """
        dispatcher (Dispatch): Allows posting events to the Dispatch.
        model (GameEngine): a strong reference to the game Model.
        """

        super(PygameController, self).__init__(dispatcher, model,
                                               [TICK, INIT_SCREEN])
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
            self.handle_battle_start()
        elif current_state == state.BATTLE_ANIMATION:
            self.advance_animation()
        else:
            raise state.StateError(current_state)

    def handle_battle_menu(self):
        m = self.model.state_model
        for event in pygame.event.get():
            if not m.local_set:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        m.local_set = True
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

    def handle_battle_start(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.dispatch.event_trigger(StateChangeEvent())
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.model.state_model.winner:
                        self.dispatch.event_trigger(StateChangeEvent())
                    else:
                        self.dispatch.event_trigger(
                            StateChangeEvent(state.BATTLE_MENU))

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

    def advance_animation(self):
        # Clear the event queue to prevent phantom commands.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE,
                                 pygame.K_ESCAPE,
                                 pygame.K_RETURN]:
                    self.model.state_model.step_animation()
            elif event.type == pygame.QUIT:
                self.dispatch.event_trigger(QuitEvent())

    def menu_accept(self):
        if self.model.state_model.selection == 0:
            self.dispatch.event_trigger(
                StateChangeEvent(state.BATTLE_RESOLUTION))
        elif self.model.state_model.selection == 1:
            # self.model.state.push(state.BREED_MENU)
            pass
        elif self.model.state_model.selection == 2:
            # self.model.state.push(state.OPTIONS)
            pass
        else:
            self.dispatch.event_trigger(QuitEvent())


class AutomatedController(Controller):
    """
    A controller to handle state based controls and automation.
    """

    def __init__(self, dispatcher, model):
        super(AutomatedController, self).__init__(dispatcher, model)
        self.clock = pygame.time.Clock()

    def event_trigger(self, event):

        if event.id == TICK:
            self.model.time = self.clock.tick()
            current_state = self.model.state.peek()
            m = self.model.state_model
            if current_state == state.BATTLE_MENU:
                if m.player.hp == 0:
                    m.winner = "Opponent"
                    self.dispatch.event_trigger(StateChangeEvent())
                elif m.opponent.hp == 0:
                    m.winner = "Player"
                    self.dispatch.event_trigger(StateChangeEvent())
                elif m.local_set and not m.remote_set:
                    if m.multiplayer:
                        pass
                    else:
                        m.selection_o = self.ai()
                        m.remote_set = True
                elif m.local_set and m.remote_set:
                    self.dispatch.event_trigger(
                        StateChangeEvent(
                            state.BATTLE_ANIMATION))
                else:
                    return
            elif current_state == state.BATTLE_ANIMATION:
                if self.model.state_model.animation_step > 5:
                    self.model.state_model.end_animation()
                    self.dispatch.event_trigger(StateChangeEvent())

    def ai(self):
        return randint(0, 2)