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
            # Button(self.button_x, 300, self.button_width, self.button_height, "Đuổi", self.kick_player),
            # Button(self.button_x, 300 + self.button_height + self.button_spacing, self.button_width, self.button_height, "Giải tán", self.dismiss_room),
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
        self.screen.fill((232,232,232))
        grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(grandparent_directory, 'ready', 'Arial.ttf')
        self.font = pygame.font.Font(font_path, 32)
        for button in self.buttons:
            button.draw(self.screen, self.font)
            # Vẽ hai hình vuông
        self.draw_master(150, 100, 100)  # Hình vuông thứ nhất (màu đỏ)
        self.draw_member(550, 100, 100)  # Hình vuông thứ hai (màu xanh)
        # Vẽ hai nhãn phía dưới hình vuông
        label1_surface = self.font.render("Chủ phòng", True, (205,0,0))  # Red color (RGB)
        label1_rect = label1_surface.get_rect(center=(150 + 100 // 2, 235))
        self.screen.blit(label1_surface, label1_rect)

        label2_surface = self.font.render("Thành viên", True, (205,0,0))  # Red color (RGB)
        label2_rect = label2_surface.get_rect(center=(550 + 100 // 2, 235))
        self.screen.blit(label2_surface, label2_rect)

        label1_surface = self.font.render(self.room_name, True, (16,78,139))
        label1_rect = label1_surface.get_rect(center=(150+100//2, 275))
        self.screen.blit(label1_surface, label1_rect)

        label2_surface = self.font.render(self.player_name, True, (16,78,139))
        label2_rect = label2_surface.get_rect(center=(550+100//2, 275))
        self.screen.blit(label2_surface, label2_rect)
        pygame.display.flip()

    def draw_master(self, x, y, size):
        # Replace with image loading and blitting
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resource/img/room/master.png"))
        print(image_path)
        image = pygame.image.load(image_path)
        resized_image = pygame.transform.smoothscale(image, (size, size))
        self.screen.blit(resized_image, (x, y))

    def draw_member(self, x, y, size):
        # Replace with image loading and blitting
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resource/img/room/member.png"))
        print(image_path)
        image = pygame.image.load(image_path)
        resized_image = pygame.transform.smoothscale(image, (size, size))
        self.screen.blit(resized_image, (x, y))
    def draw_square(self, x, y, size, color):
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(self.screen, color, rect)

    # def kick_player(self):
    #     print("Đuổi người chơi")
    #
    # def dismiss_room(self):
    #     print("Giải tán phòng")

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
