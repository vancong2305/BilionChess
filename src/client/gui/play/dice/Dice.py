import pygame
import random

from src.client.gui.parameter.Para import Para


class Dice:
    animation_interval = 90
    current_image_index = 0
    position_x = 50
    position_y = 50
    rolling_result = 0

    def __init__(self):
        self.action = "idle"
        self.images = self.load_images()
        self.animation_timer = pygame.time.get_ticks()
    def load_images(self):
        image_paths = []
        if self.action == "roll":
            image_paths = [
                "../../resource/img/dice/roll/Dice_000.png",
                "../../resource/img/dice/roll/Dice_001.png",
                "../../resource/img/dice/roll/Dice_002.png",
                "../../resource/img/dice/roll/Dice_003.png",
                "../../resource/img/dice/roll/Dice_004.png",
                "../../resource/img/dice/roll/Dice_005.png",
                "../../resource/img/dice/roll/Dice_006.png",
                "../../resource/img/dice/roll/Dice_007.png"
            ]
        elif self.action == "stop":
            image_paths = [
                "../../resource/img/dice/idle/Dice_000.png",
                "../../resource/img/dice/idle/Dice_001.png",
                "../../resource/img/dice/idle/Dice_002.png",
                "../../resource/img/dice/idle/Dice_003.png",
                "../../resource/img/dice/idle/Dice_004.png",
                "../../resource/img/dice/idle/Dice_005.png"
            ]
        elif self.action == "idle":
            image_paths = [
                "../../resource/img/dice/idle/Dice_000.png"
            ]
        images = []
        for path in image_paths:
            image = pygame.image.load(path)
            resized_image = pygame.transform.smoothscale(image, (Para.SIZE, Para.SIZE))
            images.append(resized_image)
        return images

    def hide(self):
        self.current_image_index = 0

    def rolling(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)

    def result(self, number):
        self.current_image_index = number

    def draw(self, screen):
        current_image = self.images[self.current_image_index]
        screen.blit(current_image, (Para.WIDTH/2-Para.SIZE/2-5, Para.HEIGHT/2+Para.SIZE*1.5))

    def run(self):
        total_time = 3000  # Thời gian chạy quay liên tục (milliseconds)
        start_time = pygame.time.get_ticks()
        end_time = start_time + total_time

        while pygame.time.get_ticks() < end_time:
            self.rolling()
            self.draw()
            pygame.time.wait(self.animation_interval)

        self.action = "stop"  # Đặt hành động là "idle"
        number = random.randint(0, 5)  # Số ngẫu nhiên từ 0 đến 5
        self.images = self.load_images()
        self.result(number)

        total_idle_time = 300  # Thời gian hiển thị hình ảnh trong trạng thái "idle" (milliseconds)
        idle_start_time = pygame.time.get_ticks()
        idle_end_time = idle_start_time + total_idle_time

        while pygame.time.get_ticks() < idle_end_time:
            self.draw()
            pygame.time.wait(self.animation_interval)
        pygame.quit()
# dice = Dice()
# dice.run()