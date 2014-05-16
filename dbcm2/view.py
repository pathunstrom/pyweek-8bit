import pygame
import dbcm2
import model
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

    def event_trigger(self, event):
        if event.id == TICK:
            self.update()  # Update the display.
        elif event.id == QUIT:
            self.stop()  # Shut down display.
        elif event.id == INIT_GAME:
            self.initialize()  # Start the display.

    def update(self):
        """
        Draw the screen based on state.
        """

        if self.is_initialized:
            self.display.fill((0, 0, 0))
            message = self.small_font.render(
                'View is drawing on your screen',
                True,
                (255, 255, 255))
            self.display.blit(message, (0, 0))
            pygame.display.update()

    def initialize(self):
        """
        Set up the pygame window and load graphical resources.
        """

        pygame.init()
        pygame.display.set_caption('demo game')
        self.display = pygame.display.set_mode(dbcm2.resolution)
        self.small_font = pygame.font.Font(None, 20)
        self.is_initialized = True
        self.dispatch.event_trigger(ScreenInitializedEvent())

    def stop(self):
        self.is_initialized = False
        pygame.quit()