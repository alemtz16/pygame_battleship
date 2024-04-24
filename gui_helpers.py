import pygame
from settings import *

# Función para dibujar botones
def draw_button(screen, text, rect, color, hover_color, font):
    """
    Dibuja un botón con el texto dado y cambia de color al pasar el mouse.
    """
    mouse_pos = pygame.mouse.get_pos()  # Posición actual del mouse
    is_hovering = rect.collidepoint(mouse_pos)  # Verifica si el mouse está sobre el botón

    # Escoge el color según si el mouse está sobre el botón
    current_color = hover_color if is_hovering else color
    pygame.draw.rect(screen, current_color, rect)  # Dibuja el botón
    pygame.draw.rect(screen, BLACK, rect, 2)  # Dibuja el borde del botón

    # Dibuja el texto centrado en el botón
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)  # Coloca el texto en el centro

    return is_hovering  # Devuelve si el mouse está sobre el botón


# Función para detectar clics en botones
def button_click_event(button_rect):
    """
    Devuelve True si el botón está clickeado.
    """
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                return True  # El botón fue clickeado
    return False


# Función para mostrar mensajes en pantalla
def show_message(screen, text, font, color, position, duration=2):
    """
    Muestra un mensaje en la pantalla durante un tiempo especificado.
    """
    text_surface = font.render(text, True, color)  # Crea el texto
    text_rect = text_surface.get_rect(center=position)  # Posiciona el texto
    start_time = pygame.time.get_ticks()  # Tiempo de inicio del mensaje
    
    # Mostrar el mensaje durante el tiempo especificado
    while pygame.time.get_ticks() - start_time < duration * 1000:
        screen.blit(text_surface, text_rect)  # Dibuja el mensaje
        pygame.display.flip()  # Actualiza la pantalla


# Función para implementar Drag and Drop
def handle_drag_and_drop(ship, board_size, event, dragging_ship):
    """
    Maneja el evento de arrastrar y soltar para un barco.
    """
    mouse_pos = pygame.mouse.get_pos()  # Posición actual del mouse

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Verifica si el clic se hizo sobre el barco
        ship_rect = pygame.Rect(
            ship.start_position[0] * CELL_SIZE, 
            ship.start_position[1] * CELL_SIZE, 
            ship.size * CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE, 
            ship.size * CELL_SIZE if ship.orientation == 'vertical' else CELL_SIZE
        )
        if ship_rect.collidepoint(mouse_pos):
            dragging_ship = ship  # Iniciar el arrastre

    elif event.type == pygame.MOUSEMOTION and dragging_ship:
        # Ajustar la posición mientras se arrastra
        dragging_ship.start_position = (
            mouse_pos[0] // CELL_SIZE,
            mouse_pos[1] // CELL_SIZE
        )

    elif event.type == pygame.MOUSEBUTTONUP and dragging_ship:
        # Ajustar la posición para mantener dentro del tablero
        dragging_ship.start_position = (
            max(0, min(board_size - (dragging_ship.size if dragging_ship.orientation == 'horizontal' else 1), dragging_ship.start_position[0])),
            max(0, min(board_size - (dragging_ship.size if dragging_ship.orientation == 'vertical' else 1), dragging_ship.start_position[1]))
        )
        dragging_ship = None  # Terminar el arrastre

    return dragging_ship  # Devuelve el barco arrastrado
