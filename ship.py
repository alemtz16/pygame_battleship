import pygame
import logging
from settings import CELL_SIZE, BLACK

class Ship:
    def __init__(self, name, size, orientation, start_position, image_path=None):
        self.name = name
        self.size = size
        self.orientation = orientation
        self.dragging = False

        # Adjust dimensions based on orientation
        if orientation == 'horizontal':
            self.width = CELL_SIZE * size
            self.height = CELL_SIZE  
        else:
            self.width = CELL_SIZE
            self.height = CELL_SIZE * size

        # Convert start_position from grid coordinates to pixel coordinates
        self.rect = pygame.Rect(start_position[0] * CELL_SIZE, start_position[1] * CELL_SIZE, self.width, self.height)

        # Attempt to load an image if a path is provided
        self.image = None
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                logging.debug(f"Image loaded for {self.name} from {image_path}")
            except Exception as e:
                logging.error(f"Error loading image for {self.name}: {e}")
                self.image = None  # Ensure image is None if loading fails

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset_x = event.pos[0] - self.rect.x
                self.drag_offset_y = event.pos[1] - self.rect.y
                logging.debug(f"Started dragging {self.name} from {self.rect.topleft}")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                # Snap to the nearest grid position upon release
                self.rect.x = round(self.rect.x / CELL_SIZE) * CELL_SIZE
                self.rect.y = round(self.rect.y / CELL_SIZE) * CELL_SIZE
                logging.debug(f"Stopped dragging {self.name}; snapped to grid at {self.rect.topleft}")
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update position while dragging
            self.rect.x = event.pos[0] - self.drag_offset_x
            self.rect.y = event.pos[1] - self.drag_offset_y
            logging.debug(f"Dragging {self.name} to {self.rect.topleft}")

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            # Draw a filled rectangle with a border if no image is available
            pygame.draw.rect(screen, BLACK, self.rect, 1)  # Draw outline
            pygame.draw.rect(screen, (70, 70, 70), self.rect)  # Fill with gray for visibility

