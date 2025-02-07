import pygame

from utils import image_loader
from param import IMAGE_PATH
from sound import Sound

BLACK = (0, 0, 0)
BLUE = (0,0,160)
RED = (255,0,0)

import pygame

class HealthBar:
    def __init__(self, screen, max_hearts=3):
        self.screen = screen
        self.max_hearts = max_hearts
        self.current_hearts = max_hearts
        
        self.combatUI = image_loader(f'{IMAGE_PATH}combatUI.png', flip=False, scale=(1280, 50))
        self.heart = image_loader(f'{IMAGE_PATH}heart.png', flip=False, scale=(50, 30))

        self.heart_positions = [(25, 10), (105, 10), (185, 10)]

    def draw(self):
        self.screen.blit(self.combatUI, (0, 0))
        for i in range(self.current_hearts):
            self.screen.blit(self.heart, self.heart_positions[i])

    def lose_heart(self):
        if self.current_hearts > 0:
            self.current_hearts -= 1

    def reset(self):
        self.current_hearts = self.max_hearts


class AmmoCounter:
    def __init__(self, screen, x, y, width, height, max_ammo):
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.max_ammo = max_ammo
        self.current_ammo = max_ammo

        self.ammoImage = image_loader(f'{IMAGE_PATH}ammo.jpg', flip=False, scale=(30, 30))
        self.background = image_loader(f'{IMAGE_PATH}button.png', flip=False, scale=(width, height))
        self.empty_background = pygame.Surface((width, height))
        self.empty_background.fill((255, 0, 0)) 

        self.reset_timer = None 
        self.reset_delay = 1000
        self.waiting_for_reset = False 

        self.blink = False
        self.blink_interval = 200 
        self.last_blink_time = pygame.time.get_ticks()

    def draw(self):
        current_time = pygame.time.get_ticks()

        # Hiển thị hiệu ứng nhấp nháy khi hết đạn
        if self.current_ammo == 0:
            if current_time - self.last_blink_time >= self.blink_interval:
                self.blink = not self.blink
                self.last_blink_time = current_time

            self.screen.blit(self.empty_background if self.blink else self.background, (self.x, self.y))
        else:
            self.screen.blit(self.background, (self.x, self.y))

        for i in range(self.current_ammo):
            self.screen.blit(self.ammoImage, (self.x + 20 + i * 30, self.y + 10))

        if self.waiting_for_reset and current_time - self.reset_timer >= self.reset_delay:
            self._complete_reset()

    def shoot(self):
        if self.waiting_for_reset:
            return
        print('shot')
        if self.current_ammo > 0:
            self.current_ammo -= 1

        if self.current_ammo == 0 and not self.waiting_for_reset:
            self.reset_timer = pygame.time.get_ticks()
            self.waiting_for_reset = True

    def reset(self):
        if not self.waiting_for_reset:
            self.reset_timer = pygame.time.get_ticks()
            self.waiting_for_reset = True

    def _complete_reset(self):
        self.current_ammo = self.max_ammo
        self.waiting_for_reset = False
        self.reset_timer = None

       
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

        