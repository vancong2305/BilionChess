import asyncio
import json
import os
import threading
from concurrent.futures import thread

import pygame

from src.client.WebSocketClient import WebSocketClient
from src.client.gui.play.Game import Game


def start_game():
    print("Bắt đầu trò chơi")


class WaitRoomMember:
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

        self.buttons = [
            Button(self.button_x, 300 + (self.button_height + self.button_spacing) * 2, self.button_width,
                   self.button_height, "Rời phòng", start_game)
        ]
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                    exit(0)
            for button in self.buttons:
                button.handle_event(event)

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
        while True:
            message = await WebSocketClient.client.recv()
            # Đưa tin nhắn vào hàng đợi
            WebSocketClient.message_queue.put(message)

    async def run(self):
        # Tạo một event loop mới
        asyncio.create_task(self.receive_message())

        while self.running:
            # Kiểm tra xem có tin nhắn mới từ server không
            if not WebSocketClient.message_queue.empty():
                message = WebSocketClient.message_queue.get()
                # Xử lý tin nhắn từ server
                parsed_data = json.loads(message)
                if parsed_data.get('match_id'):
                    self.running = False
                    await Game(parsed_data).start()
                else:
                    members = parsed_data['data'][0]['members']
                    for member in members:
                        if member['role'] == 'member':
                            user_name = member['user_name']
                            self.player_name = user_name
                            print(user_name)
            await asyncio.sleep(1 / 60)
            self.handle_events()
            self.draw()
            self.clock.tick(60)

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
