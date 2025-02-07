import pygame
import json

class Spritesheet:
    def __init__(self, filePath):
        pygame.display.init()
        self.filePath = filePath
        self.sprite_sheet = pygame.image.load(filePath).convert_alpha()
        self.meta_data = self.filePath.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data[name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image
