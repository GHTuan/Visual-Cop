import pygame
import json

class Spritesheet:
    def __init__(self, filePath):
        self.filePath = filePath
        self.sprite_sheet = pygame.image.load(filePath).convert_alpha()
        json_path = self.filePath.replace('.png', '.json')
        with open(json_path) as f:
            self.data = json.load(f)

    def get_sprite(self, x, y, w, h, flip = False):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return pygame.transform.flip(sprite, True, False) if flip else sprite

    def parse_sprite(self, name):
        sprite_info = self.data.get(name)
        if not sprite_info:
            raise ValueError(f"Sprite '{name}' không tồn tại trong metadata.")
        
        frame = sprite_info["frame"]
        return self.get_sprite(frame["x"], frame["y"], frame["w"], frame["h"], sprite_info.get("flip", False))
