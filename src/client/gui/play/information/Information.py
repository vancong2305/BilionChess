import os
import pygame

from src.client.RootProgram import RootProgram
from src.client.gui.parameter.Para import Para


class Information:
    infomation = None
    screen = None
    def __init__(self):
        self.turn = 0
        self.remaining_time = 0  # Total time in seconds for the current turn

        root_path = RootProgram().get_root_path()
        font_path = os.path.join(root_path, "resource", "font", "Arial.ttf")
        self.font = pygame.font.Font(font_path, 18)

    def set_turn(self, turn):
        self.turn = turn
        self.remaining_time = 0  # Reset remaining time for new turn

    def set_time(self, time_in_seconds):
        self.remaining_time = time_in_seconds

    def update(self):
        """
        Decrements the remaining time if it's greater than zero.
        """
        if self.remaining_time > 0:
            self.remaining_time -= 1

    def draw(self, screen):
        # Top left label (assuming specific text)
        top_left_text = "Bạn: 1000$"
        top_left_surface = self.font.render(top_left_text, True, (255,255,0))
        top_left_rect = top_left_surface.get_rect(topleft=(5, 5))
        screen.blit(top_left_surface, top_left_rect)

        # Top right label (assuming specific text)
        top_right_text = "Đối thủ: 2000$"
        top_right_surface = self.font.render(top_right_text, True, (255,255,0))
        top_right_rect = top_right_surface.get_rect(topright=(screen.get_width() - 5, 5))
        screen.blit(top_right_surface, top_right_rect)

        # Center label (already defined in your previous code)
        turn_message = (
            "Lượt của bạn, kết thúc trong: " if self.turn == 0 else "Lượt của đối thủ, kết thúc trong: "
        )
        label2_surface = self.font.render(turn_message + str(self.remaining_time) + " giây", True, (0, 0, 0))
        label_width, label_height = label2_surface.get_size()
        center_x = screen.get_width() // 2
        center_y = Para.SIZE // 5
        label2_rect = label2_surface.get_rect(center=(center_x, center_y))
        screen.blit(label2_surface, label2_rect)

