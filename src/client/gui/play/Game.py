# Game is store object will change
# Store is manage object not change
import asyncio
import json
import threading
import time
from concurrent.futures import thread

import pygame
from pygame.locals import *

from src.client.WebSocketClient import WebSocketClient
from src.client.gui.parameter.Para import Para
from src.client.gui.play.dice.Dice import Dice
from src.client.gui.play.dice.Roll import Roll
from src.client.gui.play.figure.Body import Body
from src.client.gui.play.information.Information import Information
from src.client.gui.play.item.Item import Item
from src.client.gui.play.map.Map import Map


class Game:
    def __init__(self, match):
        print(match)
        pygame.init()
        pygame.display.set_caption("Merchant Chess")
        self.getDataState = 1
        self.screen = pygame.display.set_mode((Para.WIDTH, Para.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.information = Information()
        self.dice = Dice()
        self.map = Map()
        self.roll = Roll()
        self.character_one = Body(1)
        self.character_two = Body(2)
        self.item1 = Item(1)
        self.item2 = Item(2)
        self.item3 = Item(3)
        self.item4 = Item(4)

    async def start(self):
        self.running = True
        # self.state = "run"
        self.state = "stop"
        Dice.state = "roll"
        while self.running:
            if not WebSocketClient.message_queue.empty():
                message = WebSocketClient.message_queue.get()
                # Xử lý tin nhắn từ server
                parsed_data = json.loads(message)
                if parsed_data.get('remaining_time'):
                    self.information.set_time(parsed_data.get('remaining_time'))
            await asyncio.sleep(1 / 60)
            self.handle_events()
            self.update()
            self.render()
            if (Dice.state == "roll"):
                Dice.state = "stop"
                self.dice.run(self.screen)
            if self.state == "run":
                # Sử dụng hàm moveList() để di chuyển nhân vật đến danh sách các vị trí
                map_positions = Map.map_positions
                target_positions = [(pos['x'], pos['y']) for pos in map_positions[:5]]
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

    def run_dice(self, screen):
        self.dice.run(screen)
    def render(self):
        self.screen.fill((115, 115, 115))
        self.map.draw(self.screen)
        self.character_one.draw(self.screen)
        self.character_two.draw(self.screen)
        Body.player_one = self.character_one
        Body.player_two = self.character_two
        Body.player_one.screen = self.screen
        Body.player_two.screen = self.screen

        self.map.get_position()
        self.map.get_corner_positions()
        Map.map_positions = self.map.positions
        Map.map_corner = self.map.get_corner_positions()
        Map.map = self.map
        Map.screen = self.screen

        self.information.draw(self.screen)
        Information.infomation = self.information
        Information.screen = self.screen
        # self.information.set_time(10)

        self.dice.draw(self.screen)
        Dice.dice = self.dice
        Dice.screen = self.screen
        # self.roll.draw(self.roll)

        self.item1.drawDefault(self.screen)
        Item.item1 = self.item1
        Item.item1.screen = self.screen
        self.item2.drawDefault(self.screen)
        Item.item2 = self.item2
        Item.item2.screen = self.screen
        self.item3.drawDefault(self.screen)
        Item.item3 = self.item3
        Item.item3.screen = self.screen
        self.item4.drawDefault(self.screen)
        Item.item4 = self.item4
        Item.item4.screen = self.screen

        pygame.display.flip()

# Sử dụng lớp Game từ một lớp khác
# game = Game()
# await game.start()