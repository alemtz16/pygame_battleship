import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2

class Ship:
    def __init__(self, name, size, orientation, start_position, image_path,start_cell_position ):
        self.name = name
        self.size = size
        self.selected= False
        self.orientation = orientation
        self.image_path = image_path
        self.start_position = start_position
        self.image = pygame.image.load(image_path)
        self.start_cell_position = start_cell_position
        self.rect = self.image.get_rect(topleft=start_position)
        self.dragging = False
        
        self.update_image(CELL_SIZE2)
 

    def update_image(self, cell_size):
        width = cell_size if self.orientation == 'horizontal' else cell_size * self.size
        height = cell_size * self.size if self.orientation == 'horizontal' else cell_size
        original_image = pygame.image.load(self.image_path)
        if self.orientation == 'vertical':
            original_image = pygame.transform.rotate(original_image, -90)  # Rotate the image by -90 degrees for vertical orientation
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect(topleft=self.start_position)

    def update_position(self, cell_position, cell_size):
        # Convert cell position to pixel coordinates
        self.rect.topleft = (cell_position[0] * cell_size, cell_position[1] * cell_size)

        # Log the occupied positions in board terms
        occupied_positions = []
        if self.orientation == 'horizontal':
            for i in range(self.size):
                occupied_positions.append((cell_position[0] + i, cell_position[1]))
        else:
            for i in range(self.size):
                occupied_positions.append((cell_position[0], cell_position[1] + i))

        logging.debug(f"{self.name}: {occupied_positions}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
 

    def handle_mouse_event(self, event, ships):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.selected = True
                self.mouse_offset = pygame.Vector2(self.rect.topleft) - event.pos
 
                for ship in ships:
                    if ship != self:
                        ship.selected = False


        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
 
                self.start_position = self.rect.topleft
 

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.topleft = event.pos + self.mouse_offset
 
    
    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # Flip the orientation of the ship vertically
                self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
                self.update_image(CELL_SIZE2 if self.orientation == 'horizontal' else CELL_SIZE2)