import pygame

from utils import image_loader
from param import IMAGE_PATH
from sound import Sound

BLACK = (0, 0, 0)
BLUE = (0,0,160)
RED = (255,0,0)

# class Image:
#     def __init__(self):
#         self.combatUI = image_loader(f'{IMAGE_PATH}combatUI.png', flip = False, scale = (1280, 20))
#         self.heart = image_loader(f'{IMAGE_PATH}heart.png', flip = False, scale = (15, 15))
   
# image = Image()

class HealthBar:
    def __init__(self, screen):
        self.screen = screen
        self.combatUI = image_loader(f'{IMAGE_PATH}combatUI.png', flip = False, scale = (1280, 50))
        self.heart = image_loader(f'{IMAGE_PATH}heart.png', flip = False, scale = (50, 30)) 

    def draw(self):
        self.screen.blit(self.combatUI,(0,0))
        self.screen.blit(self.heart,(25,10))
        self.screen.blit(self.heart,(105,10))
        self.screen.blit(self.heart,(185,10))

class AmmoCounter:
    def __init__(self):
        pass
        #TODO
    def draw():
        pass
        #TODO
        
class Button:
    def __init__(self, screen, x, y, width, height, text = "PlaceHolder" ,image = None):

        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        
        self.text = self.font.render(text, True, BLUE)
        self.hover_text =  self.font.render(text, True, RED)
        
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
            self.screen.blit(self.image, self.rect.topleft)
        rectangle = renderText.get_rect(center=self.rect.center)
        self.screen.blit(renderText, rectangle)
        
        return action
    
    def drawVolumeButton(self):
        action = False
        if Sound.SOUND_OFF:
            self.text = self.font.render('Volume: Off', True, BLUE)
            self.hover_text =  self.font.render('Volume: Off', True, RED)
        else:
            self.text = self.font.render('Volume: On', True, BLUE)
            self.hover_text =  self.font.render('Volume: On', True, RED)
     
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            renderText = self.hover_text
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                Sound.SOUND_OFF = not Sound.SOUND_OFF
                if Sound.SOUND_OFF:
                    Sound.turnOff('background')
                else:
                    Sound.turnOn('background')
                
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            renderText = self.text
        
        if self.background:
            self.screen.blit(self.image, self.rect.topleft)
        rectangle = renderText.get_rect(center=self.rect.center)
        self.screen.blit(renderText, rectangle)
        
        return action

        