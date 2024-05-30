import pygame
from settings import *
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def draw_button(screen, text, rect, color, hover_color, font):
    """
    Draws a button with the given text and changes color on mouse hover.
    """
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = rect.collidepoint(mouse_pos)

    current_color = hover_color if is_hovering else color
    pygame.draw.rect(screen, current_color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return is_hovering

def show_turn_selection_popup(screen):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(200, 150, 400, 300)
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)
    
    manual_button = pygame.Rect(popup_rect.x + 50, popup_rect.y + 200, 120, 50)
    random_button = pygame.Rect(popup_rect.x + 230, popup_rect.y + 200, 120, 50)
    
    screen.fill(WHITE, popup_rect)
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)
    
    prompt_text = font.render("Choose who starts:", True, BLACK)
    prompt_rect = prompt_text.get_rect(center=(popup_rect.x + popup_rect.width // 2, popup_rect.y + 50))
    screen.blit(prompt_text, prompt_rect)
    
    draw_button(screen, "Manual", manual_button, BLUE, RED, font)
    draw_button(screen, "Random", random_button, BLUE, RED, font)
    
    pygame.display.flip()
    
    waiting_for_selection = True
    while waiting_for_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if manual_button.collidepoint(event.pos):
                    return 'manual'
                elif random_button.collidepoint(event.pos):
                    return 'random'


def manual_turn_selection(screen):
    font = pygame.font.Font(None, 36)
    manual_rect = pygame.Rect(200, 150, 400, 300)
    pygame.draw.rect(screen, GRAY, manual_rect)
    pygame.draw.rect(screen, BLACK, manual_rect, 2)

    computer_button = pygame.Rect(manual_rect.x + 50, manual_rect.y + 200, 120, 50)
    player_button = pygame.Rect(manual_rect.x + 230, manual_rect.y + 200, 120, 50)

    screen.fill(WHITE, manual_rect)
    pygame.draw.rect(screen, GRAY, manual_rect)
    pygame.draw.rect(screen, BLACK, manual_rect, 2)

    prompt_text = font.render("Who starts?", True, BLACK)
    prompt_rect = prompt_text.get_rect(center=(manual_rect.x + manual_rect.width // 2, manual_rect.y + 50))
    screen.blit(prompt_text, prompt_rect)

    draw_button(screen, "Computer", computer_button, BLUE, RED, font)
    draw_button(screen, "Player", player_button, BLUE, RED, font)

    pygame.display.flip()

    waiting_for_selection = True
    while waiting_for_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if computer_button.collidepoint(event.pos):
                    return 'computer'
                elif player_button.collidepoint(event.pos):
                    return 'player'

def random_turn_selection(screen):
    font = pygame.font.Font(None, 36)
    random_rect = pygame.Rect(200, 150, 400, 300)
    pygame.draw.rect(screen, GRAY, random_rect)
    pygame.draw.rect(screen, BLACK, random_rect, 2)

    screen.fill(WHITE, random_rect)
    pygame.draw.rect(screen, GRAY, random_rect)
    pygame.draw.rect(screen, BLACK, random_rect, 2)

    prompt_text = font.render("Deciding who starts...", True, BLACK)
    prompt_rect = prompt_text.get_rect(center=(random_rect.x + random_rect.width // 2, random_rect.y + 50))
    screen.blit(prompt_text, prompt_rect)

    pygame.display.flip()

    choices = ['Computer', 'Player']
    result = random.choice(choices)

    start_time = time.time()
    duration = 6   

    while time.time() - start_time < duration:
        current_choice = random.choice(choices)
        choice_text = font.render(current_choice, True, BLACK)
        choice_rect = choice_text.get_rect(center=(random_rect.x + random_rect.width // 2, random_rect.y + random_rect.height // 2))
        
        screen.fill(GRAY, random_rect)
        pygame.draw.rect(screen, BLACK, random_rect, 2)
        screen.blit(prompt_text, prompt_rect)
        screen.blit(choice_text, choice_rect)

        pygame.display.flip()
        pygame.time.wait(100)  # Adjust this value to control the speed of the roulette effect

    result_text = font.render(f"{result} starts the game!", True, BLACK)
    result_rect = result_text.get_rect(center=(random_rect.x + random_rect.width // 2, random_rect.y + random_rect.height // 2))

    screen.fill(GRAY, random_rect)
    pygame.draw.rect(screen, BLACK, random_rect, 2)
    screen.blit(result_text, result_rect)

    pygame.display.flip()
    pygame.time.wait(2000)  # Display the result for 2 seconds

    return result.lower()


def button_click_event(button_rect, event):
    """
    Returns True if the button is clicked.
    This function now requires an event to be passed to it.
    """
    if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
        logging.debug("Button clicked.")
        return True
    return False

def show_message(screen, text, font, color, position):
    """
    Shows a message on the screen at a given position.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def handle_drag_and_drop(ship, board_size, event, dragging_ship):
    """
    Handles the drag and drop event for a ship based on the passed event.
    """
    mouse_pos = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN and not dragging_ship:
        ship_rect = pygame.Rect(
            ship.start_position[0] * CELL_SIZE2,
            ship.start_position[1] * CELL_SIZE2,
            ship.size * CELL_SIZE2 if ship.orientation == 'horizontal' else CELL_SIZE2,
            ship.size * CELL_SIZE2 if ship.orientation == 'vertical' else CELL_SIZE2
        )
        if ship_rect.collidepoint(mouse_pos):
            dragging_ship = ship

    elif event.type == pygame.MOUSEMOTION and dragging_ship:
        dragging_ship.start_position = (
            mouse_pos[0] // CELL_SIZE,
            mouse_pos[1] // CELL_SIZE
        )

    elif event.type == pygame.MOUSEBUTTONUP and dragging_ship:
        dragging_ship.start_position = (
            max(0, min(board_size - (dragging_ship.size if dragging_ship.orientation == 'horizontal' else 1), dragging_ship.start_position[0])),
            max(0, min(board_size - (dragging_ship.size if dragging_ship.orientation == 'vertical' else 1), dragging_ship.start_position[1]))
        )
        dragging_ship = None

    return dragging_ship
