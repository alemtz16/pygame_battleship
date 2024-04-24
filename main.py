# main.py

import pygame
import sys
from settings import *
from menu import GameMenu
from board import Board
from ship import Ship
from gui_helpers import handle_drag_and_drop, show_message

# Inicialización de Pygame
pygame.init()

# Establecer el tamaño de la ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battleship")

# Crear el menú del juego
menu = GameMenu(screen)

# Crear los tableros para el jugador y la computadora
player_board = Board(10)  # Tablero del jugador
computer_board = Board(10)  # Tablero de la computadora


ships = [
    Ship(2),  # Barco pequeño
    Ship(3),
    Ship(4),
    Ship(5),
    Ship(6),
]

dragging_ship = None
# Crear instancias de Ship y asignarlos a los tableros
# Para el jugador
destroyer = Ship(2)  # Destructor de tamaño 2
submarine = Ship(3)  # Submarino de tamaño 3
battleship = Ship(4)  # Acorazado de tamaño 4
player_board.place_ship(destroyer)  # Colocar el destructor
player_board.place_ship(submarine)  # Colocar el submarino
player_board.place_ship(battleship)  # Colocar el acorazado

# Para la computadora
comp_destroyer = Ship(2, start_position=(2, 2))
comp_submarine = Ship(3, start_position=(4, 4))
comp_battleship = Ship(4, start_position=(6, 6))
computer_board.place_ship(comp_destroyer)  # Colocar el destructor
computer_board.place_ship(comp_submarine)  # Colocar el submarino
computer_board.place_ship(comp_battleship)  # Colocar el acorazado

# Variables de control
in_menu = True  # Indica si estamos en el menú
game_running = False  # Indica si el juego está en ejecución
game_started = False  # Indica si el juego ha comenzado (para arrastrar y soltar)

# Bucle principal del juego
while True:
    if in_menu:
        # Mostrar el menú del juego
        menu.draw()
        menu_event = menu.handle_events()

        if menu_event == "start_game":
            in_menu = False  # Salir del menú para empezar el juego
            game_running = True  # El juego comienza
        elif menu_event == "exit":
            break  # Salir del bucle para terminar el juego
    elif game_running:
        # Limpiar la pantalla para el juego
        screen.fill(WHITE)

        # Dibujar los tableros
        player_board.draw(screen, CELL_SIZE, offset=(20, 50))  # Tablero del jugador
        computer_board.draw(screen, CELL_SIZE, offset=(450, 50))  # Tablero de la computadora

 
        # Mostrar información para el jugador
        font = pygame.font.Font(None, TEXT_FONT_SIZE)
        show_message(screen, "Player Board", font, BLACK, (150, 20), duration=0)  # Mostrar el nombre del tablero del jugador
        show_message(screen, "Computer Board", font, BLACK, (450, 20), duration=0)  # Mostrar el nombre del tablero de la computadora

           # Actualizar la pantalla
        dragging_ship = None
        # Manejar eventos del juego
        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            dragging_ship = handle_drag_and_drop(dragging_ship, player_board.size, event, dragging_ship)  # Corregir el comportamiento de arrastre

            for ship in ships:
                dragging_ship = handle_drag_and_drop(ship, player_board.size, event, dragging_ship)  # Corregir el comportamiento de arrastre

            # Comenzar el juego cuando el usuario está listo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True  # El juego comienza oficialmente

            if game_started:
                # Manejar disparos a los tableros
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()  # Posición del mouse
                    cell_pos = (
                        (mouse_pos[0] - 350) // CELL_SIZE, 
                        (mouse_pos[1] - 50) // CELL_SIZE
                    )  # Coordenadas en el tablero de la computadora

                    # Verificar si es un disparo válido
                    if 0 <= cell_pos[0] < computer_board.size and 0 <= cell_pos[1] < computer_board.size:
                        hit = computer_board.check_shot(cell_pos)  # Verificar si es un golpe

                        if hit:
                            show_message(screen, "Hit!", font, RED, (450, 450), duration=1)  # Mostrar "Hit" si es un golpe
                        else:
                            show_message(screen, "Miss!", font, BLUE, (450, 450), duration=1)  # Mostrar "Miss" si no golpea

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Rotar el barco seleccionado
                    if dragging_ship:
                        dragging_ship.rotate()  # Cambia la orientación
 
        for ship in ships:
            pos_x = ship.start_position[0] * CELL_SIZE + 50
            pos_y = ship.start_position[1] * CELL_SIZE + 50
            size_x = (ship.size if ship.orientation == 'horizontal' else 1) * CELL_SIZE
            size_y = (1 if ship.orientation == 'horizontal' else ship.size) * CELL_SIZE
            
            pygame.draw.rect(
                screen,
                BLACK,
                pygame.Rect(pos_x, pos_y, size_x, size_y),
            )

        pygame.display.flip()