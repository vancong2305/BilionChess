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
from src.client.gui.parameter.Connect import Connect
from src.client.gui.parameter.Para import Para
from src.client.gui.play.dice.Dice import Dice
from src.client.gui.play.dice.Roll import Roll
from src.client.gui.play.figure.Body import Body
from src.client.gui.play.information.Information import Information
from src.client.gui.play.item.Item import Item
from src.client.gui.play.map.Map import Map
from src.client.handle.MatchRequest import MatchRequest


class Game:
    def __init__(self, match):
        print(match)
        self.match = match
        pygame.init()
        pygame.display.set_caption("Merchant chess ID: " + Connect.ID.__str__())
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
        while self.running:
            self.update()
            self.render()
            await self.handle_events()
            if not WebSocketClient.message_queue.empty():
                message = WebSocketClient.message_queue.get()
                # Xử lý tin nhắn từ server
                parsed_data = json.loads(message)
                if parsed_data.get('remaining_time'):

                    self.information.set_time(parsed_data.get('remaining_time'))
                    if (parsed_data.get('remaining_time') == 20):
                        self.state = "roll"
                if parsed_data.get('match_id'):
                    self.match = parsed_data
                    # print(parsed_data)
                    # users = parsed_data.get('users')
                    # hp_user1 = users[0]["hp"]
                    # hp_user2 = users[1]["hp"]
                    # user_id1 = users[0]["user_id"]
                    # user_id2 = users[1]["user_id"]
                    # self.character_one.health_bar.max_health = 2000
                    # # self.character_one.health_bar.current_health = hp_user1
                    # self.character_one.health_bar.name = user_id1
                    # self.character_one.health_bar.text2_color = (141, 238, 238)
                    # # self.character_two.health_bar.current_health = hp_user2
                    # self.character_two.health_bar.name = user_id2
                    # self.character_two.health_bar.max_health = 2200
                    # self.character_two.health_bar.text2_color =(244, 164, 96)

                    parsed_data.get('dice')
                    if self.state == "roll":
                        self.dice.run(self.screen, parsed_data.get('dice')-1)
                        self.state = "run"
                    if self.state == "run":
                        target_positions = [(pos["x"], pos["y"]) for pos in parsed_data.get('move_positions')]
                        if parsed_data.get('char_id') == 1:
                            self.character_one.moveList(self.screen, target_positions, 1, 1)
                            self.state = self.character_one.action
                            pass
                        if parsed_data.get('char_id') == 2:
                            self.character_two.moveList(self.screen, target_positions, 1, 2)
                            self.state = self.character_two.action
                            pass
                    users = parsed_data.get('users')
                    hp_user1 = users[0]["hp"]
                    hp_user2 = users[1]["hp"]
                    user_id1 = users[0]["user_id"]
                    user_id2 = users[1]["user_id"]
                    gold1 = users[0]["gold"]
                    gold2 = users[1]["gold"]
                    self.character_one.health_bar.max_health = 2000
                    self.character_one.health_bar.current_health = hp_user1
                    self.character_one.health_bar.name = user_id1
                    self.character_one.health_bar.text2_color = (141, 238, 238)
                    self.character_two.health_bar.current_health = hp_user2
                    self.character_two.health_bar.name = user_id2
                    self.character_two.health_bar.max_health = 2200
                    self.character_two.health_bar.text2_color =(244, 164, 96)

                    self.information.set_name(parsed_data.get('turn_id').__str__())
                    self.information.set_top_left_text("Người chơi " + user_id1.__str__() + " có: " + gold1.__str__() + " VND")
                    self.information.set_top_right_text("Người chơi " + user_id2.__str__() + " có: " + gold2.__str__() + " VND")
            if len(self.match.get('items')) > 0:
                for item in self.match.get('items'):
                    if item.get('item_id') == 1:
                        x = item["position"]["x"]
                        y = item["position"]["y"]
                        Item(1).draw(self.screen, x + 20, y + 10, item.get('user_id'), item.get('color'))
                    if item.get('item_id') == 2:
                        x = item["position"]["x"]
                        y = item["position"]["y"]
                        Item(2).draw(self.screen, x + 20, y + 10, item.get('user_id'), item.get('color'))
                    if item.get('item_id') == 3:
                        x = item["position"]["x"]
                        y = item["position"]["y"]
                        Item(3).draw(self.screen, x + 20, y + 10, item.get('user_id'), item.get('color'))
                    if item.get('item_id') == 4:
                        x = item["position"]["x"]
                        y = item["position"]["y"]
                        Item(4).draw(self.screen, x + 20, y + 10, item.get('user_id'), item.get('color'))
            pygame.display.flip()
            await asyncio.sleep(1/32)
            self.clock.tick(32)
        pygame.quit()
    async def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.item1.button_buy_rect.collidepoint(mouse_pos):
                    print("Vào đây nè 1" + str(self.match['match_id']))
                    await MatchRequest().update_match(1, int(self.match['match_id']))
                if self.item2.button_buy_rect.collidepoint(mouse_pos):
                    print("Vào đây nè 2")
                    await MatchRequest().update_match(2, int(self.match['match_id']))
                if self.item3.button_buy_rect.collidepoint(mouse_pos):
                    print("Vào đây nè 3")
                    await MatchRequest().update_match(3, int(self.match['match_id']))
                if self.item4.button_buy_rect.collidepoint(mouse_pos):
                    print("Vào đây nè 4")
                    await MatchRequest().update_match(4, int(self.match['match_id']))
    def update(self):
        self.character_one.update("idle")
        self.character_two.update("idle")

    def run_dice(self, screen):
        self.dice.run(screen)
    def render(self):
        self.screen.fill((115, 115, 115))
        self.map.draw(self.screen)
        self.character_two.draw(self.screen)
        self.character_one.draw(self.screen)
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


# Sử dụng lớp Game từ một lớp khác
# game = Game()
# await game.start()