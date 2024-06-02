import random
from typing import List, Tuple
from gui_helpers import  show_attack_result_popup

class AI:
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.dynamic_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.shots_fired = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.high_scores = []
        self.ships = []
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        self.heatmap = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.init_heatmap()

    def init_heatmap(self) -> None:
        pattern = [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            [5, 1, 2, 2, 2, 2, 2, 2, 1, 5],
            [5, 1, 2, 3, 3, 3, 3, 2, 1, 5],
            [5, 1, 2, 3, 4, 4, 3, 2, 1, 5],
            [5, 1, 2, 3, 4, 4, 3, 2, 1, 5],
            [5, 1, 2, 3, 3, 3, 3, 2, 1, 5],
            [5, 1, 2, 2, 2, 2, 2, 2, 1, 5],
            [5, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        ]
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.heatmap[y][x] = pattern[y][x]

    def place_ships(self, ship_sizes: List[int]) -> None:
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                x, y = self.find_best_position(size, orientation)

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

    def find_best_position(self, size: int, orientation: str) -> Tuple[int, int]:
        best_score = -1
        best_position = (0, 0)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.can_place_ship(x, y, size, orientation):
                    score = self.calculate_heatmap_score(x, y, size, orientation)
                    if score > best_score:
                        best_score = score
                        best_position = (x, y)
        return best_position

    def calculate_heatmap_score(self, x: int, y: int, size: int, orientation: str) -> int:
        score = 0
        for i in range(size):
            if orientation == 'horizontal':
                score += self.heatmap[y][x + i]
            else:
                score += self.heatmap[y + i][x]
        return score

    def update_dynamic_matrix(self) -> None:
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if not self.shots_fired[y][x]:
                    self.dynamic_matrix[y][x] = self.calculate_score(x, y)
                else:
                    self.dynamic_matrix[y][x] = -1

    def calculate_score(self, x: int, y: int) -> int:
        max_distance = min(x, self.grid_size - x - 1, y, self.grid_size - y - 1)
        return max_distance

    def find_best_shot(self) -> Tuple[int, int]:
        self.update_dynamic_matrix()
        max_score = max(max(row) for row in self.dynamic_matrix)
        best_options = [(y, x) for y in range(self.grid_size) for x in range(self.grid_size) if self.dynamic_matrix[y][x] == max_score]
        return random.choice(best_options)

    def mark_shot(self, x: int, y: int, hit: bool = False) -> None:
        self.shots_fired[y][x] = True
        if hit:
            self.heatmap[y][x] = 0  # Optionally, adjust heatmap based on hits

    def make_move(self) -> Tuple[int, int]:
        best_shot = self.find_best_shot()
        self.mark_shot(best_shot[1], best_shot[0])
        return best_shot

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
                if isinstance(cell, str) and cell == 'S':  # Check for unhit ship parts
                    return False
        return True

def process_ai_attack(screen,ai_player: AI, player_board) -> None:
    ai_move = ai_player.make_move()
    x, y = ai_move
    cell = player_board.grid[y][x]
    if cell == 'S':
        print(f"AI hit at {chr(y + 65)}{x + 1}!")
        player_board.grid[y][x] = 'X'
        ai_player.mark_shot(x, y, hit=True)
        show_attack_result_popup(screen, "AI hit a boat!", duration=2)
    else:
        print(f"AI miss at {chr(y + 65)}{x + 1}.")
        player_board.grid[y][x] = 'O'
        ai_player.mark_shot(x, y, hit=False)
        show_attack_result_popup(screen, "AI hit water!", duration=2)

# Create an instance of AI to initialize the board and place ships
ai_player = AI()
ai_player.place_ships([5, 4, 3, 2])
