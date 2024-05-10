import pygame

from src.client.gui.parameter.Para import Para


class Roll:
    def __init__(self):
        self.button_rect = None

    def draw(self, screen):
        button_width = 90
        button_height = 35
        button_x = Para.WIDTH // 2 - button_width // 2 - 3
        button_y = Para.HEIGHT // 2 + Para.SIZE * 1.2 - button_height // 2

        self.button_rect = pygame.Rect(button_x, button_y + 70, button_width, button_height)
        corner_radius = 16  # Adjust the radius as desired
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect, border_radius=corner_radius)

        font = pygame.font.Font(None, 25)
        text = font.render("Quay", True, (255, 127, 0))
        text_rect = text.get_rect(center=self.button_rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, mouse_pos):
        if self.button_rect is not None:
            return self.button_rect.collidepoint(mouse_pos)
        return False