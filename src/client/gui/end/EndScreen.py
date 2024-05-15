import pygame
import sys
import os

from src.client.RootProgram import RootProgram
from src.client.gui.parameter.Connect import Connect


class Endscreen:
    def __init__(self, reason):
        pygame.init()
        self.reason = reason
        # Kích thước cửa sổ và màu nền
        self.width, self.height = 800, 600
        self.background_color = (190, 190, 190)

        # Tạo cửa sổ
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Màn hình kết quả của ' + Connect.ID.__str__())

        # Font chữ
        root_path = RootProgram().get_root_path()
        font_path = os.path.join(root_path, "resource", "font", "Arial.ttf")
        self.font = pygame.font.Font(font_path, 20)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Xóa màn hình
            self.screen.fill(self.background_color)

            # Tạo danh sách các dòng văn bản
            max_line_length = 20
            lines = []
            current_line = ""
            words = self.reason.split()

            for word in words:
                if len(current_line) + len(word) <= max_line_length:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "

            if current_line:
                lines.append(current_line.strip())

            # Vẽ văn bản lên màn hình
            y = self.height // 2 - len(lines) * self.font.get_height() // 2
            for line in lines:
                text = self.font.render(line, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.width // 2, y))
                self.screen.blit(text, text_rect)
                y += self.font.get_height()

            # Cập nhật màn hình
            pygame.display.flip()

        pygame.quit()
        sys.exit()