import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2

class Ship:
    def __init__(self, name, size, orientation, start_position, image_path):
        self.name = name
        self.size = size
        self.selected= False
        self.orientation = orientation
        self.image_path = image_path
        self.start_position = start_position
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=start_position)
        self.dragging = False
        self.update_image(CELL_SIZE2)
        logging.debug(f"Image loaded for {name} from {image_path}")

    def update_image(self, cell_size):
        width = cell_size if self.orientation == 'horizontal' else cell_size * self.size
        height = cell_size * self.size if self.orientation == 'horizontal' else cell_size
        original_image = pygame.image.load(self.image_path)
        if self.orientation == 'vertical':
            original_image = pygame.transform.rotate(original_image, -90)  # Rotate the image by -90 degrees for vertical orientation
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect(topleft=self.start_position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        logging.debug(f"Drawing ship {self.name} at {self.rect.topleft}")

    def handle_mouse_event(self, event, ships):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.selected = True
                self.mouse_offset = pygame.Vector2(self.rect.topleft) - event.pos
                logging.debug(f"{self.name} selected for dragging")
                for ship in ships:
                    if ship != self:
                        ship.selected = False


        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                logging.debug(f"{self.name} dropped at {self.rect.topleft}")
 

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.topleft = event.pos + self.mouse_offset
                logging.debug(f"{self.name} moved to {self.rect.topleft}")
    
    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # Flip the orientation of the ship vertically
                self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
                self.update_image(CELL_SIZE2 if self.orientation == 'horizontal' else CELL_SIZE2)