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
        self.start_button = pygame.Rect(300, 350, 200, 50)
        self.text_font = pygame.font.Font(None, 36)
        self.exit_button = pygame.Rect(300, 450, 200, 50)
        self.logo = pygame.image.load('assets/images/battleship.png')  # Make sure you have the logo image in the correct path
        self.logo = pygame.transform.scale(self.logo, (400, 100))

    def draw(self):
        """
        Draws the game menu.
        """
        self.screen.fill(WHITE)
        logo_rect = self.logo.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(self.logo, logo_rect)

        text_surface = self.text_font.render("Made by Alejandra and Ana Lucia", True, (249, 246, 238))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 280))
        self.screen.blit(text_surface, text_rect)

        
        if draw_button(self.screen, "Start Game", self.start_button, (0,0,0), GRAY, self.font):
            logging.debug("Hovering over Start button")
        if draw_button(self.screen, "Exit", self.exit_button,  (0,0,0), GRAY, self.font):
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