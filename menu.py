import pygame
from settings import *
from gui_helpers import draw_button, button_click_event
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class GameMenu:
    def __init__(self, screen):
        """
        Initializes the game menu.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.start_button = pygame.Rect(300, 200, 200, 50)
        self.exit_button = pygame.Rect(300, 300, 200, 50)

    def draw(self):
        """
        Draws the game menu.
        """
        self.screen.fill(WHITE)

        if draw_button(self.screen, "Start Game", self.start_button, BLUE, GRAY, self.font):
            logging.debug("Hovering over Start button")
        if draw_button(self.screen, "Exit", self.exit_button, RED, GRAY, self.font):
            logging.debug("Hovering over Exit button")

        pygame.display.flip()

    def handle_events(self, events):
        """
        Handles menu events by processing a list of events passed from the main event loop.
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"

            # Enhanced mouse event handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    logging.debug("Start button clicked.")
                    return "start_game"
                if self.exit_button.collidepoint(event.pos):
                    logging.debug("Exit button clicked.")
                    pygame.quit()
                    return "exit"

        return None
