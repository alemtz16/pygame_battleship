import pygame

class Button:
    def __init__(self, screen, text, pos, size, color, highlight_color, font_size=30):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.highlight_color = highlight_color
        self.font_size = font_size
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, font_size)
        self.text_surf = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            return True
        return False

class TextInput:
    def __init__(self, screen, initial_text, pos, size, font_size=30):
        self.screen = screen
        self.text = initial_text
        self.pos = pos
        self.size = size
        self.font_size = font_size
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # or do something more useful
                    self.text = ''  # Reset text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self):
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        width = max(200, text_surf.get_width()+10)
        self.rect.w = width
        self.screen.blit(text_surf, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
