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
    map = None
    map_positions = []
    map_corner = []
    numbers = [0, 1, 2, 3, 4, 5, 6, 7]
    numbers1 = [0, 1, 2, 3]
    gap = 20
    screen = None
    def __init__(self):
        self.positions = []
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

    def get_position(self):
        x = 0 * (Para.SIZE + self.gap) + Para.SIZE / 2  # Tọa độ x
        y = Para.SIZE  # Tọa độ y
        self.positions.append((x, y))
        # Vẽ bên trái
        for num in self.numbers1:
            x = Para.SIZE / 2
            y = (num + 1) * (Para.SIZE + self.gap) + Para.SIZE  # Tọa độ y
            self.positions.append((x, y))
        # Vẽ hàng dưới
        for num in self.numbers:
            x = num * (Para.SIZE + self.gap) + Para.SIZE / 2  # Tọa độ x
            y = (len(self.numbers1) + 1) * (Para.SIZE + self.gap) + Para.SIZE
            self.positions.append((x, y))
        # Vẽ bên phải
        for num in self.numbers1[::-1]:  # Iterate through numbers1 in reverse order
            x = (len(self.numbers) - 1) * (Para.SIZE + self.gap) + Para.SIZE / 2
            y = (num + 1) * (Para.SIZE + self.gap) + Para.SIZE  # Tọa độ y
            self.positions.append((x, y))
        # Vẽ hàng trên
        for num in self.numbers[::-1]:  # Iterate through self.numbers in reverse order
            x = num * (Para.SIZE + self.gap) + Para.SIZE / 2  # Tọa độ x
            y = Para.SIZE  # Tọa độ y
            self.positions.append((x, y))
    def get_corner_positions(self):
        # Extract top-left corner position
        top_left_x = self.numbers[0] * (Para.SIZE + self.gap) + Para.SIZE / 2
        top_left_y = Para.SIZE

        # Extract top-right corner position
        top_right_x = (len(self.numbers) - 1) * (Para.SIZE + self.gap) + Para.SIZE / 2
        top_right_y = Para.SIZE

        # Extract bottom-left corner position
        bottom_left_x = Para.SIZE / 2
        bottom_left_y = (len(self.numbers1) + 1) * (Para.SIZE + self.gap) + Para.SIZE

        # Extract bottom-right corner position
        bottom_right_x = (len(self.numbers) - 1) * (Para.SIZE + self.gap) + Para.SIZE / 2
        bottom_right_y = (len(self.numbers1) + 1) * (Para.SIZE + self.gap) + Para.SIZE

        # Return corner positions as a list of tuples
        return [(top_left_x, top_left_y), (top_right_x, top_right_y),
                (bottom_left_x, bottom_left_y), (bottom_right_x, bottom_right_y)]


