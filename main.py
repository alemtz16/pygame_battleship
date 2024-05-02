import pygame
import sys
from settings import *
from menu import GameMenu
from board import Board
from ship import Ship
from gui_helpers import handle_drag_and_drop, show_message
from fleet_config import FLEET  
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")


menu = GameMenu(screen)


player_board = Board(10)  
computer_board = Board(10) 
 
ships = []
for ship_key, data in FLEET.items():
    ship_name = data[0]
    image_path = data[1]
    start_position = data[2]
    orientation = data[3]
    size = data[4]

    new_ship = Ship(ship_name, size, orientation, start_position, image_path)
    ships.append(new_ship)


def adjust_start_position(ship, board_size, cell_size):
    """
    Adjusts the ship's position to ensure it's within the board and doesn't cause overlap.
    """
  
    if ship.orientation == 'horizontal':
        x = max(0, min(board_size * cell_size - ship.rect.width, ship.start_position[0]))
    else:
        x = max(0, min(board_size * cell_size - cell_size, ship.start_position[0]))

  
    if ship.orientation == 'vertical':
        y = max(0, min(board_size * cell_size - ship.rect.height, ship.start_position[1]))
    else:
        y = max(0, min(board_size * cell_size - cell_size, ship.start_position[1]))

  
    ship.start_position = (x, y)
    ship.rect.topleft = (x, y)

    
    def is_overlapping(ship, other_ships):
        ship_positions = set(ship.get_positions())
        for other_ship in other_ships:
            if ship == other_ship:
                continue 
            other_positions = set(other_ship.get_positions())
            if ship_positions & other_positions: 
                return True
        return False

    if is_overlapping(ship, placed_ships):
       
        x = max(0, min(board_size * cell_size - ship.rect.width, x))
        y = max(0, min(board_size * cell_size - ship.rect.height, y))
        ship.start_position = (x, y)
        ship.rect.topleft = (x, y)



placed_ships = []
for ship in ships:
    if not (0 <= ship.start_position[0] < ship.size and 0 <= ship.start_position[1] < ship.size):
        ship.start_position = (50, 70) 
 
    adjust_start_position(ship, GRID_SIZE, CELL_SIZE)
 
    if player_board.place_ship(ship):
        placed_ships.append(ship)
    
 
     



 

dragging_ship = None
in_menu = True 
game_running = False
game_started = False  
dragging = False
dragged_ship = None

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            logging.debug(f"Mouse Button Down at {event.pos}")
            for ship in ships:
                if ship.rect.collidepoint(event.pos):
                    dragging = True
                    dragged_ship = ship
                    ship.drag_offset_x = ship.rect.x - event.pos[0]
                    ship.drag_offset_y = ship.rect.y - event.pos[1]
                    logging.debug(f"Started dragging {ship.name} from {ship.rect.topleft}")
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging:
                logging.debug("Mouse Button Up")
                dragging = False
                dragged_ship = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and dragged_ship is not None:
                new_x = event.pos[0] + dragged_ship.drag_offset_x
                new_y = event.pos[1] + dragged_ship.drag_offset_y
                dragged_ship.rect.topleft = (new_x, new_y)
                logging.debug(f"Dragging {dragged_ship.name} to {dragged_ship.rect.topleft}")

    if in_menu:
        menu.draw()
        menu_event = menu.handle_events()
        if menu_event == "start_game":
            in_menu = False
            game_running = True
            game_started = True
        elif menu_event == "exit":
            running = False

    if game_started:
        screen.fill(WHITE)  # Clear screen before drawing
        player_board.draw(screen, CELL_SIZE, offset=(20, 50))
        computer_board.draw(screen, CELL_SIZE, offset=(450, 50))
        player_board.draw_ships_below_board(screen, ships, CELL_SIZE)
        font = pygame.font.Font(None, TEXT_FONT_SIZE)
        show_message(screen, "Player Board", font, BLACK, (150, 20))
        show_message(screen, "Computer Board", font, BLACK, (500, 20))
        game_started = False  # Reset game_started to prevent reinitializing the boards unnecessarily

    if game_running:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                cell_pos = ((mouse_pos[0] - 350) // CELL_SIZE, (mouse_pos[1] - 50) // CELL_SIZE)

    # Update display after all processing
    pygame.display.flip()
    logging.debug("Screen updated")

pygame.quit()