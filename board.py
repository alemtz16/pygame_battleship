# board.py

import pygame
from ship import Ship

class Board:
    def __init__(self, size):
        """
        Inicializa el tablero con una matriz cuadrada de un tamaño específico.
        """
        self.size = size  # Tamaño del tablero
        # Crear una matriz 2D para representar el tablero
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []  # Lista para mantener los barcos colocados en el tablero

    def place_ship(self, ship):
        """
        Coloca un barco en el tablero si las posiciones son válidas.
        """
        positions = ship.get_positions()  # Obtiene las posiciones que ocupa el barco

        # Verificar si todas las posiciones están dentro del tablero y no están ocupadas
        if all(self.is_within_bounds(pos) and not self.grid[pos[1]][pos[0]] for pos in positions):
            for pos in positions:
                self.grid[pos[1]][pos[0]] = ship  # Marca la posición en la cuadrícula
            self.ships.append(ship)  # Añade el barco a la lista de barcos
            return True
        return False

    def is_within_bounds(self, position):
        """
        Verifica si una posición está dentro del tablero.
        """
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def receive_shot(self, position):
        """
        Recibe un disparo en una posición y devuelve True si golpea un barco.
        """
        x, y = position
        if not self.is_within_bounds(position):
            return False  # Disparo fuera del tablero

        if self.grid[y][x] is not None:
            ship = self.grid[y][x]
            self.grid[y][x] = "hit"  # Marcar como golpeado
            return True
        return False

    def is_sunk(self, ship):
        """
        Determina si un barco está completamente hundido.
        """
        positions = ship.get_positions()  # Obtiene las posiciones del barco
        # Verificar si todas las posiciones están marcadas como golpeadas
        return all(self.grid[pos[1]][pos[0]] == "hit" for pos in positions)

    def draw(self, screen, cell_size, offset=(0, 0)):
        """
        Dibuja el tablero en la pantalla.
        """
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(
                    offset[0] + x * cell_size,
                    offset[1] + y * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(screen, (0,0,0), rect, 1)  # Dibuja la celda

                if self.grid[y][x] == "hit":
                    # Dibuja un marcador para un golpe
                    pygame.draw.circle(
                        screen,
                        (255, 0, 0),
                        (rect.centerx, rect.centery),
                        cell_size // 4,
                    )
