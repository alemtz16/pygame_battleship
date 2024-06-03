import pygame
from ai_computer import AI, process_ai_attack
from gui_helpers import show_confirmation_popup, show_attack_result_popup, show_no_repetition
from settings import *
import logging
from ship import Ship
from fleet_config import FLEET
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

chosen_squares = set()
def is_ship_sunk(board, ship):
    logging.debug(f"Checking if ship {ship} is sunk.")
    x_start, y_start, size, orientation = ship
    for i in range(size):
        if orientation == 'horizontal':
            x, y = x_start + i, y_start
        else:
            x, y = x_start, y_start + i
        
        logging.debug(f"Checking position ({x}, {y}) with board state: {board.grid[y][x]}")
        if board.grid[y][x] != 'X':
            logging.debug(f"Ship {ship} is not sunk. Position ({x}, {y}) is not hit.")
            return False
    logging.debug(f"Ship {ship} is sunk.")
    return True


def show_ship_sunk_popup(screen, message, ship_positions, image_path, duration=2):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(300, 150, 400, 400)
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)

    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(popup_rect.x + popup_rect.width // 2, popup_rect.y + 50))
    screen.blit(text_surface, text_rect)

    flame_image = pygame.image.load('assets/images/explosion.png')   
    flame_image = pygame.transform.scale(flame_image, (300, 200))   
    flame_image_rect = flame_image.get_rect(center=(popup_rect.x + popup_rect.width // 2, popup_rect.y + 200))   
    screen.blit(flame_image, flame_image_rect)

    pygame.display.flip()
    pygame.time.wait(duration * 1000)


def process_player_attack(screen, attack_position, ai_player, computer_board):
    x, y = attack_position
    cell = ai_player.grid[y][x]

    red_image = pygame.image.load('assets/images/redtoken.png')
    red_image = pygame.transform.scale(red_image, (CELL_SIZE2, CELL_SIZE2))
    blue_image = pygame.image.load('assets/images/bluetoken.png')
    blue_image = pygame.transform.scale(blue_image, (CELL_SIZE2, CELL_SIZE2))     

    logging.debug(f"Processing attack at ({x}, {y}) - Cell content before attack: {cell}")
    with open("control_file.txt", "a") as file:
        if cell == 'S':
            logging.debug(f"Hit at {chr(y + 65)}{x + 1}!")
            ai_player.grid[y][x] = 'X'
            computer_board.grid[y][x] = 'X'
            file.write(f"Player miss at {chr(y + 65)}{x + 1}\n")
            show_attack_result_popup(screen, f"Player hit a boat at {chr(y + 65)}{x + 1}!", duration=2)
            tile_rect = pygame.Rect(520 + x * CELL_SIZE2, 100 + y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
            pygame.draw.rect(screen, BLACK, tile_rect)
            pygame.draw.rect(screen, BLACK, tile_rect, 1)

            for ship in ai_player.ships:
                logging.debug(f"Checking ship: {ship}")
                if isinstance(ship, tuple):
                    logging.debug(f"Ship {ship} is a tuple.")
                    if is_ship_sunk(ai_player, ship):
                        logging.debug(f"Player sunk the ship at {ship}!")
                        ship_positions = []
                        x_start, y_start, size, orientation = ship
                        for i in range(size):
                            if orientation == 'horizontal':
                                ship_positions.append((x_start + i, y_start))
                            else:
                                ship_positions.append((x_start, y_start + i))
                        
                        for fleet_ship in FLEET.values():
                            if fleet_ship['size'] == size:
                                ship_name = fleet_ship['name']
                                ship_image_path = fleet_ship['image_path']
                                break
                        
                        for position in ship_positions:
                            computer_board.grid[position[1]][position[0]] = 'SUNK'

                        computer_board.sunk_ships.append((ship_positions, ship_image_path, orientation))

                        for position in ship_positions:
                            x, y = position
                            tile_rect = pygame.Rect(520 + x * CELL_SIZE2, 100 + y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
                            screen.blit(red_image, tile_rect.topleft)



                            pygame.draw.rect(screen, BLACK, tile_rect, 1)
                            ship_image = pygame.image.load(ship_image_path)
                            if orientation == 'horizontal':
                                ship_image = pygame.transform.scale(ship_image, (CELL_SIZE2 * size, CELL_SIZE2))
                            else:
                                ship_image = pygame.transform.scale(ship_image, (CELL_SIZE2, CELL_SIZE2 * size))
                                ship_image = pygame.transform.rotate(ship_image, 90)
                        

                        show_ship_sunk_popup(screen, f"Player sunk the {ship_name}!", ship_positions, ship_image_path, duration=2)
                        file.write(f"Player sunk the {ship_name} at {chr(y + 65)}{x + 1}\n")
                        ai_player.ships.remove(ship)  
                        break   
                else:
                    logging.debug(f"{ship} is not a tuple.")
        else:
            logging.debug(f"Miss at {chr(y + 65)}{x + 1}.")
            ai_player.grid[y][x] = 'O'
            computer_board.grid[y][x] = 'O'
            file.write(f"Player miss at {chr(y + 65)}{x + 1}\n")
            show_attack_result_popup(screen, f"Player hit water at {chr(y + 65)}{x + 1}!", duration=2)
            tile_rect = pygame.Rect(520 + x * CELL_SIZE2, 100 + y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
            screen.blit(blue_image, tile_rect.topleft)

            
            pygame.draw.rect(screen, BLACK, tile_rect, 1)

    logging.debug(f"Cell content after attack: {computer_board.grid[y][x]}")


def player_turn(events, screen, ai_player, cursor_x, cursor_y, computer_board):
    cursor_active = True
    turn_over = False
    cursor_image = pygame.image.load('assets/images/cursor.png')
    cursor_image = pygame.transform.scale(cursor_image, (CELL_SIZE2, CELL_SIZE2))
    pygame.mouse.set_visible(False)
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and cursor_x > 0:
                cursor_x -= 1
            elif event.key == pygame.K_RIGHT and cursor_x < GRID_SIZE - 1:
                cursor_x += 1
            elif event.key == pygame.K_UP and cursor_y > 0:
                cursor_y -= 1
            elif event.key == pygame.K_DOWN and cursor_y < GRID_SIZE - 1:
                cursor_y += 1
            elif event.key == pygame.K_RETURN:
                attack_position = (cursor_x, cursor_y)
                row_label = chr(cursor_y + 65)
                col_label = str(cursor_x + 1)
                cell = ai_player.grid[cursor_y][cursor_x]
                logging.debug(f"Attacking {row_label}{col_label} - Cell content: {cell}")
                if attack_position in chosen_squares:
                    logging.debug(f"Position {row_label}{col_label} has already been chosen.")
                    show_no_repetition(screen, f"Position {row_label}{col_label} has already been chosen.\n Choose another.", duration=2)
                else:
                    # Show the cursor
                    pygame.mouse.set_visible(True)
                    if not show_confirmation_popup(screen, row_label, col_label):
                        attack_position = None 
                    else: 
                        logging.debug(f"Attack position confirmed: {row_label}{col_label}")
                        process_player_attack(screen, attack_position, ai_player, computer_board)
                        chosen_squares.add(attack_position)  
                        cursor_active = False
                        return True, cursor_x, cursor_y   
 
    cursor_rect = pygame.Rect(520 + cursor_x * CELL_SIZE2, 100 + cursor_y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
 
    screen.blit(cursor_image, cursor_rect.topleft)
    return False, cursor_x, cursor_y   

def show_popup(screen, message):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(200, 300, 200,300)
    pygame.draw.rect(screen, (200, 200, 200), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

    text_surface = font.render(message, True, (0, 0, 0))
    screen.blit(text_surface, (popup_rect.x + 10, popup_rect.y + 10))

    pygame.display.flip()
    pygame.time.wait(2000)