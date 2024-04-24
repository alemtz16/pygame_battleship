# menu.py

import pygame
from settings import *
from gui_helpers import draw_button, button_click_event

# Clase para el Menú del Juego
class GameMenu:
    def __init__(self, screen):
        """
        Inicializa el menú del juego.
        """
        self.screen = screen  # Pantalla de Pygame
        self.font = pygame.font.Font(None, TITLE_FONT_SIZE)  # Fuente para el menú

        # Botones del Menú
        self.start_button = pygame.Rect(300, 200, 200, 50)  # Botón para iniciar el juego
        self.exit_button = pygame.Rect(300, 300, 200, 50)  # Botón para salir del juego

    def draw(self):
        """
        Dibuja el menú del juego.
        """
        self.screen.fill(WHITE)  # Fondo blanco para el menú

        # Dibuja los botones del menú
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

        pygame.display.flip()  # Actualiza la pantalla

    def handle_events(self):
        """
        Maneja los eventos del menú.
        """
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "exit"

                if event.type == pygame.MOUSEBUTTONDOWN:  # Detecta clics
                    if self.start_button.collidepoint(pygame.mouse.get_pos()):  # Si el clic está en el botón
                        return "start_game"

                    if self.exit_button.collidepoint(pygame.mouse.get_pos()):  # Si el clic está en el botón de salida
                        pygame.quit()
                        return "exit"

        return None  # Sin cambios
