import logging
import pygame
from settings import *
from menu import GameMenu
from board import Board
from ship import Ship
from gui_helpers import draw_button
from fleet_config import FLEET

 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")

menu = GameMenu(screen)
player_board = Board(10)
computer_board = Board(10, show_ships=False)   

 
ships = []
for ship_info in FLEET.values():
    new_ship = Ship(
        name=ship_info['name'],
        size=ship_info['size'],
        orientation=ship_info['orientation'],
        start_position=(ship_info['position'][0], ship_info['position'][1]),
        image_path=ship_info['image_path'],
        start_cell_position=(ship_info['position'][0], ship_info['position'][1]) 
    )
    player_board.add_ship(new_ship)
    ships.append(new_ship)

game_state = 'MENU'   
next_button = pygame.Rect(700, 550, 100, 50)   

clock = pygame.time.Clock()  

 
running = True
while running:
    clock.tick(60)   
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)  

    if game_state == 'MENU':
        menu_action = menu.handle_events(events)   
        if menu_action == 'start_game':
            game_state = 'SETUP'
            logging.debug("Transitioning to SETUP state.")
            for ship in ships:
                ship.update_image(CELL_SIZE2)
        elif menu_action == 'exit':
            running = False

    if game_state == 'MENU':
        menu.draw()
    elif game_state == 'SETUP':
        player_board.draw(screen, CELL_SIZE2, offset=(50, 100), title="Player Board")   
        for ship in player_board.ships:
            ship.draw(screen)
            for event in events:
                ship.handle_mouse_event(event, ships)
                if ship.selected:
                    ship.handle_keyboard_event(event)

        if draw_button(screen, "Next", next_button, BLUE, RED, pygame.font.Font(None, 36)) and pygame.mouse.get_pressed()[0]:
            if player_board.all_ships_within_bounds():
                game_state = 'GAME'
                logging.debug("Transitioning to GAME state.")
                for ship in ships:
                    ship.update_position(ship.start_cell_position, CELL_SIZE2)
                    ship.update_image(CELL_SIZE2)
                screen = pygame.display.set_mode((950, WINDOW_HEIGHT))
            else:
                logging.debug("Some ships are out of bounds.")

    elif game_state == 'GAME':
        player_board.draw(screen, CELL_SIZE2, offset=(50, 100),title="Player Board")   
        computer_board.draw(screen, CELL_SIZE2, offset=(520, 100),title="Computer Board")  
        occupied_positions = []
 
        for ship in player_board.ships:
            occupied_positions.extend(ship.get_occupied_positions())

        print("Posiciones ocupadas en el tablero:")
        for position in occupied_positions:
            print(position)
     

    pygame.display.flip()

pygame.quit()