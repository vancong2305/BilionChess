import asyncio
import json
import os
import threading
from concurrent.futures import thread

import pygame

from src.client.WebSocketClient import WebSocketClient
from src.client.gui.play.Game import Game
from src.client.handle.MatchRequest import MatchRequest
from src.client.handle.RoomRequest import RoomRequest
import textwrap

class WaitRoomMaster:
    def __init__(self, room_name, player_name):
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Phòng chờ của " + room_name)
        self.room_name = room_name
        self.player_name = player_name
        grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(grandparent_directory, 'ready', 'Arial.ttf')
        self.font = pygame.font.Font(font_path, 32)
        self.button_width, self.button_height = 200, 50
        self.button_spacing = 20
        self.button_x = (self.screen_width - self.button_width) // 2
        self.runningTask = True
        self.buttons = [
            Button(self.button_x, 300 + (self.button_height + self.button_spacing) * 2, self.button_width,
                   self.button_height, "Bắt đầu", self.start_game),
            Button(self.button_x, 300 + (self.button_height + self.button_spacing) * 2.9, self.button_width,
                   self.button_height, "Rời phòng", self.delete_room)
        ]
        self.running = True

    async def start_game(self):
        print("Bắt đầu trận đấu")
        if self.player_name.__str__() == "Unknow":
            print("CHưa có người chơi trong phòng")
        else:
            await MatchRequest().create_match()

    async def delete_room(self):
        print("Bắt đầu trận đấu")
        await RoomRequest().delete()

    def draw(self):
        self.screen.fill((232, 232, 232))

        for button in self.buttons:
            button.draw(self.screen, self.font)
        self.draw_master(150, 100, 100)
        self.draw_member(550, 100, 100)
        label1_surface = self.font.render("Chủ phòng", True, (205, 0, 0))
        label1_rect = label1_surface.get_rect(center=(150 + 100 // 2, 235))
        self.screen.blit(label1_surface, label1_rect)

        label2_surface = self.font.render("Thành viên", True, (205, 0, 0))
        label2_rect = label2_surface.get_rect(center=(550 + 100 // 2, 235))
        self.screen.blit(label2_surface, label2_rect)


        label1_surface = self.font.render(self.room_name, True, (16, 78, 139))
        label1_rect = label1_surface.get_rect(center=(150 + 100 // 2, 275))
        self.screen.blit(label1_surface, label1_rect)

        label2_surface = self.font.render(self.player_name, True, (16, 78, 139))
        label2_rect = label2_surface.get_rect(center=(550 + 100 // 2, 275))
        self.screen.blit(label2_surface, label2_rect)



        if self.player_name.__str__() == "Unknow":
            text = self.player_name + " không phải người chơi, không thể bắt đầu trận đấu!"

            # Số ký tự tối đa cho mỗi dòng
            max_characters_per_line = 30

            # Tách đoạn văn bản thành các dòng
            wrapped_lines = textwrap.wrap(text, max_characters_per_line)

            # Render các dòng thành các surface
            line_surfaces = []
            for line in wrapped_lines:
                line_surface = self.font.render(line, True, (205, 0, 0))
                line_surfaces.append(line_surface)

            # Tính toán tọa độ và vẽ các dòng lên màn hình
            y = self.screen.get_height() // 2 + 50
            for line_surface in line_surfaces:
                line_rect = line_surface.get_rect(center=(self.screen.get_width() // 2, y))
                self.screen.blit(line_surface, line_rect)
                y += line_surface.get_height()

        pygame.display.flip()

    def draw_master(self, x, y, size):
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resource/img/room/master.png"))
        image = pygame.image.load(image_path)
        resized_image = pygame.transform.smoothscale(image, (size, size))
        self.screen.blit(resized_image, (x, y))

    def draw_member(self, x, y, size):
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resource/img/room/member.png"))
        image = pygame.image.load(image_path)
        resized_image = pygame.transform.smoothscale(image, (size, size))
        self.screen.blit(resized_image, (x, y))

    async def receive_message(self):
        try:
            while self.runningTask:
                message = await WebSocketClient.client.recv()
                # Đưa tin nhắn vào hàng đợi
                WebSocketClient.message_queue.put(message)
                await asyncio.sleep(1/30)
        except asyncio.CancelledError:
            # Xử lý khi task bị hủy
            print("Task bị hủy.")


    async def run(self):
        # Tạo một event loop mới
        self.task = asyncio.create_task(self.receive_message())  # Tạo task

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                        exit(0)
                for button in self.buttons:
                    await button.handle_event(event)
            if not WebSocketClient.message_queue.empty():
                message = WebSocketClient.message_queue.get()
                # Xử lý tin nhắn từ server
                parsed_data = json.loads(message)
                if parsed_data.get('match_id'):
                    self.running = False
                    await Game(parsed_data).start()
                elif parsed_data.get('status_delete'):
                    print("have")
                    self.runningTask = False
                    try:
                        self.task.cancel()
                        await self.task
                    except asyncio.CancelledError:
                        pass
                    self.running = False
                    break
                elif parsed_data.get('status_leave'):
                    self.player_name = "Unknow"
                else:
                    members = parsed_data['data'][0]['members']
                    for member in members:
                        if member['role'] == 'member':
                            user_name = member['user_name']
                            self.player_name = user_name
                            print(user_name)
            await asyncio.sleep(1 / 30)
            self.draw()
            self.clock.tick(30)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    async def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action is not None:
                    await self.action()
