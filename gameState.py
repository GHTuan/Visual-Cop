import pygame
import sys
import random

from param import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, IMAGE_PATH
from utils import image_loader

from people import Thief1

from UI import Button, HealthBar, AmmoCounter
from sound import Sound

BLACK = (0, 0, 0)
WHITE = (255,255,255)
BLUE = (0,0,160)

GAME_TIME = 30

SCREEN_SIZE = ((SCREEN_WIDTH, SCREEN_HEIGHT))

window = pygame.display.set_mode(SCREEN_SIZE)

class Background:
    def __init__(self):
        self.background = image_loader(f'{IMAGE_PATH}background.png', flip = False, scale = SCREEN_SIZE)
        self.building = image_loader(f'{IMAGE_PATH}building1.png', flip = False, scale = (1000, 480))
        
        self.menu = image_loader(f'{IMAGE_PATH}background.png', flip = False, scale = SCREEN_SIZE)
        self.logo = image_loader(f'{IMAGE_PATH}logo.png', flip = False, scale = (480, 300))
        
        self.crosshair = image_loader('Sprite/crosshair.png', flip=False, scale=(25, 25))
        
        # self.click_sword = image_loader('Sprite/Temp/click_sword.png', flip = False, scale = (15, 15))
        
        self.pause = image_loader(f'{IMAGE_PATH}pause.png', flip = False, scale = (20, 20)) 
        
        self.pause_background = image_loader(f'{IMAGE_PATH}pause-pixel_game.png', flip = False, scale = SCREEN_SIZE) 
        
        self.game_over = image_loader(f'{IMAGE_PATH}gameover.png', flip = False, scale = (680, 300)) 
        
        self.button = image_loader(f'{IMAGE_PATH}button.png', flip = False, scale= (250, 75))

background = Background()


class Intro:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

        self.font = pygame.font.Font('fonts/m5x7.ttf', 200)

        self.interval = 100 # in milliseconds
        self.current = pygame.time.get_ticks()
        self.next = self.current + self.interval
        self.index = 0
        
        self.curtain = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.curtain.fill(BLACK)
        self.alpha = 0

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        self.current = pygame.time.get_ticks()
        if self.current > self.next and self.index < len(GAME_NAME):
            self.next = self.current + self.interval
            self.index += 1
            Sound.turnOn('intro')
            
        if any(pygame.key.get_pressed()) or any(pygame.mouse.get_pressed()):
            self.state.set_state('menu')
            Sound.turnOn('background')
                
        self.screen.fill(BLACK)
        rendered_text = self.font.render(GAME_NAME[:self.index], True, WHITE)
        rectangle = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(rendered_text, rectangle)
        
        if self.index >= len(GAME_NAME):
            self.alpha += 5
            self.curtain.set_alpha(self.alpha)
            if self.alpha > 255:
                self.state.set_state('menu')
                Sound.turnOn('background')
            self.screen.blit(self.curtain, (0, 0))   
            Sound.turnOff('intro')
    
class Menu:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

        self.playButton = Button(self.screen, 100, 515, 250, 75, "Play Game", background.button)
        self.volumeButton = Button(self.screen, 500, 514, 250, 75, "Volume: On", background.button)
        self.quitButton = Button(self.screen, 900, 515, 250, 75, "Quit Game", background.button)
   
    def run(self):
              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(background.menu, (0, 0))
        self.screen.blit(background.logo, (400, 100))

        if self.playButton.draw():
            self.state.set_state('play_game')

        self.volumeButton.drawVolumeButton()

        if self.quitButton.draw():
            pygame.quit()
            sys.exit()
        
        window.blit(self.screen, (0,0))
        pygame.display.update()


class GameOver:
    def __init__(self, screen, state, play_game):
        self.screen = screen
        self.state = state

        self.play_game = play_game

        self.font = pygame.font.Font('fonts/m5x7.ttf', 75)
    

        self.menuButton = Button(self.screen, 260, 500, 250, 75, "Menu", background.button)
        self.playAgainButton = Button(self.screen, 770, 500, 250, 75, "Play again", background.button)

    def run(self):
        pygame.mouse.set_visible(True)
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
       
        self.screen.blit(background.game_over, (300, 0))

        if self.playAgainButton.draw():
            self.state.set_state('play_game')

        if self.menuButton.draw():
            self.state.set_state('menu')

        
