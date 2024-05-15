import os
import pygame

from src.client.gui.room.WaitRoomMaster import WaitRoomMaster
from src.client.gui.room.WaitingRoomList import WaitingRoomList
from src.client.handle.RoomRequest import RoomRequest

class WelcomeScreen:
    player_name = ''

    def __init__(self, player_name):
        WelcomeScreen.player_name = player_name
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Giao diện trực quan")
        grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(grandparent_directory, 'ready', 'Arial.ttf')
        self.font = pygame.font.Font(font_path, 32)
        self.button_width, self.button_height = 300, 50
        self.button_spacing = 70
        self.button_x = (self.screen_width - self.button_width) / 2
        image_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../resource/img/map/background.png'))
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.buttons = [
            Button(self.button_x, 200, self.button_width, self.button_height, "Chơi trực tuyến", self.play_online),
            Button(self.button_x, 200 + self.button_spacing, self.button_width, self.button_height, "Tạo phòng",
                   self.create_room),
            Button(self.button_x, 200 + self.button_spacing * 2, self.button_width, self.button_height,
                   "Chơi với máy", self.play_with_ai),
            Button(self.button_x, 200 + self.button_spacing * 3, self.button_width, self.button_height, "Thoát",
                   self.quit_game)
        ]

    async def play_online(self):
        await WaitingRoomList(WelcomeScreen.player_name).run()
        print("Chơi trực tuyến")
        await self.run()

    async def create_room(self):
        # pygame.quit()
        await RoomRequest().create()
        await WaitRoomMaster(WelcomeScreen.player_name, "Unknow").run()
        await self.run()

    def play_with_ai(self):
        pygame.quit()
        print("Chơi với máy")

    def quit_game(self):
        pygame.quit()
        exit(0)

    async def run(self):
        while True:
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
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            label_surface = self.font.render("Xin chào " + WelcomeScreen.player_name, True, (0, 0, 0))
            label_rect = label_surface.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(label_surface, label_rect)
            for button in self.buttons:
                button.draw(self.screen, self.font)

            pygame.display.flip()
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

    async def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                await self.action()