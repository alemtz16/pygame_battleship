import random
 


class AI:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.dynamic_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.shots_fired = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.high_scores = []

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


ai_player = AI()
next_move = ai_player.make_move()
 
