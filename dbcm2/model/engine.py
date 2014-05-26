import pygame
from dbcm2.dispatch import *
import state
import menu
import battle


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
        self.state_model = menu.MainMenu()
        self.time = 0

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
            self.change_state_model(self.state.peek())
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
            self.dispatch.event_trigger(TickEvent())

    def change_state_model(self, new_state):
        if new_state == state.MENU:
            if not type(self.state_model) == menu.MainMenu:
                self.state_model = menu.MainMenu()
        elif new_state == state.BATTLE_RESOLUTION:
            if not type(self.state_model) == battle.BattleModel:
                self.state_model = battle.BattleModel()