import pygame
from gui_helpers import show_confirmation_popup
from settings import *
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def process_player_attack(attack_position, computer_board):
    x, y = attack_position
    cell = computer_board.grid[y][x]
    logging.debug(f"Processing attack at ({x}, {y}) - Cell content before attack: {cell}")
    if cell == 'S':
        logging.debug(f"Hit at {chr(y + 65)}{x + 1}!")
        computer_board.grid[y][x] = 'X'
    else:
        logging.debug(f"Miss at {chr(y + 65)}{x + 1}.")
        computer_board.grid[y][x] = 'O'
    logging.debug(f"Cell content after attack: {computer_board.grid[y][x]}")



def player_turn(events, screen, computer_board, cursor_x, cursor_y):
    cursor_active = True
    turn_over = False

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
                cell = computer_board.grid[cursor_y][cursor_x]
                logging.debug(f"Attacking {row_label}{col_label} - Cell content: {cell}")
                if not show_confirmation_popup(screen, row_label, col_label):
                    attack_position = None 
                else: 
                    logging.debug(f"Attack position confirmed: {row_label}{col_label}")
                    process_player_attack(attack_position, computer_board)
                    cursor_active = False
                    return True, cursor_x, cursor_y  # Attack confirmed, turn ends

    cursor_rect = pygame.Rect(520 + cursor_x * CELL_SIZE2, 100 + cursor_y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, cursor_rect, CELL_SIZE2)
    return False, cursor_x, cursor_y  # Turn continues

def show_popup(screen, message):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(200, 300, 200,300)
    pygame.draw.rect(screen, (200, 200, 200), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

    text_surface = font.render(message, True, (0, 0, 0))
    screen.blit(text_surface, (popup_rect.x + 10, popup_rect.y + 10))

    pygame.display.flip()
    pygame.time.wait(2000)