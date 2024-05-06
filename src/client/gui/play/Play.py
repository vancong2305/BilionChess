import os
import time

import pygame
from pygame.locals import *

from src.client.gui.parameter.Para import Para
from src.client.gui.play.figure.Body import Body
from src.client.gui.play.map.Ground import Map


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Merchant Chess")
        self.screen = pygame.display.set_mode((Para.WIDTH, Para.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False

        self.map = Map()
        self.character_one = Body(1)
        self.character_two = Body(2)

        image = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resource/img/map/background.png"))
        self.background_image = pygame.image.load(image)
        self.background_image = pygame.transform.scale(self.background_image, (Para.WIDTH, Para.HEIGHT))

    def start(self):
        self.running = True
        start_time = time.time()
        your_function_interval = 10  # Khoảng thời gian (giây) giữa các lần gọi hàm your_function()
        your_function_last_call = start_time
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            current_time = time.time()
            elapsed_time = current_time - your_function_last_call
            if elapsed_time >= your_function_interval:
                self.character_two.move(self.screen, 200, 200, 1)
                your_function_last_call = current_time
            self.clock.tick(60)
        pygame.quit()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
    def update(self):
        self.character_one.update("idle")
        self.character_two.update("idle")
    def render(self):
        self.screen.fill((0, 188, 110))  # Màu xanh lá cây
        self.screen.blit(self.background_image, (0, 0))
        self.map.draw(self.screen)
        self.character_one.draw(self.screen)
        self.character_two.draw(self.screen)
        pygame.display.flip()

# Sử dụng lớp Game từ một lớp khác
game = Game()
game.start()