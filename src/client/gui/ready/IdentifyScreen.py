import os

import pygame
from pygame.locals import *

from src.client.gui.parameter.Connect import Connect
from src.client.gui.room.WelcomeScreen import WelcomeScreen
from src.client.handle.NameRequest import NameRequest


class IdentifyScreen:
    name = None
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Xác thực người chơi")
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        font_path = os.path.join(os.path.dirname(__file__), "Arial.ttf")
        self.confirm_button = Button(screen_width/2-100/2, screen_height/2+40, 100, 40, "Xác nhận")
        self.label_font = pygame.font.Font(font_path, 44)
        self.label_text = self.label_font.render("Tên hiển thị của bạn là: " + Connect.ID.__str__(), True, (255, 255, 255))
        self.caption = "My Screen"
        self.running = False

    def get_name_input_content(self):
        return self.name_input.text
    async def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                        exit(0)
                await self.confirm_button.handle_event(event)
            self.screen.fill((0, 80, 110))
            label_x = (self.screen.get_width() - self.label_text.get_width()) // 2
            label_y = self.screen.get_height()/2 - 150
            self.screen.blit(self.label_text, (label_x, label_y))
            self.confirm_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        font_path = os.path.join(os.path.dirname(__file__), "Arial.ttf")
        self.font = pygame.font.Font(font_path, 20)
        self.text = text

    async def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                pygame.quit()
                await NameRequest().create_user(Connect.ID.__str__())
                await WelcomeScreen(Connect.ID.__str__()).run()
    def print_input_content(self):
        self.screen.print_input_content()
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 110, 120), (self.x, self.y, self.width, self.height))
        # Vẽ văn bản nút
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

