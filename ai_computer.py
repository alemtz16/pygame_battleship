import random
from typing import List, Tuple
from gui_helpers import show_attack_result_popup

class Coordinates:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class GridCoordinate:
    def __init__(self, x, y, x_val=0, y_val=0):
        self.x = x
        self.y = y
        self.x_val = x_val
        self.y_val = y_val
        self.x_val_rev = 0
        self.y_val_rev = 0
        self._sumx = 0
        self._sumy = 0

    def add_xy(self, x_val, y_val):
        self.x_val_rev = x_val
        self.y_val_rev = y_val
        self._sumx = self._sum(self.x_val, self.x_val_rev)
        self._sumy = self._sum(self.y_val, self.y_val_rev)

    def get_score(self):
        result = self._sumx * self._sumy
        if result < 80:
            return result
        else:
            return 67 if not random.randint(0, 4) else 61

    def _sum(self, a, b):
        return (a + b) - abs(a - b)

class AI:
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        self.shots_fired = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.ships = []
        self._dm_size = grid_size - 1
        self._dm = [[GridCoordinate(x, y) for x in range(grid_size)] for y in range(grid_size)]
        self._enemy_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self._max_size = 5
        self.last_shot = Coordinates()
        self.hit_list = []
        self.ship_orientation = None
        self.hit_direction = None
        self.switch_direction = False

    SHOT_FIRED = 1
    SHIP_HIT = 2

    def place_ships(self, ship_sizes: List[int]) -> None:
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                x, y = random.randint(0, self.grid_size - size), random.randint(0, self.grid_size - size)

                if self.can_place_ship(x, y, size, orientation):
                    self.ships.append((x, y, size, orientation))
                    for i in range(size):
                        if orientation == 'horizontal':
                            self.grid[y][x + i] = 'S'
                        else:
                            self.grid[y + i][x] = 'S'
                    placed = True

    def can_place_ship(self, x: int, y: int, size: int, orientation: str) -> bool:
        for i in range(size):
            if orientation == 'horizontal':
                if x + i >= self.grid_size or self.grid[y][x + i] == 'S':
                    return False
            else:
                if y + i >= self.grid_size or self.grid[y + i][x] == 'S':
                    return False
        return True

    def mark_shot(self, x: int, y: int, hit: bool = False) -> None:
        self.shots_fired[y][x] = True
        self._enemy_grid[y][x] = self.SHIP_HIT if hit else self.SHOT_FIRED

    def make_move(self) -> Tuple[int, int]:
        if self.hit_list:
            return self._get_coordinates_sink()
        else:
            return self._get_coordinates_find()

    def process_hit(self, x: int, y: int) -> None:
        self.hit_list.append(Coordinates(x, y))
        self.determine_orientation()
        self.hit_direction = None
        self.switch_direction = False

    def determine_orientation(self) -> None:
        if len(self.hit_list) >= 2:
            if self.hit_list[-1].x == self.hit_list[-2].x:
                self.ship_orientation = 'vertical'
            elif self.hit_list[-1].y == self.hit_list[-2].y:
                self.ship_orientation = 'horizontal'

    def _get_coordinates_find(self) -> Tuple[int, int]:
        pattern = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) if (x + y) % 2 == 0]
        random.shuffle(pattern)
        for (x, y) in pattern:
            if not self.shots_fired[y][x]:
                self.last_shot = Coordinates(x, y)
                self.mark_shot(x, y)
                return x, y
        return 0, 0

    def _get_coordinates_sink(self) -> Tuple[int, int]:
        if not self.hit_list:
            return self._get_coordinates_find()

        directions = self._get_possible_directions()
        for dx, dy in directions:
            nx, ny = self.hit_list[-1].x + dx, self.hit_list[-1].y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and not self.shots_fired[ny][nx]:
                self.last_shot = Coordinates(nx, ny)
                self.mark_shot(nx, ny)
                return nx, ny

        if self.ship_orientation and not self.switch_direction:
            self.switch_direction = True
            self.hit_list.reverse()
        else:
            self.switch_direction = False
            self.hit_list.pop()

        if not self.hit_list:
            return self._get_coordinates_find()
        return self._get_coordinates_sink()

    def _get_possible_directions(self) -> List[Tuple[int, int]]:
        if self.ship_orientation:
            if self.ship_orientation == 'horizontal':
                return [(1, 0), (-1, 0)]
            else:
                return [(0, 1), (0, -1)]
        return [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def get_ship_positions(self) -> List[List[Tuple[int, int]]]:
        ship_positions = []
        for x, y, size, orientation in self.ships:
            positions = []
            for i in range(size):
                if orientation == 'horizontal':
                    positions.append((x + i, y))
                else:
                    positions.append((x, y + i))
            ship_positions.append(positions)
        return ship_positions

    def print_grid(self) -> None:
        for row in self.grid:
            print(' '.join(['S' if cell == 'S' else '.' for cell in row]))

    def check_game_over(self):
        for row in self.grid:
            for cell in row:
                if isinstance(cell, str) and cell == 'S':
                    return False
        return True

def process_ai_attack(screen, ai_player: AI, player_board) -> None:
    ai_move = ai_player.make_move()
    x, y = ai_move
    cell = player_board.grid[y][x]
    if cell == 'S':
        print(f"AI hit at {chr(y + 65)}{x + 1}!")
        player_board.grid[y][x] = 'X'
        ai_player.mark_shot(x, y, hit=True)
        ai_player.process_hit(x, y)
        show_attack_result_popup(screen, "AI hit a boat!", duration=2)
    else:
        print(f"AI miss at {chr(y + 65)}{x + 1}.")
        player_board.grid[y][x] = 'O'
        ai_player.mark_shot(x, y, hit=False)
        show_attack_result_popup(screen, "AI hit water!", duration=2)
