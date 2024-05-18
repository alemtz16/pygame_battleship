import pygame
from settings import *
import logging

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
            ship.start_position[0] * CELL_SIZE,
            ship.start_position[1] * CELL_SIZE,
            ship.size * CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE,
            ship.size * CELL_SIZE if ship.orientation == 'vertical' else CELL_SIZE
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
