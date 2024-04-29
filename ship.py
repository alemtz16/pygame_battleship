
import pygame

from settings import CELL_SIZE, BLACK

class Ship:
    def __init__(self, name, size, orientation='horizontal', start_position=(0, 0), image_path=None):
        """
        Inicializa un barco con un tamaño específico, una orientación y una posición de inicio.
        """
        print(f"Initializing ship: {name}, size: {size}, orientation: {orientation}, start_position: {start_position}")
        self.name = name
        self.size = size 
        self.orientation = orientation  
        self.start_position = start_position 
        self.dragging = False 
        width = self.size * CELL_SIZE if orientation == 'horizontal' else CELL_SIZE
        height = CELL_SIZE if orientation == 'horizontal' else self.size * CELL_SIZE
        self.rect = pygame.Rect(start_position, (width, height)) 
       
        try:
            if image_path:
                self.image = pygame.image.load(image_path)
                if self.orientation == 'horizontal':
                    scale = (self.size * CELL_SIZE, CELL_SIZE)
                else:
                    scale = (CELL_SIZE, self.size * CELL_SIZE)
                self.image = pygame.transform.scale(self.image, scale)  
                print(f"Image loaded for {self.name} from {image_path}")
        except Exception as e:
            print(f"Error loading image for {self.name}: {e}")
            self.image = None  


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
