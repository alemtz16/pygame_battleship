import pygame
import logging
from settings import CELL_SIZE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT
from ship import Ship
from fleet_config import FLEET

# Setup basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Board:
    def __init__(self, size, show_ships=True):
        """
        Initializes the board with a square matrix of a specific size.
        Args:
            size (int): The size of the board (number of cells in one row or column).
            show_ships (bool): Determines if ships are shown on the board.
        """
        self.size = size  
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []  
        self.show_ships = show_ships  # Controls the visibility of ships
        logging.debug("Board initialized with size {}x{}.".format(size, size))

    def add_ship(self, ship):
        """Adds a ship to the board without checking positions."""
        self.ships.append(ship)
        logging.debug(f"Ship {ship.name} added to the board at {ship.rect.topleft}.")

    def place_ship(self, ship):
        """Places a ship on the board if the positions are valid."""
        start_x, start_y = ship.rect.topleft[0] // CELL_SIZE, ship.rect.topleft[1] // CELL_SIZE
        if self.is_within_bounds((start_x, start_y)) and self.grid[start_y][start_x] is None:
            self.grid[start_y][start_x] = ship
            self.ships.append(ship)
            logging.debug(f"Placed ship {ship.name} at grid position ({start_x}, {start_y}).")
            return True
        else:
            logging.warning(f"Failed to place ship {ship.name} at grid position ({start_x}, {start_y}).")
            return False

    def is_within_bounds(self, position):
        """Checks if a position is within the board."""
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def draw(self, screen, cell_size, offset=(0, 0)):
        logging.debug("Starting to draw the board.")
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if self.grid[y][x] is not None:
                    self.grid[y][x].draw(screen)
                    logging.debug(f"Drawing ship at {x}, {y}.")

        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen)
                logging.debug(f"Drawing ship {ship.name} at {ship.rect.topleft}.")
        logging.debug("Finished drawing the board.")


    def receive_shot(self, position):
        """Receives a shot at a position and returns if it hits a ship."""
        x, y = position
        if not self.is_within_bounds(position):
            logging.debug(f"Shot at {position} is out of bounds.")
            return False
        if self.grid[y][x] is not None:
            logging.debug(f"Hit at {position}.")
            self.grid[y][x] = None  # This could be changed to handle hits differently
            return True
        logging.debug(f"Miss at {position}.")
        return False
