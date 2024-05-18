import logging
import pygame
from settings import *
from menu import GameMenu
from board import Board
from ship import Ship
from gui_helpers import draw_button, button_click_event
from fleet_config import FLEET

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")

menu = GameMenu(screen)
player_board = Board(10)
computer_board = Board(10, show_ships=False)  # Optionally show ships on the computer board

# Initialize ships
ships = []
for ship_info in FLEET.values():
    new_ship = Ship(
        name=ship_info['name'],
        size=ship_info['size'],
        orientation=ship_info['orientation'],
        start_position=(ship_info['position'][0], ship_info['position'][1]),
        image_path=ship_info['image_path']
    )
    player_board.add_ship(new_ship)  # Make sure ships are added to the board

game_state = 'MENU'  # Start with the menu
next_button = pygame.Rect(700, 550, 100, 50)  # Example position and size for 'Next' button

clock = pygame.time.Clock()  # Control the frame rate

# Main game loop
running = True
while running:
    clock.tick(60) 
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state == 'MENU':
            menu_action = menu.handle_events(events)  # Pass the events to the menu for processing
            if menu_action == 'start_game':
                game_state = 'SETUP'
                logging.debug("Transitioning to SETUP state.")
            elif menu_action == 'exit':
                pygame.quit()
                exit()

        elif game_state == 'SETUP':
            for ship in ships:
                ship.handle_mouse_event(event)  # Each ship handles its mouse events

    screen.fill(WHITE)
    if game_state == 'MENU':
        menu.draw()
    elif game_state == 'SETUP':
        player_board.draw(screen, CELL_SIZE, offset=(20, 50))  # Draw the player board
        
        if draw_button(screen, "Next", next_button, BLUE, RED, pygame.font.Font(None, 36)) and pygame.mouse.get_pressed()[0]:
            game_state = 'GAME'
            logging.debug("Transitioning to GAME state.")

    elif game_state == 'GAME':
        player_board.draw(screen, CELL_SIZE, offset=(20, 50))  # Draw the player board in game state
        computer_board.draw(screen, CELL_SIZE, offset=(450, 50))  # Draw the computer board in game state
        # Additional game logic here

    pygame.display.flip()
    clock.tick(60)  # Ensure the game runs at 60 FPS

pygame.quit()
