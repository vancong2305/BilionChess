import os
import pygame
from pygame.locals import *
from pathlib import Path


class RoomScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.caption = "Room Screen"
        self.running = False

        # Lấy đường dẫn gốc tới thư mục gui, gui là cha của room, ở tệp này
        project_root = Path(__file__).parent.parent
        font_path = project_root / 'ready' / 'Arial.ttf'

        # Tạo font cho các nút và hiển thị phòng
        self.button_font = pygame.font.Font(font_path, 24)  # Kích thước font tùy chỉnh
        self.room_font = pygame.font.Font(font_path, 36)  # Font hiển thị phòng

        # Tạo các nút
        self.greeting_button = Button(50, 50, 200, 50, "Xin chào + xyz", self.button_font)
        self.create_room_button = Button(50, 150, 200, 50, "Tạo phòng", self.button_font)
        self.refresh_button = Button(50, 250, 200, 50, "Làm mới phòng", self.button_font)

        # Danh sách phòng trống
        self.empty_rooms = ["Phòng 1", "Phòng 2", "Phòng 3"]

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                self.greeting_button.handle_event(event)
                self.create_room_button.handle_event(event)
                self.refresh_button.handle_event(event)

            self.screen.fill((255, 255, 255))  # Màu nền của màn hình Room

            # Hiển thị nút "Xin chào + xyz"
            self.greeting_button.draw(self.screen)

            # Hiển thị nút "Tạo phòng"
            self.create_room_button.draw(self.screen)

            # Hiển thị nút "Làm mới phòng"
            self.refresh_button.draw(self.screen)

            # Hiển thị danh sách phòng trống
            self.display_empty_rooms()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def display_empty_rooms(self):
        text = self.room_font.render("Danh sách phòng trống:", True, (0, 0, 0))
        self.screen.blit(text, (300, 50))
        y = 100
        for room in self.empty_rooms:
            room_text = self.room_font.render(room, True, (0, 0, 0))
            self.screen.blit(room_text, (300, y))
            y += 50


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font  # Sử dụng font được truyền vào

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                print("Nút", self.text, "đã được nhấn")

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 120, 200), (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)