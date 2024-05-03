import pygame
from src.client.gui.parameter.Para import Para

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

    def load_images(self):
        image_paths = []
        if self.character_type == 1:
            if self.action == "idle":
                image_paths = [
                    "./img/boy/idle/Idle_000.png",
                    "./img/boy/idle/Idle_001.png",
                    "./img/boy/idle/Idle_002.png",
                    "./img/boy/idle/Idle_003.png",
                    "./img/boy/idle/Idle_004.png",
                    "./img/boy/idle/Idle_005.png",
                    "./img/boy/idle/Idle_006.png",
                    "./img/boy/idle/Idle_007.png",
                    "./img/boy/idle/Idle_008.png",
                    "./img/boy/idle/Idle_009.png"
                ]
            elif self.action == "walk":
                image_paths = [
                    "./img/boy/walk/Walk_000.png",
                    "./img/boy/walk/Walk_001.png",
                    "./img/boy/walk/Walk_002.png",
                    "./img/boy/walk/Walk_003.png",
                    "./img/boy/walk/Walk_004.png",
                    "./img/boy/walk/Walk_005.png",
                    "./img/boy/walk/Walk_006.png",
                    "./img/boy/walk/Walk_007.png",
                    "./img/boy/walk/Walk_008.png",
                    "./img/boy/walk/Walk_009.png"
                ]
            # Add more cases for other actions as needed
        elif self.character_type == 2:
            if self.action == "idle":
                image_paths = [
                    "./img/girl/idle/Idle_000.png",
                    "./img/girl/idle/Idle_001.png",
                    "./img/girl/idle/Idle_002.png",
                    "./img/girl/idle/Idle_003.png",
                    "./img/girl/idle/Idle_004.png",
                    "./img/girl/idle/Idle_005.png",
                    "./img/girl/idle/Idle_006.png",
                    "./img/girl/idle/Idle_007.png",
                    "./img/girl/idle/Idle_008.png",
                    "./img/girl/idle/Idle_009.png"
                ]
            elif self.action == "walk":
                image_paths = [
                    "./img/girl/walk/Walk_000.png",
                    "./img/girl/walk/Walk_001.png",
                    "./img/girl/walk/Walk_002.png",
                    "./img/girl/walk/Walk_003.png",
                    "./img/girl/walk/Walk_004.png",
                    "./img/girl/walk/Walk_005.png",
                    "./img/girl/walk/Walk_006.png",
                    "./img/girl/walk/Walk_007.png",
                    "./img/girl/walk/Walk_008.png",
                    "./img/girl/walk/Walk_009.png"
                ]
            # Add more cases for other actions as needed
        else:
            raise ValueError("Invalid character type")

        images = []
        for path in image_paths:
            image = pygame.image.load(path)
            resized_image = pygame.transform.smoothscale(image, (Para.SIZE // 3, Para.SIZE // 2))
            images.append(resized_image)
        return images

    def draw(self, screen):
        current_image = self.images[self.current_image_index]
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