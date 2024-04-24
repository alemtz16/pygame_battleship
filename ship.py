# Define la clase para los barcos y su comportamiento.
import pygame

class Ship:
    def __init__(self, name, size, orientation='horizontal', start_position=(0, 0), image_path=None):
        """
        Inicializa un barco con un tamaño específico, una orientación y una posición de inicio.
        """
        self.name = name
        self.size = size  # Tamaño del barco (por ejemplo, 2 para un destructor)
        self.orientation = orientation  # Orientación ('horizontal' o 'vertical')
        self.start_position = start_position  # Posición inicial (x, y)
        self.dragging = False  # Controla si el barco está siendo arrastrado

        # Cargar la imagen si se proporciona un camino
        if image_path:
            self.image = pygame.image.load(image_path)
            self.rect = self.image.get_rect(center=start_position)  # Bounding box
        else:
            # Crear un rectángulo predeterminado según la orientación
            width = size * 20 if orientation == 'horizontal' else 20
            height = 20 if orientation == 'horizontal' else size * 20
            self.rect = pygame.Rect(start_position, (width, height))

    def get_positions(self):
        """
        Retorna una lista de posiciones ocupadas por el barco basado en su tamaño, orientación y posición inicial.
        """
        if self.orientation == 'horizontal':
            # Genera posiciones horizontales
            return [(self.rect.left + i * 20, self.rect.top) for i in range(self.size)]
        else:
            # Genera posiciones verticales
            return [(self.rect.left, self.rect.top + i * 20) for i in range(self.size)]

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
            self.rect.size = (20, self.size * 20)  # Ajustar tamaño del rectángulo
        else:
            self.orientation = 'horizontal'
            self.rect.size = (self.size * 20, 20)  # Ajustar tamaño del rectángulo

        # Mantener la posición actual en el centro del nuevo tamaño
        self.rect.center = self.start_position

    def move_to(self, new_position):
        """
        Mueve el barco a una nueva posición.
        """
        self.start_position = new_position
        self.rect.topleft = new_position

    def draw(self, screen):
        """
        Dibuja el barco en la pantalla.
        """
        if hasattr(self, 'image'):
            screen.blit(self.image, self.rect.topleft)  # Dibujar la imagen
        else:
            # Dibujar un rectángulo simple si no hay imagen
            pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Color blanco

    def update(self, events):
        """
        Maneja la lógica de arrastrar y soltar.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(pygame.mouse.get_pos()):  # Clic izquierdo
                    self.dragging = True  # Comienza a arrastrar

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False  # Dejar de arrastrar

        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()  # Mover con el mouse
