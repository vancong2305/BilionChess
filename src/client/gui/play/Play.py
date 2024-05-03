import pygame
from pygame.locals import *

from src.client.gui.parameter.Para import Para
from src.client.gui.play.figure.Body import Body
from src.client.gui.play.figure.HealthBar import HealthBar
from src.client.gui.play.map.Ground import Map

pygame.init()

# Tạo bản đồ
map = Map()

# Tạo một đối tượng thanh máu
health_bar = HealthBar(100, 100, Para.SIZE/2, 10, 100)
health_bar.decrease_health(10)

# Tạo đối tượng nhân vật 1
character_one = Body(1)

# Tạo đối tượng nhân vật 2
character_two = Body(2)

# Tải hình ảnh nền
background_image = pygame.image.load("../../img/map/background.png")
background_image = pygame.transform.scale(background_image, (Para.WIDTH, Para.HEIGHT))

# Tạo màn hình
screen = pygame.display.set_mode((Para.WIDTH, Para.HEIGHT))
pygame.display.set_caption("Merchant Chess")

# Đối tượng Clock
clock = pygame.time.Clock()

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill((0, 188, 110))  # Màu xanh lá cây

    # Vẽ hình ảnh nền
    screen.blit(background_image, (0, 0))

    map.draw(screen)
    # Vẽ nhân vật 1
    character_one.draw(screen)
    character_one.update("idle")


    health_bar.x = character_one.position_x - Para.SIZE/12
    health_bar.y = character_one.position_y - Para.SIZE/4
    health_bar.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Giới hạn tốc độ khung hình

pygame.quit()