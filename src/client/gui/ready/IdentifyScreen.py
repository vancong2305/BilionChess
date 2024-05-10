import os

import pygame
from pygame.locals import *

from src.client.gui.room.WelcomeScreen import WelcomeScreen


class IdentifyScreen:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Xác thực người chơi")
        self.screen = pygame.display.set_mode((400, 300))
        self.clock = pygame.time.Clock()
        self.name_input = NameInput(40, 125, 320, 50)
        font_path = os.path.join(os.path.dirname(__file__), "Arial.ttf")
        self.confirm_button = Button(150, 200, 100, 40, "Xác nhận")
        self.label_font = pygame.font.Font(font_path, 22)
        self.label_text = self.label_font.render("Mời bạn nhập tên hiển thị", True, (255, 255, 255))
        self.caption = "My Screen"
        self.running = False

    def get_name_input_content(self):
        return self.name_input.text
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                self.name_input.handle_event(event)
                self.confirm_button.handle_event(event)
            self.screen.fill((0, 80, 110))
            label_x = (self.screen.get_width() - self.label_text.get_width()) // 2
            label_y = 80
            self.screen.blit(self.label_text, (label_x, label_y))
            self.name_input.draw(self.screen)
            self.confirm_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


#Sub class
class NameInput:
    text = ''
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        font_path = os.path.join(os.path.dirname(__file__), "Arial.ttf")
        self.font = pygame.font.Font(font_path, 32)
        self.text = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem chuột có được nhấn vào vùng nhập tên hay không
            if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            # Nhập ký tự vào vùng nhập tên
            if self.active:
                if event.key == pygame.K_RETURN:
                    print("Tên đã được nhập:", self.text)
                    NameInput.text = self.text
                    pygame.quit()
                    WelcomeScreen(NameInput.text).run()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    NameInput.text = self.text
                else:
                    self.text += event.unicode
                    NameInput.text = self.text

    def draw(self, screen):
        # Vẽ hình chữ nhật vùng nhập tên
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
        # Vẽ văn bản nhập tên
        # Vẽ văn bản nhập tên
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        font_path = os.path.join(os.path.dirname(__file__), "Arial.ttf")
        self.font = pygame.font.Font(font_path, 20)
        self.text = text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem chuột có được nhấn vào nút hay không
            if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                text = NameInput.text
                pygame.quit()
                WelcomeScreen(text).run()
                # RoomListScreen().run()

    def print_input_content(self):
        self.screen.print_input_content()
    def draw(self, screen):
        # Vẽ hình chữ nhật nút
        pygame.draw.rect(screen, (50, 110, 120), (self.x, self.y, self.width, self.height))
        # Vẽ văn bản nút
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

