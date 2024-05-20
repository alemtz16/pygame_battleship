import pygame
import logging

class Ship:
    def __init__(self, name, size, orientation, start_position, image_path):
        self.name = name
        self.size = size
        self.orientation = orientation
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=start_position)
        self.dragging = False
        logging.debug(f"Image loaded for {name} from {image_path}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        logging.debug(f"Drawing ship {self.name} at {self.rect.topleft}")

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_offset = pygame.Vector2(self.rect.topleft) - event.pos
                logging.debug(f"{self.name} selected for dragging")

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                logging.debug(f"{self.name} dropped at {self.rect.topleft}")

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.topleft = event.pos + self.mouse_offset
                logging.debug(f"{self.name} moved to {self.rect.topleft}")