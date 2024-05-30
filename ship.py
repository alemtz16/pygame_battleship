import pygame
import logging
from settings import CELL_SIZE, CELL_SIZE2

class Ship:
    def __init__(self, name, size, orientation, start_position, image_path, start_cell_position):
        self.name = name
        self.size = size
        self.selected = False
        self.orientation = orientation
        self.image_path = image_path
        self.start_position = start_position
        self.image = pygame.image.load(image_path)
        self.start_cell_position = start_cell_position
        self.rect = self.image.get_rect(topleft=start_position)
        self.dragging = False

        self.update_image(CELL_SIZE2)

    def update_image(self, cell_size):
        logging.debug(f"Updating image for {self.name} with orientation {self.orientation}")
        if self.orientation == 'horizontal':
            width = cell_size * self.size
            height = cell_size
        else:
            width = cell_size
            height = cell_size * self.size

        original_image = pygame.image.load(self.image_path)
        if self.orientation == 'vertical':
            original_image = pygame.transform.rotate(original_image, -90)  # Rotar la imagen 90 grados para orientación vertical
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect(topleft=self.start_position)
        logging.debug(f"Image updated for {self.name}: {self.rect}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_position(self, cell_position, cell_size):
        self.rect.topleft = (cell_position[0] * cell_size, cell_position[1] * cell_size)
        occupied_positions = []
        if self.orientation == 'horizontal':
            for i in range(self.size):
                occupied_positions.append((cell_position[0] + i, chr(cell_position[1] + 65)))
        else:
            for i in range(self.size):
                occupied_positions.append((cell_position[0], chr(cell_position[1] + i + 65)))
        logging.debug(f"{self.name} updated positions: {occupied_positions}")

    def get_occupied_positions(self):
        cell_x = self.rect.topleft[0] // CELL_SIZE2
        cell_y = self.rect.topleft[1] // CELL_SIZE2
        occupied_positions = []

        for i in range(self.size):
            if self.orientation == 'horizontal':
                occupied_positions.append((cell_x + i, chr(cell_y + 65-2)))
            else:
                occupied_positions.append((cell_x, chr(cell_y + i + 65-2)))

        logging.debug(f"{self.name} positions: {occupied_positions}")
        return occupied_positions

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
                logging.debug(f"Before orientation change: {self.orientation}")
                self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
                logging.debug(f"After orientation change: {self.orientation}")
                self.update_image(CELL_SIZE2)
