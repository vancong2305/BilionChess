import pygame

GREEN = (0, 255, 0)  # Màu xanh lá cây
RED = (255, 0, 0)  # Màu đỏ

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health

    def decrease_health(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def draw(self, screen):
        # Vẽ thanh máu đầy đủ (màu đỏ)
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Tính toán chiều dài của thanh máu dựa trên giá trị hiện tại
        current_health_width = int((self.current_health / self.max_health) * self.width)
        # Vẽ thanh máu dựa trên giá trị hiện tại và màu xanh
        pygame.draw.rect(screen, GREEN, (self.x, self.y, current_health_width, self.height))