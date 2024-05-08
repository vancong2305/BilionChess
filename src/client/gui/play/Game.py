# Game is store object will change
# Store is manage object not change


import time

import pygame
from pygame.locals import *

from src.client.gui.parameter.Para import Para
from src.client.gui.play.figure.Body import Body
from src.client.gui.play.map.Map import Map


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Merchant Chess")
        self.getDataState = 1
        self.screen = pygame.display.set_mode((Para.WIDTH, Para.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False

        self.map = Map()
        self.character_one = Body(1)
        self.character_two = Body(2)

    def start(self):
        self.running = True
        self.state = "run"
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            if self.state == "run":
                # Sử dụng hàm moveList() để di chuyển nhân vật đến danh sách các vị trí
                x, y = (1, 2)
                Map.map_positions = Map.map_positions
                target_positions = Map.map_positions
                self.character_two.moveList(self.screen, target_positions, 1)
                self.state = self.character_two.action
            self.clock.tick(30)
        pygame.quit()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
    def update(self):
        self.character_one.update("idle")
        self.character_two.update("idle")
    def render(self):
        self.screen.fill((115, 115, 115))
        self.map.draw(self.screen)
        self.character_one.draw(self.screen)
        self.character_two.draw(self.screen)
        Body.player_one = self.character_one
        Body.player_two = self.character_two
        self.map.get_position()
        self.map.get_corner_positions()
        Map.map_positions = self.map.positions
        Map.map_corner = self.map.get_corner_positions()
        pygame.display.flip()

# Sử dụng lớp Game từ một lớp khác
game = Game()
game.start()