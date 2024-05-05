import pygame
from pygame.locals import *
class ErrorMenu:
    def __init__(self, message, x, y, width, height):
        self.message = message
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font("./Arial.ttf", 24)
        self.visible = False  # Cờ để theo dõi trạng thái hiển thị

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_x = self.x + (self.width - text_surface.get_width()) // 2
            text_y = self.y + (self.height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))