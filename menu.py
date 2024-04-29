

import pygame
from settings import *
from gui_helpers import draw_button, button_click_event


class GameMenu:
    def __init__(self, screen):
        """
        Inicializa el menú del juego.
        """
        self.screen = screen 
        self.font = pygame.font.Font(None, TITLE_FONT_SIZE)  

    
        self.start_button = pygame.Rect(300, 200, 200, 50) 
        self.exit_button = pygame.Rect(300, 300, 200, 50)  
    def draw(self):
        """
        Dibuja el menú del juego.
        """
        self.screen.fill(WHITE) 


        draw_button(
            self.screen,
            "Start Game",
            self.start_button,
            BLUE,
            GRAY,
            self.font,
        )
        draw_button(
            self.screen,
            "Exit",
            self.exit_button,
            RED,
            GRAY,
            self.font,
        )

        pygame.display.flip()  

    def handle_events(self):
        """
        Maneja los eventos del menú.
        """
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "exit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(pygame.mouse.get_pos()): 
                        return "start_game"

                    if self.exit_button.collidepoint(pygame.mouse.get_pos()):  
                        pygame.quit()
                        return "exit"

        return None  
