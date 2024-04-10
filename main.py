import pygame
from menu import Menu
from settings import screen_width, screen_height
from board import Board

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battleship')

# Initialize menu and board
menu = Menu(screen)
board = Board()

# Game state
is_menu = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Event handling for the menu
        if is_menu:
            menu.handle_event(event)
    
    # Drawing
    screen.fill((0, 0, 0))  # Fill the screen with black or some background
    if is_menu:
        menu.draw()  # Draw the menu
    else:
        board.draw(screen)  # Draw the game board

    pygame.display.flip()

pygame.quit()
