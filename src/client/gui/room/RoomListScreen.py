import pygame
from pygame.locals import *


class RoomListScreen:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Danh sách phòng")
        self.clock = pygame.time.Clock()

        content_height = 12 * 100  # Chiều cao nội dung
        scroll_speed = 5

        self.content = pygame.Surface((self.width, content_height))
        self.content.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 36)

        room_height = 100  # Chiều cao của mỗi phần tử (title, content, button)
        room_y = 10  # Vị trí y của phần tử đầu tiên

        class Element:
            def __init__(self, title, content):
                self.font = pygame.font.Font(None, 36)
                self.title = title
                self.content = content
                self.button_text = "Vào"
                self.title_surface = self.font.render(self.title, True, (0, 0, 0))
                self.content_surface = self.font.render(self.content, True, (0, 0, 0))
                self.button_surface = self.font.render(self.button_text, True, (255, 255, 255))
                self.button_rect = pygame.Rect(0, 0, 65, 40)  # Button's rectangle

            def draw(self, surface, x, y):
                surface.blit(self.title_surface, (x, y))
                surface.blit(self.content_surface, (x, y + 40))
                button_x = x + surface.get_width() - self.button_surface.get_width() - 50
                button_y = y + 10
                self.button_rect.topleft = (button_x, button_y)  # Update button's position
                pygame.draw.rect(surface, (0, 0, 255), self.button_rect)
                surface.blit(self.button_surface, (button_x + 10, button_y + 10))

        self.elements = []
        for i in range(1, 13):
            title = f"Title {i}"
            content = f"Content {i}"
            element = Element(title, content)
            self.elements.append(element)

        self.scroll_y = 0
        self.max_scroll_y = max(content_height - self.height, 0)  # Giới hạn cuộn
        # self.max_drag_distance = room_height * len(self.elements) - self.height  # Giới hạn kéo tương đương với số lượng phần tử
        self.max_drag_distance = room_height * len(
            self.elements) - self.height  # Giới hạn kéo tương đương với số lượng phần tử

        self.running = False
        self.is_dragging = False
        self.last_mouse_pos = None

    def handle_event(self, event):
        if event.type == QUIT:
            self.running = False
            exit(0)

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra sự kiện click vào button
                for element in self.elements:
                    if element.button_rect.collidepoint(event.pos):
                        print("Button Clicked!")  # Thực hiện hành động tương ứng khi button được click

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            if self.is_dragging:
                current_mouse_pos = pygame.mouse.get_pos()
                mouse_movement = current_mouse_pos[1] - self.last_mouse_pos[1]

                self.scroll_y -= mouse_movement

                # Giới hạn cuộn
                if self.scroll_y < 0:
                    self.scroll_y = 0
                elif self.scroll_y > self.max_scroll_y:
                    self.scroll_y = self.max_scroll_y

                # Giới hạn kéo tương đương với số lượng phần tử
                if self.scroll_y < 0:
                    self.scroll_y = 0
                elif self.scroll_y > self.max_drag_distance:
                    self.scroll_y = self.max_drag_distance

                self.last_mouse_pos = current_mouse_pos

            # Xóa nội dung cũ trên màn hình chính
            self.screen.fill((255, 255, 255))

            # Vẽ nội dung
            self.screen.blit(self.content, (0, -self.scroll_y))

            # Vẽ các phần tử
            for i, element in enumerate(self.elements):
                element.draw(self.screen, 10, i * 100 - self.scroll_y)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
