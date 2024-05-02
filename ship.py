
import pygame
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Now you can use logging.debug(), logging.info(), logging.warning(), etc., to log messages.

from settings import CELL_SIZE, BLACK

class Ship:
    def __init__(self, name, size, orientation='horizontal', start_position=(0, 0), image_path=None):
        """
        Inicializa un barco con un tamaño específico, una orientación y una posición de inicio.
        """
       
        self.name = name
        self.size = size 
        self.orientation = orientation  
        self.start_position = start_position 
        self.dragging = False 
        width = self.size * CELL_SIZE if orientation == 'horizontal' else CELL_SIZE
        height = CELL_SIZE if orientation == 'horizontal' else self.size * CELL_SIZE
        self.rect = pygame.Rect(start_position[0], start_position[1], width, height)  # Update dimensions based on orientation
        logging.debug(f"Initialized {self.name} at {self.rect.topleft}")
        self.cell_size = CELL_SIZE  # Assuming CELL_SIZE is globally defined
        self.update_dimensions(start_position)
        
        try:
            if image_path:
                self.image = pygame.image.load(image_path)
                if self.orientation == 'horizontal':
                    scale = (self.size * CELL_SIZE, CELL_SIZE)
                else:
                    scale = (CELL_SIZE, self.size * CELL_SIZE)
                self.image = pygame.transform.scale(self.image, scale)  
              
        except Exception as e:
         
            self.image = None  

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset_x = self.rect.x - event.pos[0]
                self.drag_offset_y = self.rect.y - event.pos[1]
                logging.debug(f"{self.name} dragging started at {event.pos}")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                self.rect.x = round((self.rect.x + self.drag_offset_x) / CELL_SIZE) * CELL_SIZE
                self.rect.y = round((self.rect.y + self.drag_offset_y) / CELL_SIZE) * CELL_SIZE
                logging.debug(f"{self.name} stopped dragging; snapped to grid at {self.rect.topleft}")
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.x = event.pos[0] + self.drag_offset_x
            self.rect.y = event.pos[1] + self.drag_offset_y
            logging.debug(f"{self.name} is being dragged to {self.rect.topleft}")




    def move_to(self, new_position):
        self.start_position = new_position
        self.rect.topleft = new_position

    def rotate(self):
        """
        Rotates the ship between horizontal and vertical orientations.
        """
        self.orientation = 'horizontal' if self.orientation == 'vertical' else 'vertical'

    def update_rect(self, cell_size):
        """
        Updates the ship's rectangle based on its position and orientation.
        """
        width = cell_size if self.orientation == 'vertical' else self.size * cell_size
        height = self.size * cell_size if self.orientation == 'vertical' else cell_size
        self.rect = pygame.Rect(self.start_position[0] * cell_size, self.start_position[1] * cell_size, width, height)

    def get_positions(self):
        """
        Returns a list of positions occupied by the ship based on its size, orientation, and start position.
        """
        positions = []
        if self.orientation == 'horizontal':
           
            positions = [(self.start_position[0] + i * 20, self.start_position[1]) for i in range(self.size)]
        else:
            
            positions = [(self.start_position[0], self.start_position[1] + i * 20) for i in range(self.size)]
        return positions

    def is_within_bounds(self, board_rect):
        """
        Verifica si el barco está completamente dentro de los límites del tablero.
        """
        return board_rect.contains(self.rect)

    def rotate(self):
        """
        Rota el barco entre orientación horizontal y vertical.
        """
        if self.orientation == 'horizontal':
            self.orientation = 'vertical'
            self.rect.size = (20, self.size * 20)  
        else:
            self.orientation = 'horizontal'
            self.rect.size = (self.size * 20, 20)  

       
        self.rect.center = self.start_position

    def move_to(self, new_position):
        """
        Mueve el barco a una nueva posición.
        """
        self.start_position = new_position
        self.rect.topleft = new_position

    def update_dimensions(self, start_position):
        width = self.size * self.cell_size if self.orientation == 'horizontal' else self.cell_size
        height = self.cell_size if self.orientation == 'horizontal' else self.size * self.cell_size
        self.rect = pygame.Rect(start_position[0] * self.cell_size, start_position[1] * self.cell_size, width, height)
  
    def draw(self, screen):
      
        screen_x = self.start_position[0] * CELL_SIZE
        screen_y = self.start_position[1] * CELL_SIZE

      
        base_height = CELL_SIZE 

        if self.image:
           
            scale_width = CELL_SIZE

           
            scale_height = base_height * self.size 

     
            scaled_image = pygame.transform.scale(self.image, (scale_width, scale_height))

           
            screen.blit(scaled_image, (screen_x, screen_y))
        else:

            rect_width = self.size * CELL_SIZE
            rect_height = base_height * self.size  
            pygame.draw.rect(screen, BLACK, (screen_x, screen_y, rect_width, rect_height))

    def update(self, events):
        """
        Maneja la lógica de arrastrar y soltar.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(pygame.mouse.get_pos()): 
                    self.dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False 

        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()
