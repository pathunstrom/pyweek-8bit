import time
import pygame
from dbcm2.model import state
import os
import dbcm2
from dispatch import *


class GraphicalView():
    """Draws the model state onto the screen."""

    def __init__(self, dispatch, model):
        """
        dispatch (Dispatch): Allows posting messages to the event queue.
        model (Engine): a strong reference to the game Model.

        Attributes:
        screen (pygame.Surface): the primary display.
        """

        self.dispatch = dispatch
        self.dispatch.subscribe([TICK, QUIT, INIT_GAME], self)
        self.model = model
        self.is_initialized = False
        self.display = None
        self.small_font = None
        self.ui_elements = []

    def event_trigger(self, event):
        if event.id == TICK:
            if self.is_initialized:
                self.update()  # Update the display.
        elif event.id == QUIT:
            self.stop()  # Shut down display.
        elif event.id == INIT_GAME:
            self.initialize()  # Start the display.

    def update(self):
        """
        Render the screen based on state.
        """
        current_state = self.model.state.peek()
        if current_state == state.MENU:
            self.render_menu()
        elif current_state == state.BATTLE_MENU:
            self.render_battle_menu()
        elif current_state == state.BATTLE_RESOLUTION:
            self.render_battle_resolution()
        else:
            raise state.StateError(current_state)

    def render_menu(self):
        self.display.fill((255, 255, 255))
        button = self.ui_elements[0]
        for index, option in enumerate(self.model.state_model.options):
            location = 280, index * 50
            text_location = 280 + 30, index*50 + 20
            source = pygame.Rect(0, 50, 120, 50)
            if index == self.model.state_model.selection:
                source.top = 0
            self.display.blit(button, location, source)
            message = self.small_font.render(option, True, (0, 0, 0))
            self.display.blit(message, text_location)
        pygame.display.update()

    def render_battle_resolution(self):
        self.display.fill((0, 0, 0))
        message = self.small_font.render(
            'The game is animating a battle.',
            True, (255, 255, 255))
        self.display.blit(message, (0, 0))
        message = self.small_font.render(
            'It will return to the battle menu shortly.',
            True, (255, 255, 255))
        self.display.blit(message, (0, 30))
        pygame.display.update()

    def render_battle_menu(self):
        self.display.fill((191, 163, 163))
        pygame.draw.rect(self.display, (242, 218, 218),
                         pygame.Rect(0, 250, 400, 150))

        # Draw menu
        pygame.draw.rect(self.display, (26, 64, 63),
                         pygame.Rect(0, 250, 400, 150), 2)
        button = self.ui_elements[0]
        stance = self.model.state_model.player.stance
        for index, option in self.model.state_model.player.moves[stance]:
            location = 280, 250 + 50*index
            text_location = location[0] + 30, location[1] + 20
            source = pygame.Rect(0, 50, 120, 50)
            if index == self.model.state_model.selection:
                source.top = 0
            self.display.blit(button, location, source)
            message = self.small_font.render(option, True, (0, 0, 0))
            self.display.blit(message, text_location)


        # Draw battle zone
        # Draw Player Information
        hp_element = self.ui_elements[1]
        hp_max = self.model.state_model.player.max_hp
        hp_current = self.model.state_model.player.hp
        hp_percent = int(hp_current / float(hp_max) * 100)
        color = (0, 255, 0) if hp_percent > 50 else (255, 0, 0)
        pygame.draw.rect(self.display, color,
                         pygame.Rect(270, 183, hp_percent, 5))
        self.display.blit(hp_element, (170, 170))
        message = "{} / {}".format(hp_current, hp_max)
        render = self.small_font.render(message, True, (0, 0, 0))
        self.display.blit(render, (285, 193))

        # Draw the Enemy Information
        hp_element = pygame.transform.flip(hp_element, 1, 0)
        hp_max = self.model.state_model.opponent.max_hp
        hp_current = self.model.state_model.opponent.hp
        hp_percent = int(hp_current / float(hp_max) * 100)
        color = (0, 255, 0) if hp_percent > 50 else (255, 0, 0)
        pygame.draw.rect(self.display, color,
                         pygame.Rect(30, 23, hp_percent, 5))
        self.display.blit(hp_element, (10, 10))
        message = "{} / {}".format(hp_current, hp_max)
        render = self.small_font.render(message, True, (0, 0, 0))
        self.display.blit(render, (45, 33))

        pygame.display.update()

    def render_splash(self):
        self.display.fill((193, 153, 204))
        render = self.small_font.render(
            'Game By',
            True, (42, 102, 26))
        self.display.blit(render, (175, 180))
        render = self.small_font.render(
            'Patrick Thunstrom',
            True, (42, 102, 26))
        self.display.blit(render, (140, 200))
        pygame.display.update()

    def initialize(self):
        """
        Set up the pygame window and load graphical resources.
        """

        pygame.init()
        pygame.display.set_caption('demo game')
        self.display = pygame.display.set_mode(dbcm2.resolution)
        self.small_font = pygame.font.Font(None, 20)
        self.display.fill((193, 153, 204))
        render = self.small_font.render(
            'Game By',
            True, (42, 102, 26))
        self.display.blit(render, (175, 180))
        render = self.small_font.render(
            'Patrick Thunstrom',
            True, (42, 102, 26))
        self.display.blit(render, (140, 200))
        pygame.display.update()
        time.sleep(1)

        images = os.path.dirname(os.path.abspath(__file__))
        images = os.path.join(images, "resources", "ui")
        for image in os.listdir(images):
            uri = os.path.join(images, image)
            self.ui_elements.append(pygame.image.load(uri))
        for surface in self.ui_elements:
            surface.convert_alpha()

        self.is_initialized = True
        self.dispatch.event_trigger(ScreenInitializedEvent())

    def stop(self):
        self.is_initialized = False
        pygame.quit()