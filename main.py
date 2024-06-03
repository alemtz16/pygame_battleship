import logging
import pygame
from settings import *
from menu import GameMenu
from board import Board
from ship import Ship
from gui_helpers import draw_button, show_turn_selection_popup, manual_turn_selection, random_turn_selection, show_end_game_popup
from fleet_config import FLEET
import random
import time
from player import player_turn
from ai_computer import AI, process_ai_attack

# Erase the contents of control_file.txt
open("control_file.txt", "w").close()

# Add a variable to track the alert display time
alert_start_time = None
alert_duration = 30

pygame.init()
pygame.font.init()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")

menu = GameMenu(screen)
player_board = Board(10)
computer_board = Board(10, show_ships=False)
cursor_x, cursor_y = 0, 0
cursor_active = False
show_instructions = False
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
def reset_ships():
    global ships, player_board
    player_board = Board(10)
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
reset_button = pygame.Rect(580, 550, 100, 50)

clock = pygame.time.Clock()

ai_player = AI()
ai_player.place_ships([5, 4, 3, 2])
player_moves = []
ai_moves = []

# Variables for turn popup
turn_popup_start_time = None
turn_popup_duration = 2  # seconds
show_turn_popup = False
current_turn = 'player'  # This variable keeps track of whose turn it is

running = True
with open("control_file.txt", "w") as file:
    file.write("CONTROL FILE:\n\n")

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
            show_instructions = True
            game_state = 'INSTRUCTIONS'
        elif menu_action == 'exit':
            running = False

    if game_state == 'MENU':
        menu.draw()
    elif game_state == 'INSTRUCTIONS':
        popup_rect = pygame.Rect(50, 150, 700, 300)
        pygame.draw.rect(screen, GRAY, popup_rect)
        pygame.draw.rect(screen, BLACK, popup_rect, 2)

        font = pygame.font.Font(None, 36)
        instructions = [
            "Instructions",
            "Drag and drop the boats to your desired position",
            "Use the UP and DOWN keys to change the orientation",
            "Click 'Next' once in desired position"
        ]
        y_offset = popup_rect.y + 50
        for line in instructions:
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (popup_rect.x + 20, y_offset))
            y_offset += 50

        close_button = pygame.Rect(popup_rect.x + 300, popup_rect.y + 350, 100, 50)
        pygame.draw.rect(screen, RED, close_button)
        pygame.draw.rect(screen, BLACK, close_button, 2)
        close_text = font.render("Close", True, WHITE)
        screen.blit(close_text, (close_button.x + 20, close_button.y + 10))

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    show_instructions = False
                    game_state = 'SETUP'
                    logging.debug("Transitioning to SETUP state.")
                    for ship in ships:
                        ship.update_image(CELL_SIZE2)

    elif game_state == 'SETUP':
        player_board.draw(screen, CELL_SIZE2, offset=(50, 100), title="Player Board")
        for ship in player_board.ships:
            ship.draw(screen)
            for event in events:
                ship.handle_mouse_event(event, ships)
                if ship.selected:
                    ship.handle_keyboard_event(event)

        if draw_button(screen, "Next", next_button, BLUE, RED, pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)) and pygame.mouse.get_pressed()[0]:
            within_bounds, out_of_bounds_ships = player_board.all_ships_within_bounds()
            overlapping_ships = player_board.check_for_overlaps()

            #Si todos los barcos se colocaron correctamente
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

                # Update the player's board grid to mark ship positions
                player_board.grid = [[None for _ in range(player_board.size)] for _ in range(player_board.size)]
                for ship in player_board.ships:
                    player_board.update_grid_with_ship(ship)
                player_board.print_grid() #

                screen = pygame.display.set_mode((950, WINDOW_HEIGHT))
                current_turn = starter

                show_turn_popup = True
                turn_popup_start_time = time.time()

                # Print player ship positions
                print("Player Ship Positions:")
                for ship in player_board.ships:
                    ship_positions = ship.get_occupied_positions()
                    formatted_positions = [f"{chr(y + 64)}{x}" for x, y in ship_positions]
                    print(f"Ship at {', '.join(formatted_positions)}")
                for ship in player_board.ships:
                    print(ship.get_occupied_positions())

                print("AI Ship Positions:")
                for ship_positions in ai_player.get_ship_positions():
                    formatted_positions = [f"{chr(y + 65)}{x + 1}" for x, y in ship_positions]
                    print(f"Ship at {', '.join(formatted_positions)}")
                for ship_positions in ai_player.get_ship_positions():
                    print(ship_positions)
                ai_player.print_grid()

            #error si no se colocaron correctamente
            else:
                if not within_bounds:
                    logging.debug(f"Ships out of bounds: {', '.join(out_of_bounds_ships)}")
                    alert_message = f"Ships out of bounds: {', '.join(out_of_bounds_ships)}"
                elif overlapping_ships:
                    logging.debug(f"Ships overlapping: {', '.join(overlapping_ships)}")
                    alert_message = f"Ships overlapping: {', '.join(overlapping_ships)}"
                font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
                text_surface = font.render(alert_message, True, (255, 0, 0))
                screen.blit(text_surface, (50, 520))
                alert_start_time = time.time()

        if draw_button(screen, "Reset", reset_button, BLUE, RED, pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)) and pygame.mouse.get_pressed()[0]:
            reset_ships()
        if alert_start_time is not None:
            elapsed_time = time.time() - alert_start_time
            if elapsed_time < alert_duration:
                font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
                text_surface = font.render(alert_message, True, (255, 0, 0))
                screen.blit(text_surface, (50, 520))
            else:
                alert_start_time = None

    elif game_state == 'GAME':
        player_board.draw(screen, CELL_SIZE2, offset=(50, 100), title="Player Board")
        computer_board.draw(screen, CELL_SIZE2, offset=(520, 100), title="Computer Board")
        # After placing ships

        if show_turn_popup:
            elapsed_time = time.time() - turn_popup_start_time
            if elapsed_time < turn_popup_duration:
                font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
                turn_message = f"{current_turn.capitalize()}'s turn"
                turn_surface = font.render(turn_message, True, BLACK)
                turn_rect = turn_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

                popup_rect = pygame.Rect(turn_rect.x - 10, turn_rect.y - 10, turn_rect.width + 20, turn_rect.height + 20)
                pygame.draw.rect(screen, GRAY, popup_rect)
                pygame.draw.rect(screen, BLACK, popup_rect, 2)
                screen.blit(turn_surface, turn_rect)
            else:
                show_turn_popup = False

        if current_turn == 'player' and not show_turn_popup:
            turn_over, cursor_x, cursor_y = player_turn(events, screen, ai_player, cursor_x, cursor_y,computer_board)
            if turn_over:
                player_moves.append(f"Player attacked {chr(cursor_y + 65)}{cursor_x + 1}")
                if ai_player.check_game_over():
                    show_end_game_popup(screen, "Congratulations, you win!", "End Game")
                    running = False
                else:
                    current_turn = 'computer'
                    show_turn_popup = True
                    turn_popup_start_time = time.time()
        elif current_turn == 'computer' and not show_turn_popup:
            #ai_move = ai_player.make_move()
            #ai_moves.append(f"AI attacked {chr(ai_move[1] + 65)}{ai_move[0] + 1}")
            process_ai_attack(screen,ai_player, player_board)
            if player_board.check_game_over():
                show_end_game_popup(screen, "Better luck next time, AI wins!", "End Game")
                running = False
            else:
                current_turn = 'player'
                show_turn_popup = True
                turn_popup_start_time = time.time()

    pygame.display.flip()

pygame.quit()
