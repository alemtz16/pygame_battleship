import pygame
from ship import Ship

class Board:
    def __init__(self, size):
        """
        Initializes the board with a square matrix of a specific size.
        """
        self.size = size  
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships = []  
        self.ships_drawn = False  

    def place_ship(self, ship):
        """
        Places a ship on the board if the positions are valid.
        """
        positions = ship.get_positions()  
      

       
        if all(self.is_within_bounds(pos) and not self.grid[pos[1]][pos[0]] for pos in positions):
            for pos in positions:
                self.grid[pos[1]][pos[0]] = ship  
            self.ships.append(ship)  
          
            return True
        else:
           
            return False

    def is_within_bounds(self, position):
        """
        Checks if a position is within the board.
        """
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

   
    def draw(self, screen, cell_size, offset=(0, 0)):

        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(
                    offset[0] + x * cell_size,
                    offset[1] + y * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw the grid cell


        for ship in self.ships:
     
            ship.draw(screen) 


    def receive_shot(self, position):
        """
        Receives a shot at a position and returns True if it hits a ship.
        """
        x, y = position
        if not self.is_within_bounds(position):
            return False 

        if self.grid[y][x] is not None:
            ship = self.grid[y][x]
            self.grid[y][x] = "hit" 
            return True
        return False

 

    def draw_ships_below_board(self, screen, ships, cell_size):
        if self.ships_drawn:
            return  

        start_x = 50 
        start_y = self.size * cell_size + 100 
        x_offset = start_x  
        for idx, ship in enumerate(ships):
            if idx > 0: 
                x_offset += 40
            ship.start_position = (x_offset // cell_size, start_y // cell_size)  
            ship.draw(screen)
            prev_ship = ship 
        self.ships_drawn = True  
