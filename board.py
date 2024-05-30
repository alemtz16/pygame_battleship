import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2, BLACK

class Board:
    def __init__(self, size, show_ships=True):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.show_ships = show_ships
        self.row_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.column_labels = [str(i + 1) for i in range(size)]  

    def add_ship(self, ship):
        self.ships.append(ship)
        self.update_grid_with_ship(ship)

    def update_grid_with_ship(self, ship):
        for position in ship.get_occupied_positions():
            x, y = position
            x_num = int(x) - 1
            y_num = ord(y.upper()) - 65
            if 0 <= x_num < self.size and 0 <= y_num < self.size:
                self.grid[y_num][x_num] = ship.name

    def all_ships_within_bounds(self):
        for ship in self.ships:
            for x, y in ship.get_occupied_positions():
                x_num = int(x) - 1
                y_num = ord(y) - 65
                if x_num < 0 or x_num >= self.size or y_num < 0 or y_num >= self.size:
                    logging.debug(f"Ship {ship.name} out of bounds at position ({x}, {y})")
                    return False
        return True
    
    def all_ships_within_bounds(self):
        out_of_bounds_ships = []
        all_within_bounds = True
        for ship in self.ships:
            for x, y in ship.get_occupied_positions():
                x_num = int(x) - 1  
                y_num = ord(y) - 65  
                if x_num < 0 or x_num >= self.size or y_num < 0 or y_num >= self.size:
                    logging.debug(f"Ship {ship.name} out of bounds at position ({x}, {y})")
                    out_of_bounds_ships.append(ship.name)
                    all_within_bounds = False
                    break
        return all_within_bounds, out_of_bounds_ships



    def draw(self, screen, cell_size, offset=(0, 0), title="Player Board"):
        font = pygame.font.Font(None, 36)
        title_width, title_height = font.size(title)
        grid_width = self.size * cell_size
 
        title_x = offset[0] + (grid_width - title_width) // 2
        title_y = offset[1] - title_height - 50  
 
        title_surface = font.render(title, True, BLACK)
        screen.blit(title_surface, (title_x, title_y))

 

 
        for i, label in enumerate(self.row_labels):
            label_surface = font.render(label, True, BLACK)
            label_width, _ = font.size(label)
 
            screen.blit(label_surface, (offset[0] - label_width - 10, offset[1] + i * cell_size + (cell_size // 2 - font.get_height() // 2)))

 
        for i, label in enumerate(self.column_labels):
            label_surface = font.render(label, True, BLACK)
            _, label_height = font.size(label)
 
            screen.blit(label_surface, (offset[0] + i * cell_size + (cell_size // 2 - font.size(label)[0] // 2), offset[1] - label_height - 10))

 
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

 
        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen)