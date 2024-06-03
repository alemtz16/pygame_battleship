import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2, BLACK, BLUE, RED
from ship import *
from ai_computer import *
class Board:
    def __init__(self, size, show_ships=True):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.show_ships = show_ships
        self.row_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.column_labels = [str(i + 1) for i in range(size)]
        self.sunk_ships = []  # Add this line

    def add_ship(self, ship):
        self.ships.append(ship)
        self.update_grid_with_ship(ship)

    def update_grid_with_ship(self, ship):
        for position in ship.get_occupied_positions():
            x, y = position
            x = x-1
            y = y-1
            if 0 <= x < self.size and 0 <= y < self.size:
                self.grid[y][x] = 'S'

    def print_grid(self) -> None:
        for row in self.grid:
            print(' '.join(['S' if cell == 'S' else '.' for cell in row]))

    def all_ships_within_bounds(self):
        out_of_bounds_ships = []
        all_within_bounds = True
        for ship in self.ships:
            for x, y in ship.get_occupied_positions():
                if x < 0 or x > self.size or y < 0 or y > self.size:
                    out_of_bounds_ships.append(ship.name)
                    all_within_bounds = False
                    break
        return all_within_bounds, out_of_bounds_ships

    def check_for_overlaps(self):
        position_count = {}
        overlapping_ships = []
        for ship in self.ships:
            for position in ship.get_occupied_positions():
                if position in position_count:
                    position_count[position].append(ship.name)
                else:
                    position_count[position] = [ship.name]

        for positions, ships in position_count.items():
            if len(ships) > 1:
                overlapping_ships.extend(ships)

        return list(set(overlapping_ships))

    def draw(self, screen, cell_size, offset=(0, 0), title="Player Board"):
        font = pygame.font.SysFont(None, 36)
        red_image = pygame.image.load('assets/images/redtoken.png')
        red_image = pygame.transform.scale(red_image, (CELL_SIZE2, CELL_SIZE2))
        blue_image = pygame.image.load('assets/images/bluetoken.png')
        blue_image = pygame.transform.scale(blue_image, (CELL_SIZE2, CELL_SIZE2))
        title_surface = font.render(title, True, BLACK)
        title_width, title_height = title_surface.get_size()
        grid_width = self.size * cell_size

        title_x = offset[0] + (grid_width - title_width) // 2
        title_y = offset[1] - title_height - 50

        screen.blit(title_surface, (title_x, title_y))

        for i, label in enumerate(self.row_labels):
            label_surface = font.render(label, True, BLACK)
            label_width, _ = label_surface.get_size()

            screen.blit(label_surface, (offset[0] - label_width - 10, offset[1] + i * cell_size + (cell_size // 2 - font.get_height() // 2)))

        for i, label in enumerate(self.column_labels):
            label_surface = font.render(label, True, BLACK)
            _, label_height = label_surface.get_size()

            screen.blit(label_surface, (offset[0] + i * cell_size + (cell_size // 2 - label_surface.get_width() // 2), offset[1] - label_height - 10))

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                tile_rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                if cell == 'O':
                    screen.blit(blue_image, tile_rect.topleft)
                elif cell == 'X':
                    red_rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                    screen.blit(red_image, red_rect.topleft)
                elif cell == 'SUNK':
                    red_rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                    screen.blit(red_image, red_rect.topleft)
                pygame.draw.rect(screen, BLACK, tile_rect, 1)

        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen)
        
        for ship_positions, ship_image_path, orientation in self.sunk_ships:
            x_start, y_start = ship_positions[0]
            ship_image = pygame.image.load(ship_image_path)
            
            if orientation == 'horizontal':
                ship_image = pygame.transform.scale(ship_image, (cell_size * len(ship_positions), cell_size))
            else:
                ship_image = pygame.transform.scale(ship_image, (  cell_size * len(ship_positions),cell_size))
                ship_image = pygame.transform.rotate(ship_image, 90)
          
            screen.blit(ship_image, (offset[0] + x_start * cell_size, offset[1] + y_start * cell_size))

    def draw1(self, screen, cell_size, offset=(0, 0), title="Player Board"):
        font = pygame.font.SysFont(None, 36)
        red_image = pygame.image.load('assets/images/redtoken.png')
        red_image = pygame.transform.scale(red_image, (CELL_SIZE2, CELL_SIZE2))
        blue_image = pygame.image.load('assets/images/bluetoken.png')
        blue_image = pygame.transform.scale(blue_image, (CELL_SIZE2, CELL_SIZE2))
        title_surface = font.render(title, True, BLACK)
        title_width, title_height = title_surface.get_size()
        grid_width = self.size * cell_size

        title_x = offset[0] + (grid_width - title_width) // 2
        title_y = offset[1] - title_height - 50

        screen.blit(title_surface, (title_x, title_y))

        for i, label in enumerate(self.row_labels):
            label_surface = font.render(label, True, BLACK)
            label_width, _ = label_surface.get_size()

            screen.blit(label_surface, (offset[0] - label_width - 10, offset[1] + i * cell_size + (cell_size // 2 - font.get_height() // 2)))

        for i, label in enumerate(self.column_labels):
            label_surface = font.render(label, True, BLACK)
            _, label_height = label_surface.get_size()

            screen.blit(label_surface, (offset[0] + i * cell_size + (cell_size // 2 - label_surface.get_width() // 2), offset[1] - label_height - 10))

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                tile_rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                if cell == 'O':
                    screen.blit(blue_image, tile_rect.topleft)
                elif cell == 'X':
                    red_rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                    screen.blit(red_image, red_rect.topleft)
                elif cell == 'SUNK':
                    red_rect = pygame.Rect(offset[0] + x * cell_size, offset[1] + y * cell_size, cell_size, cell_size)
                    screen.blit(red_image, red_rect.topleft)
                pygame.draw.rect(screen, BLACK, tile_rect, 1)

        if self.show_ships:
            for ship in self.ships:
                ship.draw(screen)
            
    def check_sunk_ship(self, x: int, y: int, screen) -> Ship:
        print(f"Checking if ship at ({x}, {y}) is sunk...")
        red_image = pygame.image.load('assets/images/redtoken.png')
        red_image = pygame.transform.scale(red_image, (CELL_SIZE2, CELL_SIZE2))
        for ship in self.ships:
            occupied_positions = ship.get_occupied_positions()
            print(f"Checking ship: {ship.name} with positions: {occupied_positions}")

            if (x + 1, y + 1) in occupied_positions:
                print(f"Hit position ({x + 1}, {y + 1}) is part of ship: {ship.name}")
                # Adjust the positions to match grid coordinates
                grid_positions = [(pos[0] - 1, pos[1] - 1) for pos in occupied_positions]
                if all(self.grid[pos[1]][pos[0]] == 'X' for pos in grid_positions):
                    self.sunk_ships.append(ship)
                    print(f"Ship {ship.name} is sunk!")
 
                    for pos in grid_positions:
                        tile_rect = pygame.Rect(520 + pos[0] * CELL_SIZE2, 100 + pos[1] * CELL_SIZE2, CELL_SIZE2, CELL_SIZE2)
 
                        screen.blit(red_image, tile_rect.topleft)
                        pygame.draw.rect(screen, BLACK, tile_rect, 1)
                    ship_image_path = ship.image_path
                    ship_image = pygame.image.load(ship_image_path)
                    if ship.orientation == 'horizontal':
                        ship_image = pygame.transform.scale(ship_image, (CELL_SIZE2 * ship.size, CELL_SIZE2))
                    else:
                        ship_image = pygame.transform.scale(ship_image, (CELL_SIZE2, CELL_SIZE2 * ship.size))
                        ship_image = pygame.transform.rotate(ship_image, 90)

                    screen.blit(ship_image, (520 + grid_positions[0][0] * CELL_SIZE2, 100 + grid_positions[0][1] * CELL_SIZE2))
 
                    return ship
        print("No ship is sunk at this position.")
        return None

    def check_game_over(self):
        for row in self.grid:
            for cell in row:
                if isinstance(cell, str) and cell == 'S':  # Check for unhit ship parts
                    return False
        return True

    def print_grid(self):
        for row in self.grid:
            print(' '.join(['S' if cell == 'S' else '.' for cell in row]))

