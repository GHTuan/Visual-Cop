import pygame

from utils import image_loader
from param import IMAGE_PATH
from sound import Sound

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,160)
RED = (255,0,0)

class HealthBar:
    def __init__(self, screen, max_hearts=3):
        self.screen = screen
        self.max_hearts = max_hearts
        self.current_hearts = max_hearts  

        self.combatUI = image_loader(f'{IMAGE_PATH}combatUI.png', flip=False, scale=(1280, 50))
        self.heart = image_loader(f'{IMAGE_PATH}heart.png', flip=False, scale=(50, 30))
        
        self.heart_positions = [(25 + i * 80, 10) for i in range(max_hearts)]

    def draw(self):
        self.screen.blit(self.combatUI, (0, 0))
        for i in range(self.current_hearts):
            self.screen.blit(self.heart, self.heart_positions[i])

    def get_current_hearts(self):
        return self.current_hearts

    def set_current_hearts(self, hearts):
        self.current_hearts = max(0, min(hearts, self.max_hearts))


class AmmoCounter:
    def __init__(self, screen, x, y, width, height, max_ammo):
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.max_ammo = max_ammo

        self.ammoImage = image_loader(f'{IMAGE_PATH}ammo.jpg', flip=False, scale=(30, 30))
        self.background = image_loader(f'{IMAGE_PATH}button.png', flip=False, scale=(width, height))

    def draw(self, current_ammo):
        current_ammo = min(current_ammo, self.max_ammo)
        
        self.screen.blit(self.background, (self.x, self.y))
        for i in range(current_ammo):
            self.screen.blit(self.ammoImage, (self.x + 20 + i * 30, self.y + 10))

       
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

class ScoreDisplay:
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.x = 20
        self.y = 50
    def draw(self,score):
        display_text = self.font.render("Score: " + str(score), True, WHITE)
        self.screen.blit(display_text,(self.x,self.y))

class MissDisplay:
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.x = 20
        self.y = 80
    def draw(self,miss):
        display_text = self.font.render("Miss: " + str(miss), True, WHITE)
        self.screen.blit(display_text,(self.x,self.y))
        