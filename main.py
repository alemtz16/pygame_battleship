import logging
import pygame
from settings import *
from menu import GameMenu
from board import Board
from ship import Ship
from gui_helpers import draw_button, show_turn_selection_popup, manual_turn_selection, random_turn_selection, show_confirmation_popup
from fleet_config import FLEET
import random
import time
from player import player_turn
from ai_computer import AI, process_ai_attack 
# Add a variable to track the alert display time
alert_start_time = None
alert_duration = 30
pygame.init()
pygame.font.init()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
try:
    FONT_NAME = pygame.font.Font("Anton-Regular.ttf", 36)
except FileNotFoundError:
    logging.error("Font file not found. Make sure 'Anton-Regular.ttf' is in the 'assets/fonts/' directory.")
    FONT_NAME = pygame.font.Font(None, 36)  # Fallback to default font
 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")

menu = GameMenu(screen)
player_board = Board(10)
computer_board = Board(10, show_ships=False)   
cursor_x, cursor_y = 0, 0
cursor_active = False
 
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

ai_player = AI()
cell=ai_player.place_ships([5, 4, 3, 2]) 

next_button = pygame.Rect(700, 550, 100, 50)
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


        instruction_rect = pygame.Rect(460, 450, 334, 50)
        pygame.draw.rect(screen, (200, 200, 200), instruction_rect)
        font = pygame.font.Font(None, 24)
        instruction_text = "Use UP and DOWN arrows to rotate ships"
        text_surface = font.render(instruction_text, True, (0, 0, 0))
        screen.blit(text_surface, (instruction_rect.x + 10, instruction_rect.y + 10))

        if draw_button(screen, "Next", next_button, BLUE, RED, pygame.font.Font(None, 36)) and pygame.mouse.get_pressed()[0]:
            within_bounds, out_of_bounds_ships = player_board.all_ships_within_bounds()
            overlapping_ships = player_board.check_for_overlaps()
            
            if within_bounds and not overlapping_ships:
                choice = show_turn_selection_popup(screen)
                if choice == 'manual':
                    starter = manual_turn_selection(screen)
                    print(f"{starter.capitalize()} will start the game")
                elif choice == 'random':
                    starter = random_turn_selection(screen)
                    print(f"{starter.capitalize()} will start the game")


                game_state = 'GAME'
                logging.debug("Transitioning to GAME state.")
                for ship in ships:
                    ship.update_position(ship.start_cell_position, CELL_SIZE2)
                    ship.update_image(CELL_SIZE2)
                screen = pygame.display.set_mode((950, WINDOW_HEIGHT))
                current_turn = starter

                print("AI Ship Positions:")
                for ship_positions in ai_player.get_ship_positions():
                    formatted_positions = [f"{chr(y + 65)}{x + 1}" for x, y in ship_positions]
                    print(f"Ship at {', '.join(formatted_positions)}")
                for ship_positions in ai_player.get_ship_positions():
                    print(ship_positions)

            else:
                if not within_bounds:
                    logging.debug(f"Ships out of bounds: {', '.join(out_of_bounds_ships)}")
                    alert_message = f"Ships out of bounds: {', '.join(out_of_bounds_ships)}"
                elif overlapping_ships:
                    logging.debug(f"Ships overlapping: {', '.join(overlapping_ships)}")
                    alert_message = f"Ships overlapping: {', '.join(overlapping_ships)}"
                font = pygame.font.Font(None, 36)
                text_surface = font.render(alert_message, True, (255, 0, 0))
                screen.blit(text_surface, (50, 520))
                alert_start_time = time.time()







        if alert_start_time is not None:
            elapsed_time = time.time() - alert_start_time
            if elapsed_time < alert_duration:
                font = pygame.font.Font(None, 36)
                text_surface = font.render(alert_message, True, (255, 0, 0))
                screen.blit(text_surface, (50, 520))
            else:
                alert_start_time = None 

    elif game_state == 'GAME':
        player_board.draw(screen, CELL_SIZE2, offset=(50, 100),title="Player Board")   
        computer_board.draw(screen, CELL_SIZE2, offset=(520, 100),title="Computer Board")  

       
        occupied_positions = []

        for ship in player_board.ships:
            occupied_positions.extend(ship.get_occupied_positions())
        
        if current_turn == 'player':
            turn_over, cursor_x, cursor_y = player_turn(events, screen, computer_board, cursor_x, cursor_y, cell)
            if turn_over:
                if computer_board.check_game_over():
                    print("Player wins!")
                    running = False
                else:
                    current_turn = 'computer'
        elif current_turn == 'computer':
            process_ai_attack(ai_player, player_board)
            if player_board.check_game_over():
                print("AI wins!")
                running = False
            else:
                current_turn = 'player'

        font = pygame.font.Font(None, 36)
        turn_message = f"{current_turn.capitalize()}'s turn"
        turn_surface = font.render(turn_message, True, RED)
        screen.blit(turn_surface, (500, 500))

    pygame.display.flip()

pygame.quit()