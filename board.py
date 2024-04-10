import pygame

class Board:
    def __init__(self, grid_size=10, cell_size=40, offset=(100, 100)):
        """
        Initializes the game board.

        :param grid_size: The size of the grid (number of cells in a row and column)
        :param cell_size: The size of each cell in pixels
        :param offset: The offset from the top left corner of the screen to place the grid
        """
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.offset = offset
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        # 0 represents water, 1 represents part of a ship, and 2 represents a hit on a ship

    def draw(self, screen):
        """
        Draws the board on the screen.

        :param screen: The Pygame screen to draw on
        """
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.grid[row][col]
                color = (255, 255, 255)  # default color for water

                if cell == 1:
                    color = (128, 128, 128)  # color for ship
                elif cell == 2:
                    color = (255, 0, 0)  # color for hit

                pygame.draw.rect(screen, color, (self.offset[0] + col * self.cell_size,
                                                 self.offset[1] + row * self.cell_size,
                                                 self.cell_size, self.cell_size), 0 if cell else 1)

    def place_ship(self, start, end):
        """
        Places a ship on the board.

        :param start: A tuple (row, col) representing the starting position of the ship
        :param end: A tuple (row, col) representing the ending position of the ship
        """
        # Simple implementation: assumes horizontal or vertical placement only
        if start[0] == end[0]:  # Horizontal placement
            for col in range(start[1], end[1] + 1):
                self.grid[start[0]][col] = 1
        elif start[1] == end[1]:  # Vertical placement
            for row in range(start[0], end[0] + 1):
                self.grid[row][start[1]] = 1

    def check_hit(self, position):
        """
        Checks if a given position hits a ship.

        :param position: A tuple (row, col) to check
        :return: True if a ship is hit, False otherwise
        """
        row, col = position
        if self.grid[row][col] == 1:
            self.grid[row][col] = 2  # Mark as hit
            return True
        return False
