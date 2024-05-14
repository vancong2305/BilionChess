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
        self.text2_color = (193, 255, 193)
        self.name = None

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
        # Tạo một đối tượng văn bản
        # Tạo font cho văn bản
        self.font1 = pygame.font.Font(None, 14)
        self.font2 = pygame.font.Font(None, 17)
        # Vẽ văn bản "Hp: <giá trị hiện tại của thanh máu>" ở giữa thanh máu

        text1 = self.font1.render("Hp: " + str(self.current_health), True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(self.x + self.width // 2, self.y - self.height // 2))
        screen.blit(text1, text1_rect)

        # Vẽ văn bản "Tên: <tên>" ở giữa thanh máu
        text2 = self.font2.render("Tên: " + str(self.name), True, self.text2_color)
        text2_rect = text2.get_rect(center=(self.x + self.width // 2, self.y - self.height // 2 - 10))
        screen.blit(text2, text2_rect)