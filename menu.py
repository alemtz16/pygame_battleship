import pygame
import sys
from settings import screen_width, screen_height, black, white
from board import Board  # Make sure to import the Board class

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.board = Board(screen)  # Initialize the game board
        self.current_state = "MENU"  # The initial state is set to MENU

    def run(self):
        if self.current_state == "MENU":
            self.display_menu()
        elif self.current_state == "GAME":
            self.board.draw()  # This would be the method to draw the game board

    def display_menu(self):
        title_font = pygame.font.Font(None, 74)
        option_font = pygame.font.Font(None, 50)

        title_text = title_font.render("Battleship Game", True, white)
        start_text = option_font.render("Start", True, white)
        settings_text = option_font.render("Settings", True, white)
        quit_text = option_font.render("Quit", True, white)

        title_rect = title_text.get_rect(center=(screen_width / 2, 100))
        start_rect = start_text.get_rect(center=(screen_width / 2, 250))
        settings_rect = settings_text.get_rect(center=(screen_width / 2, 300))
        quit_rect = quit_text.get_rect(center=(screen_width / 2, 350))

        menu_options = [start_rect, settings_rect, quit_rect]

        selected_option = 0

        while self.current_state == "MENU":
            self.screen.fill(black)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            self.current_state = "GAME"  # Change state to GAME
                        elif selected_option == 1:
                            # Placeholder for opening settings
                            pass
                        elif selected_option == 2:
                            pygame.quit()
                            sys.exit()

            # Drawing
            self.screen.blit(title_text, title_rect)
            self.screen.blit(start_text, start_rect)
            self.screen.blit(settings_text, settings_rect)
            self.screen.blit(quit_text, quit_rect)

            # Highlight the selected option
            pygame.draw.rect(self.screen, white, menu_options[selected_option], 2)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Battleship Game')
    menu = Menu(screen)
    
    # Main game loop
    while menu.running:
        menu.run()

    pygame.quit()
    sys.exit()
