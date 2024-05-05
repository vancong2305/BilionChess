import os

import pygame

class RoomMaster:
    def __init__(self, room_name, player_name):
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Giao diện Room Master")

        self.room_name = room_name
        self.player_name = player_name

        self.font = pygame.font.Font(None, 32)

        self.button_width, self.button_height = 200, 50
        self.button_spacing = 20
        self.button_x = (self.screen_width - self.button_width) // 2

        self.buttons = [
            Button(self.button_x, 300, self.button_width, self.button_height, "Đuổi", self.kick_player),
            Button(self.button_x, 300 + self.button_height + self.button_spacing, self.button_width, self.button_height, "Giải tán", self.dismiss_room),
            Button(self.button_x, 300 + (self.button_height + self.button_spacing) * 2, self.button_width, self.button_height, "Bắt đầu", self.start_game)
        ]

        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        self.screen.fill((255, 255, 255))
        label_surface = self.font.render("Chủ phòng: " + self.room_name, True, (0, 0, 0))
        label_rect = label_surface.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(label_surface, label_rect)
        grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(grandparent_directory, 'ready', 'Arial.ttf')

        self.font = pygame.font.Font(font_path, 32)
        player_label_surface = self.font.render("Thành viên: " + self.player_name, True, (0, 0, 0))
        player_label_rect = player_label_surface.get_rect(center=(self.screen_width // 2, 200))
        self.screen.blit(player_label_surface, player_label_rect)

        for button in self.buttons:
            button.draw(self.screen, self.font)

        pygame.display.flip()

    def kick_player(self):
        print("Đuổi người chơi")

    def dismiss_room(self):
        print("Giải tán phòng")

    def start_game(self):
        print("Bắt đầu trò chơi")

    def run(self):
        self.running = True
        while self.running:
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
