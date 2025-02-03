import pygame

BLACK = (0, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,250,160)

class HealthBar:
    def __init__(self, x, y, width, height, color, max_health):
        pass
        #TODO
    def draw():
        pass
        #TODO

class AmmoCounter:
    def __init__(self):
        pass
        #TODO
    def draw():
        pass
        #TODO
        
class Button:
    def __init__(self, screen, x, y, width, height, text = "PlaceHolder" ,image = None):
        # self.x = x
        # self.y = y
        # self.width = width
        # self.height = height
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        
        self.text = self.font.render(text, True, WHITE)
        self.hover_text =  self.font.render(text, True, YELLOW)
        
        self.screen = screen
        self.clicked = False
        if image == None:
            self.rect = pygame.Rect(x, y, width, height)
            self.background = False
        else:
            self.image = image
            self.rect = self.image.get_rect()
            self.background = True
        self.rect.topleft = x, y
    def draw(self):
        action = False
        
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            renderText = self.hover_text
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            renderText = self.text
        
        if self.background:
            self.screen.blit(self.image, self.rect.center)
        rectangle = renderText.get_rect(center=self.rect.center)
        self.screen.blit(renderText, rectangle)
        
        return action

        