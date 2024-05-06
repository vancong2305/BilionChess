import os
import time

import pygame

from src.client.gui.parameter.Para import Para
from src.client.gui.play.figure.HealthBar import HealthBar


class Body:
    animation_interval = 100
    current_image_index = 0
    position_x = 50
    position_y = 50
    def __init__(self, character_type):
        self.character_type = character_type
        self.action = "idle"  # Hành động mặc định là "idle"
        self.images = self.load_images()
        self.animation_timer = pygame.time.get_ticks()
        # Tạo một đối tượng thanh máu
        self.health_bar = HealthBar(100, 100, Para.SIZE / 2, 10, 100)
        self.health_bar.decrease_health(20)
    def load_images(self):
        image_paths = []
        if self.character_type == 1:
            if self.action == "idle":
                image_paths = [
                    "../../../resource/img/boy/idle/Idle_000.png",
                    "../../../resource/img/boy/idle/Idle_001.png",
                    "../../../resource/img/boy/idle/Idle_002.png",
                    "../../../resource/img/boy/idle/Idle_003.png",
                    "../../../resource/img/boy/idle/Idle_004.png",
                    "../../../resource/img/boy/idle/Idle_005.png",
                    "../../../resource/img/boy/idle/Idle_006.png",
                    "../../../resource/img/boy/idle/Idle_007.png"
                ]
            elif self.action == "run":
                image_paths = [
                    "../../../resource/img/boy/run/Run_000.png",
                    "../../../resource/img/boy/run/Run_001.png",
                    "../../../resource/img/boy/run/Run_002.png",
                    "../../../resource/img/boy/run/Run_003.png",
                    "../../../resource/img/boy/run/Run_004.png",
                    "../../../resource/img/boy/run/Run_005.png",
                    "../../../resource/img/boy/run/Run_006.png",
                    "../../../resource/img/boy/run/Run_007.png"
                ]
            # Add more cases for other actions as needed
        elif self.character_type == 2:
            if self.action == "idle":
                image_paths = [
                    "../../../resource/img/girl/idle/Idle_000.png",
                    "../../../resource/img/girl/idle/Idle_001.png",
                    "../../../resource/img/girl/idle/Idle_002.png",
                    "../../../resource/img/girl/idle/Idle_003.png",
                    "../../../resource/img/girl/idle/Idle_004.png",
                    "../../../resource/img/girl/idle/Idle_005.png",
                    "../../../resource/img/girl/idle/Idle_006.png",
                    "../../../resource/img/girl/idle/Idle_007.png"
                ]
            elif self.action == "run":
                image_paths = [
                    "../../../resource/img/girl/run/Run_000.png",
                    "../../../resource/img/girl/run/Run_001.png",
                    "../../../resource/img/girl/run/Run_002.png",
                    "../../../resource/img/girl/run/Run_003.png",
                    "../../../resource/img/girl/run/Run_004.png",
                    "../../../resource/img/girl/run/Run_005.png",
                    "../../../resource/img/girl/run/Run_006.png",
                    "../../../resource/img/girl/run/Run_007.png"
                ]
            # Add more cases for other actions as needed
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
    def update(self, action):
        if action != self.action:
            self.action = action
            self.images = self.load_images()
            self.current_image_index = 0
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_interval:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.animation_timer = current_time

    def move(self, screen, x, y, duration):
        self.action = "run"
        start_time = time.time()
        elapsed_time = 0
        start_x = self.position_x  # Vị trí ban đầu của x
        start_y = self.position_y  # Vị trí ban đầu của y

        while elapsed_time < duration:
            current_time = time.time()
            elapsed_time = current_time - start_time
            progress = elapsed_time / duration
            self.position_x = start_x + (x - start_x) * progress
            self.position_y = start_y + (y - start_y) * progress
            self.draw(screen)  # Vẽ lại hình ảnh ở vị trí mới
            pygame.display.flip()  # Cập nhật màn hình
            time.sleep(0.001)