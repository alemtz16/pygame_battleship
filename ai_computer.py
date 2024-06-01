import random

class AI:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.dynamic_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.shots_fired = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.high_scores = []
        self.ships = []
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        self.heatmap = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.init_heatmap()

    def init_heatmap(self):
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
    
    def place_ships(self, ship_sizes):
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    x, y = self.find_best_position(size, orientation)
                else:
                    x, y = self.find_best_position(size, orientation)

                if self.can_place_ship(x, y, size, orientation):
                    self.ships.append((x, y, size, orientation))
                    for i in range(size):
                        if orientation == 'horizontal':
                            self.grid[y][x + i] = 'S'
                        else:
                            self.grid[y + i][x] = 'S'
                    placed = True
        self.print_grid()

    def find_best_position(self, size, orientation):
        min_heat = float('inf')
        best_position = (0, 0)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.can_place_ship(x, y, size, orientation):
                    heat = self.calculate_heat(x, y, size, orientation)
                    if heat < min_heat:
                        min_heat = heat
                        best_position = (x, y)
        return best_position

    def calculate_heat(self, x, y, size, orientation):
        heat = 0
        for i in range(size):
            if orientation == 'horizontal':
                heat += self.heatmap[y][x + i]
            else:
                heat += self.heatmap[y + i][x]
        return heat

    def can_place_ship(self, x, y, size, orientation):
        for i in range(size):
            if orientation == 'horizontal':
                if x + i >= self.grid_size or self.grid[y][x + i] != '':
                    return False
            else:
                if y + i >= self.grid_size or self.grid[y + i][x] != '':
                    return False
        return True

    def get_ship_positions(self):
        ship_positions = []
        for ship in self.ships:
            x, y, size, orientation = ship
            positions = []
            for i in range(size):
                if orientation == 'horizontal':
                    positions.append((x + i, y))
                else:
                    positions.append((x, y + i))
            ship_positions.append(positions)
        return ship_positions

    def print_grid(self):
        for row in self.grid:
            print(' '.join(['S' if cell == 'S' else '.' for cell in row]))

    def update_dynamic_matrix(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if not self.shots_fired[y][x]:
                    self.dynamic_matrix[y][x] = self.calculate_score(x, y)
                else:
                    self.dynamic_matrix[y][x] = -1

    def calculate_score(self, x, y):
        max_distance = min(x, self.grid_size - x - 1, y, self.grid_size - y - 1)
        return max_distance

    def find_best_shot(self):
        self.update_dynamic_matrix()
        max_score = max(max(row) for row in self.dynamic_matrix)
        best_options = [(y, x) for y in range(self.grid_size) for x in range(self.grid_size) if self.dynamic_matrix[y][x] == max_score]
        return random.choice(best_options)

    def mark_shot(self, x, y, hit=False):
        self.shots_fired[y][x] = True
        if hit:
            pass

    def make_move(self):
        best_shot = self.find_best_shot()
        self.mark_shot(best_shot[1], best_shot[0])
        return best_shot

def process_ai_attack(ai_player, player_board):
    ai_move = ai_player.make_move()
    x, y = ai_move
    cell = player_board.grid[y][x]
    if cell:
        print(f"AI hit at {chr(y + 65)}{x + 1}!")
        player_board.grid[y][x] = 'X'
        ai_player.mark_shot(x, y, hit=True)
    else:
        print(f"AI miss at {chr(y + 65)}{x + 1}.")
        player_board.grid[y][x] = 'O'
        ai_player.mark_shot(x, y, hit=False)

# Create an instance of AI to initialize the board and place ships
ai_player = AI()
next_move = ai_player.make_move()
