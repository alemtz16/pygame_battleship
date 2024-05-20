import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2, BLACK

class Board:
    def __init__(self, size, show_ships=True):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.show_ships = show_ships
 

    def add_ship(self, ship):
        self.ships.append(ship)
     

    def draw(self, screen, cell_size, offset=(0, 0), title=""):
 
        font = pygame.font.Font(None, 36)
        title_surface = font.render(title, True, BLACK)
        screen.blit(title_surface, (offset[0], offset[1] - 40))

        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen) 