# Please fix
        # score_text = self.font.render("Score: " + str(self.play_game.getScore()), True, WHITE)
        score_text = self.font.render("Score: 1", True, BLUE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # missed_text = self.font.render("Missed: " + str(self.play_game.escape_count), True, WHITE)
        missed_text = self.font.render("Missed: 1", True, BLUE)
        missed_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(missed_text, missed_rect)

class PauseGame:
    def __init__(self, screen, state, play_game):
        self.screen = screen
        self.state = state

        self.play_game = play_game

        self.resumeButton= Button(self.screen, 515, 380, 250, 75, "Resume", background.button)
        self.menuButton = Button(self.screen, 515, 520, 250, 75, "Menu", background.button)

    def run(self):
        pygame.mouse.set_visible(True)       
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(background.pause_background, (0, 0))
                
        if self.resumeButton.draw():
            self.state.set_state('play_game')

        if self.menuButton.draw():
            self.state.set_state('menu')
        


        
        
# --------------------------------------------------------------
# ---------------   Big Game Play Here =))  --------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

#  Test sprite sheet
from Sprite.spriteSheet import Spritesheet
door_spritesheet = Spritesheet(f'{IMAGE_PATH}/door/door.png')
open_frame = [
    door_spritesheet.parse_sprite('open')
]
close_frame = [
    door_spritesheet.parse_sprite('close')
]


class PlayGame:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

        # self.period = GAME_TIME
        # self.countdown = self.period

        self.graves = [(195, 64), (516, 116), (143, 328), (625 , 328), (413, 434), (200 , 540), (571, 596)]
        

        # self.doorPositions = [(100, 100)]
        
        self.cursor_img = background.crosshair
        self.cursor_rect = self.cursor_img.get_rect()
        self.pause_icon = background.pause
        self.pause_icon_rect = self.pause_icon.get_rect(topleft=(750, 10))
        
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.score = 0
        self.people = []
        self.generate_zombie = pygame.USEREVENT + 1
        self.appear_interval = 2000
        self.remove_interval = 2
        self.escape_count = 0
        
        pygame.time.set_timer(self.generate_zombie, self.appear_interval)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.set_timer(self.remove_interval, 1000)
        
        self.heartBar = HealthBar(self.screen) 
        self.ammo_counter = AmmoCounter(self.screen, 900, 650, 340, 50, max_ammo=10)
        
        
    def drawPeople(self):
        for person in self.people:
            person.update()
            
            
    def spawn_new_people(self):
        new_position = ()

        index = random.randint(0, 6)
        new_position = self.graves[index]

        return new_position
    
    def handle_click(self,position):
        print('Click at: ', position[0], position[1])
        
        for person in self.people:
            if person.check_colision(position):
                self.score += 1
                self.people.remove(person)
                break
        
        # TODO
        pass


    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:


                    # Test heartBar and ammo counter
                    self.heartBar.lose_heart()
                    self.ammo_counter.shoot()



                    # self.cursor_img = background.click_sword
                    click_position = pygame.mouse.get_pos()
                    if self.pause_icon_rect.collidepoint(click_position):
                        self.state.set_state('pause')
                    else:
                        self.handle_click(click_position)
                        # if not TURN_OFF_SOUND:
                        #     sound.turnOn('crosshair')

            #Test reset ammo
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.ammo_counter.reset()

            # Test Game over
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                self.state.set_state('game_over')


            else:
                self.cursor_img = background.crosshair
                    
            if event.type == self.generate_zombie:
                if len(self.people) < 7:
                    new_position = self.spawn_new_people()
                    self.people.append(Thief1(self.screen ,new_position[0], new_position[1], self.screen))
            if event.type == self.remove_interval:
                # self.removeZombie()
                pass
                
            # if event.type == pygame.USEREVENT:
            #     self.countdown -= 1
            #     if self.countdown <= 0:
            #         # self.zombies.clear()
            #         self.state.set_state('game_over')
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.state.set_state('pause')
        
        self.screen.blit(background.background, (0, 0))


        screen_rect = self.screen.get_rect()
        building_rect = background.building.get_rect()

        # Tính toán tọa độ để đặt building chính giữa screen
        building_rect.center = screen_rect.center

        # Vẽ hình ảnh building vào screen
        self.screen.blit(background.building, building_rect.topleft)

        frame = pygame.transform.scale(close_frame[int(0)],(100,100))
        self.screen.blit(frame, (300,300))

        self.screen.blit(self.pause_icon, (740, 15))
        self.drawPeople()

        # Heart Bar test

        self.heartBar.draw()
        self.ammo_counter.draw()

        # Ammo Counter test
        
        # self.displayScore()
        # self.displayMissed()
        # self.displayTime()
        
        pygame.mouse.set_visible(False)
        self.cursor_rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_rect)
        
        

    
    def reset_game(self):
        pass
        #TODO        