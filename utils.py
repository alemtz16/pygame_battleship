

import pygame
import os


def load_image(image_path, scale=None):
    """
    Carga una imagen desde el camino especificado. 
    Si 'scale' es proporcionado, la imagen se ajustará a esas dimensiones.
    """
    image = pygame.image.load(image_path)
    if scale:
        image = pygame.transform.scale(image, scale) 
    return image



def load_sound(sound_path):
    """
    Carga un sonido desde el camino especificado.
    """
    sound = pygame.mixer.Sound(sound_path)  
    return sound



def detect_collision(rect1, rect2):
    """
    Devuelve True si 'rect1' y 'rect2' se superponen, False en caso contrario.
    """
    return rect1.colliderect(rect2) 



def draw_text(screen, text, font, color, position):
    """
    Dibuja texto en la pantalla en la posición dada.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position) 
    screen.blit(text_surface, text_rect) 



def get_relative_path(relative_path):
    """
    Retorna la ruta relativa basada en el directorio actual del archivo.
    """
    base_path = os.path.dirname(__file__) 
    return os.path.join(base_path, relative_path)  
