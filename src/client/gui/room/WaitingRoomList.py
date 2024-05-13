import asyncio
import os
import sys
import pygame
from pygame.locals import *

from src.client.gui.room.WaitRoomMember import WaitRoomMember
from src.client.handle.RoomRequest import RoomRequest


class WaitingRoomList:
    rooms = []
    def __init__(self, player_name):
        pygame.init()
        self.player_name = player_name
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Danh sách phòng")
        self.clock = pygame.time.Clock()

        self.content_height = 6 * 100  # Chiều cao nội dung
        self.scroll_speed = 5
        self.room_height = 100  # Chiều cao của mỗi phần tử (title, content, button)
        self.room_y = 10  # Vị trí y của phần tử đầu tiên
        self.content = pygame.Surface((self.width,  self.content_height))
        self.content.fill((255, 255, 255))
        grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(grandparent_directory, 'ready', 'Arial.ttf')
        self.font = pygame.font.Font(font_path, 28)

        self.elements = []
        for i in range(1, 13):
            title = f"Title {i}"
            content = f"Content {i}"
            element = Element(title, content)
            self.elements.append(element)

        self.scroll_y = 0
        self.max_scroll_y = max(self.content_height - self.height, 0)  # Giới hạn cuộn
        self.max_drag_distance = self.room_height * len(self.elements) - self.height  # Giới hạn kéo tương đương với số lượng phần tử

        self.running = False
        self.is_dragging = False
        self.last_mouse_pos = None

    async def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()  # Đảm bảo Pygame được giải phóng trước khi kết thúc
                exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra sự kiện click vào button
                for element in self.elements:
                    if element.button_rect.collidepoint(event.pos):
                        print("Đã click vào button nhưng không đáng kể")
                        room_id = element.title.split(': ')[1].__str__()
                        master_name = None  # Khởi tạo master_name là None
                        print(WaitingRoomList.rooms)
                        for room in WaitingRoomList.rooms:
                            if room['room_id'].__str__() == room_id:
                                for member in room['members']:
                                    if member['role'] == 'master':
                                        master_name = member['user_name']
                                        break
                        if master_name is None:
                            master_name = 'Unknown'  # Nếu không tìm thấy master, gán giá trị là 'Unknown'
                        print(room_id)
                        print(master_name)
                        await RoomRequest().join_room(room_id)
                        await WaitRoomMember(master_name, self.player_name).run()
                if self.btr.collidepoint(event.pos):
                    self.running = False
                    print("Button Trở về Clicked!")  #
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False

    async def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                await self.handle_event(event)

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
            self.screen.blit(self.content, (0, - self.scroll_y))
            blame = await RoomRequest().get()
            if len(blame['rooms']) > 0:
                self.elements = []
                WaitingRoomList.rooms = blame['rooms']
                for room in blame['rooms']:
                    room_id = room['room_id']
                    member_count = len(room['members'])
                    title = f"Room ID: {room_id}"
                    content = f"Member Count: {member_count}"
                    element = Element(title, content)
                    self.elements.append(element)
                self.room_y = 20
                self.scroll_y = 0
                self.content_height = len(self.elements) * self.room_height  # Chiều cao nội dung
                self.max_scroll_y = max(self.content_height - self.height, 0)  # Giới hạn cuộn
                self.max_drag_distance = self.room_height * len(self.elements) - self.height
                # Vẽ các phần tử
                for i, element in enumerate(self.elements):
                    element.draw(self.screen, 10, i * 100 - self.scroll_y)
                pass
            else:
                self.no_players_label = pygame.font.Font(None, 36).render("No Players", True, (0, 0, 0))
                self.no_players_rect = self.no_players_label.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(self.no_players_label, self.no_players_rect)
            # Vẽ button
            self.btr = pygame.Rect(self.width/2-50, self.height-60, 110, 45)
            pygame.draw.rect(self.screen, (0, 0, 0), self.btr)
            button_text = self.font.render("Trở về", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=self.btr.center)
            self.screen.blit(button_text, button_text_rect)
            pygame.display.flip()
            self.clock.tick(60)
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