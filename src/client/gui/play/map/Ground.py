import pygame

from src.client.gui.parameter.Para import Para

screen = pygame.display.set_mode((Para.WIDTH, Para.HEIGHT))


grass_paths =  "./img/map/gravel.png"
grass_paths1 =  "./img/map/gravel_1.png"
grass_paths2 =  "./img/map/gravel_2.png"
grass_paths3 =  "./img/map/gravel_3.png"

grass_paths_image = pygame.transform.smoothscale(pygame.image.load(grass_paths), (Para.SIZE, Para.SIZE))
grass_paths_image1 = pygame.transform.smoothscale(pygame.image.load(grass_paths1), (Para.SIZE, Para.SIZE))
grass_paths_image2 = pygame.transform.smoothscale(pygame.image.load(grass_paths2), (Para.SIZE, Para.SIZE))
grass_paths_image3 = pygame.transform.smoothscale(pygame.image.load(grass_paths3), (Para.SIZE, Para.SIZE))
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