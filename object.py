import pygame
from enum import Enum
from param import IMAGE_PATH
from Sprite.spriteSheet import Spritesheet
from animationFrame import AnnimationFrame

doorSpriteSheet = Spritesheet(f'{IMAGE_PATH}door/door.png')

open_frames = [
    # doorSpriteSheet.parse_sprite('close'),
    doorSpriteSheet.parse_sprite('open')
]

close_frames = [
    # doorSpriteSheet.parse_sprite('open'), 
    doorSpriteSheet.parse_sprite('close')
]

class DoorState(Enum):
    CLOSE = 0
    OPEN = 1
    NONE = 2

class Door:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        
        self.animations = {
            DoorState.OPEN: AnnimationFrame(open_frames, interval=500),
            DoorState.CLOSE: AnnimationFrame(close_frames, interval=500)
        }
        
        self.current_state = DoorState.CLOSE

    def update_animation(self, state):
        """Cập nhật animation nếu trạng thái thay đổi."""
        if state in self.animations and self.current_state != state:
            self.animations[state].next_frame()
    
    def draw(self, state):
        """Vẽ cánh cửa lên màn hình."""
        if state not in self.animations:
            return  # Tránh lỗi nếu truyền state không hợp lệ
        
        self.update_animation(state)  # Cập nhật animation nếu cần
        current_image = self.animations[state].get_current_frame()
        
        self.screen.blit(
            pygame.transform.scale(current_image, (self.width, self.height)), 
            (self.x, self.y)
        )
        
        self.current_state = state  # Lưu trạng thái hiện tại
