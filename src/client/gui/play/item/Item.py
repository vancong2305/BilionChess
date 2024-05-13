import os
import time

import pygame
from pygame import QUIT

from src.client.RootProgram import RootProgram
from src.client.gui.parameter.Para import Para
from src.client.gui.play.figure.HealthBar import HealthBar
from src.client.gui.play.figure.Store import Store
from src.client.gui.play.map.Map import Map
import cv2

class Item:
    animation_interval = 100
    current_image_index = 0
    position_x = 50
    position_y = 50
    player_one = None
    player_two = None
    state = 'idle'
    screen = None
    item1 = None
    item2 = None
    item3 = None
    item4 = None
    listItem = []
    def __init__(self, character_type):
        self.character_type = character_type
        self.action = "idle"  # Hành động mặc định là "idle"
        self.images = self.load_images()
        self.animation_timer = pygame.time.get_ticks()
        root_path = RootProgram().get_root_path()
        self.font_path = os.path.join(root_path, "resource", "font", "Arial.ttf")
        self.font = pygame.font.Font(self.font_path, 18)

    def load_images(self):
        image_paths = []
        if self.character_type == 2:
            if self.action == "idle":
                image_paths = [
                    "../../../resource/img/item/robot/idle/Idle_000.png",
                    "../../../resource/img/item/robot/idle/Idle_001.png",
                    "../../../resource/img/item/robot/idle/Idle_002.png",
                    "../../../resource/img/item/robot/idle/Idle_003.png",
                    "../../../resource/img/item/robot/idle/Idle_004.png",
                    "../../../resource/img/item/robot/idle/Idle_005.png",
                    "../../../resource/img/item/robot/idle/Idle_006.png",
                    "../../../resource/img/item/robot/idle/Idle_007.png"
                ]
            elif self.action == "mlee":
                image_paths = [
                    "../../../resource/img/item/robot/mlee/Mlee_000.png",
                    "../../../resource/img/item/robot/mlee/Mlee_001.png",
                    "../../../resource/img/item/robot/mlee/Mlee_002.png",
                    "../../../resource/img/item/robot/mlee/Mlee_003.png"
                ]
            elif self.action == "dead":
                image_paths = [
                    "../../../resource/img/item/robot/dead/Dead_000.png",
                    "../../../resource/img/item/robot/dead/Dead_001.png",
                    "../../../resource/img/item/robot/dead/Dead_002.png",
                    "../../../resource/img/item/robot/dead/Dead_003.png",
                    "../../../resource/img/item/robot/dead/Dead_004.png",
                    "../../../resource/img/item/robot/dead/Dead_005.png",
                    "../../../resource/img/item/robot/dead/Dead_006.png",
                    "../../../resource/img/item/robot/dead/Dead_007.png"
                ]
            # Add more cases for other actions as needed
        elif self.character_type == 3:
            if self.action == "idle":
                image_paths = [
                    "../../../resource/img/item/ninja/idle/Idle_000.png",
                    "../../../resource/img/item/ninja/idle/Idle_001.png",
                    "../../../resource/img/item/ninja/idle/Idle_002.png",
                    "../../../resource/img/item/ninja/idle/Idle_003.png",
                    "../../../resource/img/item/ninja/idle/Idle_004.png",
                    "../../../resource/img/item/ninja/idle/Idle_005.png",
                    "../../../resource/img/item/ninja/idle/Idle_006.png",
                    "../../../resource/img/item/ninja/idle/Idle_007.png"
                ]
            elif self.action == "mlee":
                image_paths = [
                    "../../../resource/img/item/ninja/mlee/Mlee_000.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_001.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_002.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_003.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_004.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_005.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_006.png",
                    "../../../resource/img/item/ninja/mlee/Mlee_007.png"
                ]
            elif self.action == "dead":
                image_paths = [
                    "../../../resource/img/item/ninja/dead/Dead_000.png",
                    "../../../resource/img/item/ninja/dead/Dead_001.png",
                    "../../../resource/img/item/ninja/dead/Dead_002.png",
                    "../../../resource/img/item/ninja/dead/Dead_003.png",
                    "../../../resource/img/item/ninja/dead/Dead_004.png",
                    "../../../resource/img/item/ninja/dead/Dead_005.png",
                    "../../../resource/img/item/ninja/dead/Dead_006.png",
                    "../../../resource/img/item/ninja/dead/Dead_007.png"
                ]
        elif self.character_type == 4:
            if self.action == "idle":
                image_paths = [
                    "../../../resource/img/item/knight/idle/Idle_000.png",
                    "../../../resource/img/item/knight/idle/Idle_001.png",
                    "../../../resource/img/item/knight/idle/Idle_002.png",
                    "../../../resource/img/item/knight/idle/Idle_003.png",
                    "../../../resource/img/item/knight/idle/Idle_004.png",
                    "../../../resource/img/item/knight/idle/Idle_005.png",
                    "../../../resource/img/item/knight/idle/Idle_006.png",
                    "../../../resource/img/item/knight/idle/Idle_007.png"
                ]
            elif self.action == "mlee":
                image_paths = [
                    "../../../resource/img/item/knight/mlee/Mlee_000.png",
                    "../../../resource/img/item/knight/mlee/Mlee_001.png",
                    "../../../resource/img/item/knight/mlee/Mlee_002.png",
                    "../../../resource/img/item/knight/mlee/Mlee_003.png",
                    "../../../resource/img/item/knight/mlee/Mlee_004.png",
                    "../../../resource/img/item/knight/mlee/Mlee_005.png",
                    "../../../resource/img/item/knight/mlee/Mlee_006.png",
                    "../../../resource/img/item/knight/mlee/Mlee_007.png"
                ]
            elif self.action == "dead":
                image_paths = [
                    "../../../resource/img/item/knight/dead/Dead_000.png",
                    "../../../resource/img/item/knight/dead/Dead_001.png",
                    "../../../resource/img/item/knight/dead/Dead_002.png",
                    "../../../resource/img/item/knight/dead/Dead_003.png",
                    "../../../resource/img/item/knight/dead/Dead_004.png",
                    "../../../resource/img/item/knight/dead/Dead_005.png",
                    "../../../resource/img/item/knight/dead/Dead_006.png",
                    "../../../resource/img/item/knight/dead/Dead_007.png"
                ]
        elif self.character_type == 1:
            if self.action == "idle":
                image_paths = [
                    "../../../resource/img/item/zombie/idle/Idle_000.png",
                    "../../../resource/img/item/zombie/idle/Idle_001.png",
                    "../../../resource/img/item/zombie/idle/Idle_002.png",
                    "../../../resource/img/item/zombie/idle/Idle_003.png",
                    "../../../resource/img/item/zombie/idle/Idle_004.png",
                    "../../../resource/img/item/zombie/idle/Idle_005.png",
                    "../../../resource/img/item/zombie/idle/Idle_006.png",
                    "../../../resource/img/item/zombie/idle/Idle_007.png"
                ]
            elif self.action == "mlee":
                image_paths = [
                    "../../../resource/img/item/zombie/mlee/Mlee_000.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_001.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_002.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_003.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_004.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_005.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_006.png",
                    "../../../resource/img/item/zombie/mlee/Mlee_007.png"
                ]
            elif self.action == "dead":
                image_paths = [
                    "../../../resource/img/item/zombie/dead/Dead_000.png",
                    "../../../resource/img/item/zombie/dead/Dead_001.png",
                    "../../../resource/img/item/zombie/dead/Dead_002.png",
                    "../../../resource/img/item/zombie/dead/Dead_003.png",
                    "../../../resource/img/item/zombie/dead/Dead_004.png",
                    "../../../resource/img/item/zombie/dead/Dead_005.png",
                    "../../../resource/img/item/zombie/dead/Dead_006.png",
                    "../../../resource/img/item/zombie/dead/Dead_007.png"
                ]
        else:
            raise ValueError("Invalid character type")
        images = []
        for path in image_paths:
            print(os.path.dirname(__file__))
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))  # Sửa đường dẫn ở đây
            image = pygame.image.load(image_path)
            resized_image = pygame.transform.smoothscale(image, (Para.SIZE // 3, Para.SIZE // 2))
            images.append(resized_image)
        return images
    def draw(self, screen):
        current_image = self.images[self.current_image_index]
        self.health_bar.x = self.position_x - Para.SIZE / 12
        self.health_bar.y = self.position_y - Para.SIZE / 4
        self.health_bar.draw(screen)
        screen.blit(current_image, (self.position_x, self.position_y))

    import pygame

    def drawDefault(self, screen):
        if self.character_type == 1:
            self.position_x = 190
            self.position_y = 222
            label_name = "Xác sống"
            label_price = "300$"
            label_description = "+Tấn công: 500 +Mô tả: Dường như không có trí tuệ, không phân biệt địch ta!!!"

        elif self.character_type == 2:
            self.position_x = 350
            self.position_y = 222
            label_name = "Cỗ máy"
            label_price = "500$"
            label_description = "+Tấn công: 300 +Mô tả: Luôn hoạt động ổn định, được lập trình bởi +Trương Văn Công!!!"

        elif self.character_type == 3:
            self.position_x = 510
            self.position_y = 222
            label_name = "Nhẫn giả"
            label_price = "1000$"
            label_description = "+Tấn công: 1000 +Mô tả: Sức tấn công ưu việt trong tất cả lính đánh thuê!!!"

        elif self.character_type == 4:
            self.position_x = 670
            self.position_y = 222
            label_name = "Hiệp sĩ"
            label_price = "2000$"
            label_description = "+Tấn công: 500 +Mô tả: Hiệp sĩ luôn trung thành. Mua năm hiệp sĩ sẽ thắng!!!"

        current_image = self.images[self.current_image_index]

        image_width = current_image.get_width()
        image_height = current_image.get_height()

        image_center_x = self.position_x + image_width / 2
        image_center_y = self.position_y + image_height / 2

        screen.blit(current_image, (self.position_x, self.position_y))

        label_font = pygame.font.Font(self.font_path, 14)
        label_name_text = label_font.render(label_name, True, (0, 250, 154))
        label_price_text = label_font.render(label_price, True, (255, 255, 0))
        label_description_text = label_font.render(label_description, True, (255, 255, 255))

        label_name_width = label_name_text.get_width()
        label_name_height = label_name_text.get_height()
        label_price_width = label_price_text.get_width()
        label_price_height = label_price_text.get_height()
        label_description_width = label_description_text.get_width()
        label_description_height = label_description_text.get_height()

        label_name_x = image_center_x - label_name_width / 2
        label_name_y = image_center_y - label_name_height / 2 - 50
        label_price_x = image_center_x - label_price_width / 2
        label_price_y = image_center_y - label_price_height / 2 - 33
        label_description_x = image_center_x - label_description_width / 2
        label_description_y = self.position_y + 60

        button_color = (255, 200, 0)  # Light orange color for the button
        button_text_color = (0, 0, 0)  # Black color for the button text
        button_font = pygame.font.Font(None, 18)  # Choose a suitable font for the button text
        border_radius = 9  # Adjust the border radius as needed
        button_width = 50  # Button width
        button_height = 20  # Button height
        button_position_x = self.position_x - button_width // 4  # Adjust position as needed
        button_position_y = self.position_y + button_height * 2.5  # Adjust position as needed

        pygame.draw.rect(screen, button_color, (button_position_x, button_position_y, button_width, button_height),
                         border_radius=border_radius)

        button_text = button_font.render("Mua", True, button_text_color)
        text_rect = button_text.get_rect(
            center=(button_position_x + button_width // 2, button_position_y + button_height // 2))
        screen.blit(button_text, text_rect)

        screen.blit(label_name_text, (label_name_x, label_name_y))
        screen.blit(label_price_text, (label_price_x, label_price_y))

        max_description_width = 14  # Maximum character width for each line
        lines = []
        current_line = ''

        for char in label_description:
            if char == '+':
                if current_line:
                    lines.append(current_line.strip())
                current_line = ''
            elif len(current_line) >= max_description_width and char.isspace():
                lines.append(current_line.strip())
                current_line = ''
            else:
                current_line += char

        if current_line:
            lines.append(current_line.strip())

        description_y = label_description_y + label_description_height + 5

        for line in lines:
            line_text = label_font.render(line, True, (255, 255, 255))
            line_width = line_text.get_width()
            line_x = image_center_x - line_width / 2
            screen.blit(line_text, (line_x, description_y))
            description_y += line_text.get_height() + 5
    pygame.display.update()
    def update(self, action):
        if action != self.action:
            self.action = action
            self.images = self.load_images()
            self.current_image_index = 0
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_interval:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.animation_timer = current_time

