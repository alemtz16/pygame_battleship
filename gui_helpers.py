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

 
def show_end_game_popup(screen, message, button_text):
    font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 36)
    
    screen_width, screen_height = screen.get_size()
    popup_rect = pygame.Rect(0, 0, screen_width, screen_height)
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)

    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text_surface, text_rect)

    button_rect = pygame.Rect((screen_width - 200) // 2, (screen_height + 50) // 2, 200, 50)
    pygame.draw.rect(screen, WHITE, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)

    button_text_surface = button_font.render(button_text, True, BLACK)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    screen.blit(button_text_surface, button_text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

    pygame.quit()
    exit()


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
    
    draw_button(screen, "Manual", manual_button, (0, 0, 0), GRAY, pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)) 
    draw_button(screen, "Random", random_button, (0, 0, 0), GRAY, pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE))
    
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
                
def show_attack_result_popup(screen, message, duration=2):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(300, 150, 300, 200)
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)

    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(popup_rect.x + popup_rect.width // 2, popup_rect.y + popup_rect.height // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    pygame.time.wait(duration * 1000)

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

                    result_text = font.render(f"Computer starts the game!", True, BLACK)
                    result_rect = result_text.get_rect(center=(manual_rect.x + manual_rect.width // 2,  manual_rect.y + manual_rect.height // 2))

                    screen.fill(GRAY, manual_rect)
                    pygame.draw.rect(screen, BLACK, manual_rect, 2)
                    screen.blit(result_text, result_rect)

                    pygame.display.flip()
                    pygame.time.wait(2000)
                    return 'computer'
                elif player_button.collidepoint(event.pos):
                    result_text = font.render(f"Player starts the game!", True, BLACK)
                    result_rect = result_text.get_rect(center=(manual_rect.x + manual_rect.width // 2, manual_rect.y + manual_rect.height // 2))

                    screen.fill(GRAY, manual_rect)
                    pygame.draw.rect(screen, BLACK, manual_rect, 2)
                    screen.blit(result_text, result_rect)

                    pygame.display.flip()
                    pygame.time.wait(2000)
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


def show_confirmation_popup(screen, row_label, col_label):
    popup_rect = pygame.Rect(300, 200, 200, 100)
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)

    font = pygame.font.Font(None, 24)
    confirm_text = f"Confirm attack at {row_label}{col_label}?"
    confirm_surface = font.render(confirm_text, True, BLACK)
    screen.blit(confirm_surface, (popup_rect.x + 10, popup_rect.y + 10))

    yes_button = pygame.Rect(popup_rect.x + 20, popup_rect.y + 50, 60, 30)
    no_button = pygame.Rect(popup_rect.x + 120, popup_rect.y + 50, 60, 30)
    draw_button(screen, "Yes", yes_button, BLUE, RED, font)
    draw_button(screen, "No", no_button, BLUE, RED, font)

    pygame.display.flip()

    confirming = True
    while confirming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    print(f"Attack confirmed at {row_label}{col_label}")
                    confirming = False
                    return True  
                elif no_button.collidepoint(event.pos):
                    confirming = False
                    return False   

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

def show_no_repetition(screen, message, duration=2):
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(200, 200, 600, 150) 
    pygame.draw.rect(screen, GRAY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)

    lines = message.split('\n')
    y_offset = 50

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(popup_rect.x + popup_rect.width // 2, popup_rect.y + y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 40  

    pygame.display.flip()
    pygame.time.wait(duration * 1000)