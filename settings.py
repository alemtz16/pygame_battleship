# Game screen dimensions
screen_width = 800
screen_height = 600

# Colors (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
gray = (200, 200, 200)
red = (255, 0, 0)

# Game settings
grid_size = 10  # 10x10 grid
cell_size = 40  # Each cell is 40x40 pixels
board_offset = (100, 100)  # Offset from the top-left corner to start drawing the game board

# Ship settings
# Define ships as a list of lengths. For example, a standard Battleship game setup:
# 1 ship of length 5 (Carrier), 1 of length 4 (Battleship), 2 of length 3 (Cruiser and Submarine), and 1 of length 2 (Destroyer).
ships_lengths = [5, 4, 3, 3, 2]

# AI Settings
# Adjust these settings based on the difficulty level you wish to implement for your AI.
ai_difficulty = 'medium'  # Options could include 'easy', 'medium', 'hard'.
