import pygame
from gui_helpers import show_confirmation_popup
from settings import *


def process_player_attack(attack_position, computer_board):
    x, y = attack_position
 
    cell = computer_board.grid[y][x]
    if cell:
        print(f"Hit at {chr(y + 65)}{x + 1}!")
        computer_board.grid[y][x] = 'X'   
    else:
        print(f"Miss at {chr(y + 65)}{x + 1}.")
        computer_board.grid[y][x] = 'O'   

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
                if not show_confirmation_popup(screen, row_label, col_label):
                    attack_position = None 
                else: 
                    print(f"Attack position confirmed: {row_label}{col_label}")
                    cursor_active = False
                    return True, cursor_x, cursor_y  # Attack confirmed, turn ends
    cursor_rect = pygame.Rect(520 + cursor_x * CELL_SIZE2, 100 + cursor_y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, cursor_rect, CELL_SIZE2)
    return False, cursor_x, cursor_y  # Turn continues


def player_turn(events, screen, computer_board, cursor_x, cursor_y,cell):
    turn_over = False

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and cursor_x > 0:
                cursor_x -= 1
            elif event.key == pygame.K_RIGHT and cursor_x < computer_board.size - 1:
                cursor_x += 1
            elif event.key == pygame.K_UP and cursor_y > 0:
                cursor_y -= 1
            elif event.key == pygame.K_DOWN and cursor_y < computer_board.size - 1:
                cursor_y += 1
            elif event.key == pygame.K_RETURN:
                attack_position = (cursor_x, cursor_y)
                row_label = chr(cursor_y + 65)
                col_label = str(cursor_x + 1)
                cell = computer_board.grid[cursor_y][cursor_x]
                print(f"Attacking {row_label}{col_label} - Cell content: {cell}")
                if not show_confirmation_popup(screen, row_label, col_label):
                    attack_position = None 
                else: 
                    print(f"Attack position confirmed: {row_label}{col_label}")
                    cursor_active = False
                    if cell == 'S':
                        computer_board.grid[cursor_y][cursor_x] = 'X'
                        show_popup(screen, f"You hit a boat at {row_label}{col_label}")
                        turn_over = True
                    else:
                        computer_board.grid[cursor_y][cursor_x] = 'O'
                        show_popup(screen, f"You hit water at {row_label}{col_label}")
                        turn_over = True
                    
                    return True, cursor_x, cursor_y  # Attack confirmed, turn ends
                 

    cursor_rect = pygame.Rect(520 + cursor_x * CELL_SIZE2, 100 + cursor_y * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, cursor_rect, CELL_SIZE2)

    return turn_over, cursor_x, cursor_y

def show_popup(screen, message):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(300, 200, 200, 300)
    pygame.draw.rect(screen, (200, 200, 200), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

    text_surface = font.render(message, True, (0, 0, 0))
    screen.blit(text_surface, (popup_rect.x + 10, popup_rect.y + 10))

    pygame.display.flip()
    pygame.time.wait(2000)