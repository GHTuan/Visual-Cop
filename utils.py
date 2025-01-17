import pygame

def image_loader(filename = "Sprite/Zombie/placeholder.jpg",flip = True, scale = (20,20)):
    image_right = pygame.image.load(filename)
    image_right = pygame.transform.scale(image_right, scale)
    if flip: 
        image_left = pygame.transform.flip(image_right, True, False)
        return image_right, image_left
    return image_right


class StateManager:
    def __init__(self, init_state = 'intro'):
        self.state = init_state
    def get_state(self):
        return self.state
    def set_state(self, new_state):
        self.state = new_state