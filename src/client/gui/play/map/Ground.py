import os

import pygame

from src.client.gui.parameter.Para import Para

screen = pygame.display.set_mode((Para.WIDTH, Para.HEIGHT))

# Đường dẫn đến ảnh
grass_paths = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../resource/img/map/gravel.png'))

# Tải ảnh
grass_paths_image = pygame.image.load(grass_paths)

# Thay đổi kích thước ảnh
grass_paths_image = pygame.transform.smoothscale(grass_paths_image, (Para.SIZE, Para.SIZE))

class Map:
    numbers = [0, 1, 2, 3, 4, 5, 6, 7]
    numbers1 = [0, 1, 2, 3]
    gap = 20
    def __init__(self):
        pass
    def draw(self, screen):
        # Vẽ hàng trên
        for num in self.numbers:
            x = num * (Para.SIZE+self.gap) + Para.SIZE/2   # Tọa độ x
            y = Para.SIZE  # Tọa độ y
            screen.blit(grass_paths_image, (x, y))

        # Vẽ hàng dưới
        for num in self.numbers:
            x = num * (Para.SIZE+self.gap) + Para.SIZE/2  # Tọa độ x
            y = (len(self.numbers1) + 1) * (Para.SIZE + self.gap) + Para.SIZE
            screen.blit(grass_paths_image, (x, y))

        # Vẽ bên trái
        for num in self.numbers1:
            x = Para.SIZE/2
            y = (num+1) * (Para.SIZE + self.gap) + Para.SIZE  # Tọa độ y
            screen.blit(grass_paths_image, (x, y))

        # Vẽ bên phải
        for num in self.numbers1:
            x = (len(self.numbers)-1) * (Para.SIZE+self.gap) + Para.SIZE/2
            y = (num+1) * (Para.SIZE + self.gap) + Para.SIZE  # Tọa độ y
            screen.blit(grass_paths_image, (x, y))