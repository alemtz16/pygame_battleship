import pygame
import logging
from settings import CELL_SIZE, BLACK

class Board:
    def __init__(self, size, show_ships=True):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.show_ships = show_ships
        logging.debug("Board initialized with size {}x{}.".format(size, size))

    def add_ship(self, ship):
        self.ships.append(ship)
        logging.debug(f"Ship {ship.name} added to the board at {ship.rect.topleft}.")

    def draw(self, screen, cell_size, offset=(0, 0)):
        logging.debug("Starting to draw the board.")
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen)
                logging.debug(f"Drawing ship {ship.name} at {ship.rect.topleft}.")
        logging.debug("Finished drawing the board.")