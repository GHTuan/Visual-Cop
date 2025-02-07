import pygame
import sys
import random

from param import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME
from utils import image_loader

from people import Thief1
from spawner import Spawner
from gun import Gun

from UI import Button

BLACK = (0, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,250,160)

GAME_TIME = 30

SCREEN_SIZE = ((SCREEN_WIDTH, SCREEN_HEIGHT))

window = pygame.display.set_mode(SCREEN_SIZE)

class Background:
    def __init__(self):
        self.background = image_loader('Sprite/Temp/building1.png', flip = False, scale = SCREEN_SIZE) # Background image
        self.menu = image_loader('Sprite/Temp/menu.png', flip = False, scale = SCREEN_SIZE)  # Menu image
        self.sword = image_loader('Sprite/Temp/sword.png', flip = False, scale = (15,15))  # Sword image
        self.click_sword = image_loader('Sprite/Temp/click_sword.png', flip = False, scale = (15,15)) # Click sword image
        self.pause = image_loader('Sprite/Temp/pause.png', flip = False, scale = (20,20)) # Pause image
        self.pause_background = image_loader('Sprite/Temp/pause_bg.png', flip = False, scale = SCREEN_SIZE) # Pause background image
        self.game_over = image_loader('Sprite/Temp/game_over.png', flip = False, scale = SCREEN_SIZE) # Game over image

background = Background()


class Intro:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        # time variables
        self.interval = 100 # in milliseconds
        self.current = pygame.time.get_ticks() # time count tu luc lib pygame duoc chay den thoi diem hien tai
        self.next = self.current + self.interval
        self.index = 0
        
        self.curtain = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.curtain.fill(BLACK)
        self.alpha = 0;
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        self.current = pygame.time.get_ticks()
        if self.current > self.next and self.index < len(GAME_NAME):
            self.next = self.current + self.interval
            self.index += 1
            # sound.turnOn('click');
            
        if any(pygame.key.get_pressed()) or any(pygame.mouse.get_pressed()):
            self.state.set_state('menu')  # switch screen
            # sound.turnOn('background')
                
        self.screen.fill(BLACK)
        rendered_text = self.font.render(GAME_NAME[:self.index], True, WHITE)
        rectangle = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(rendered_text, rectangle)
        
        if self.index >= len(GAME_NAME):
            self.alpha += 5
            self.curtain.set_alpha(self.alpha)
            if self.alpha > 255:
                self.state.set_state('menu')
                # sound.turnOn('background')
            self.screen.blit(self.curtain, (0, 0))   
            # sound.turnOff('click')
    
class Menu:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.quit_hangover = False
        self.play_hangover = False
        self.volume_hangover = False
        
        self.playButton = Button(self.screen,285,514,515-285,596-514, "Play Game")
        self.quitButton = Button(self.screen,29,473,258-29,555-473, "Quit Game")
    def run(self):
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(background.menu, (0, 0))
        
        if self.playButton.draw():
            self.state.set_state('play_game')
        if self.quitButton.draw():
            pygame.quit()
            sys.exit()
        
        # self.screen.blit(self.volume_text, (574, 490))
        window.blit(self.screen, (0,0))
        pygame.display.update()


class GameOver:
    def __init__(self, screen, state, play_game):
        self.screen = screen
        self.state = state
        self.play_game = play_game
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.game_over_center = background.game_over.get_rect().center
        self.transition_speed = 10
        self.menu_hangover = False
        self.play_again_hangover = False
        self.menu_text = self.font.render("Menu", True, WHITE)
        self.play_again_text = self.font.render("Play Again", True, WHITE)
    def run(self):
        pygame.mouse.set_visible(True)
        mouse = pygame.mouse.get_pos()
        
        if 285 <= mouse[0] <= 515 and 405 <= mouse[1] <= 488:
            self.play_again_hangover = True
        else:
            self.play_again_hangover = False
        if 285 <= mouse[0] <= 515 and 510 <= mouse[1] <= 593:
            self.menu_hangover = True
        else:
            self.menu_hangover = False
        
        if self.menu_hangover:
            self.menu_text = self.font.render("Menu", True, YELLOW)
        else: 
            self.menu_text = self.font.render("Menu", True, WHITE)
        if self.play_again_hangover:
            self.play_again_text = self.font.render("Play Again", True, YELLOW)
        else:
            self.play_again_text = self.font.render("Play Again", True, WHITE)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 285 <= mouse[0] <= 515 and 405 <= mouse[1] <= 488:
                        self.state.set_state('play_game')
                        # self.play_game.reset_state()
                    if 285 <= mouse[0] <= 515 and 510 <= mouse[1] <= 593:
                        self.state.set_state('menu')
                        # self.play_game.reset_state()
        
        self.screen.blit(background.game_over, (0, 0))
        self.screen.blit(self.play_again_text, (318, 420))
        self.screen.blit(self.menu_text, (360, 525))
        
        score_text = self.font.render("Score: " + str(self.play_game.getScore()), True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        missed_text = self.font.render("Missed: " + str(self.play_game.escape_count), True, WHITE)
        missed_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(missed_text, missed_rect)

class PauseGame:
    def __init__(self, screen, state, play_game):
        self.screen = screen
        self.state = state
        self.play_game = play_game
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.pause_center = background.pause.get_rect().center
        self.transition_speed = 10
        self.resume_hangover = False
        self.menu_hangover = False
        self.resume_text = self.font.render("Resume", True, WHITE)
        self.menu_text = self.font.render("Menu", True, WHITE)
    def run(self):
        pygame.mouse.set_visible(True)
        mouse = pygame.mouse.get_pos()
        
        if 285 <= mouse[0] <= 515 and 292 <= mouse[1] <= 375:
            self.resume_hangover = True
        else:
            self.resume_hangover = False
        if 285 <= mouse[0] <= 515 and 397 <= mouse[1] <= 480:
            self.menu_hangover = True
        else:
            self.menu_hangover = False
        
        if self.resume_hangover:
            self.resume_text = self.font.render("Resume", True, YELLOW)
        else: 
            self.resume_text = self.font.render("Resume", True, WHITE)
        if self.menu_hangover:
            self.menu_text = self.font.render("Menu", True, YELLOW)
        else:
            self.menu_text = self.font.render("Menu", True, WHITE)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 285 <= mouse[0] <= 515 and 292 <= mouse[1] <= 375:
                        self.state.set_state('play_game')
                    if 285 <= mouse[0] <= 515 and 397 <= mouse[1] <= 480:
                        self.state.set_state('menu')
                        # self.play_game.reset_state()
        
        self.screen.blit(background.pause_background, (0, 0))
        self.screen.blit(self.resume_text, (338, 310))
        self.screen.blit(self.menu_text, (360, 415))
        
        
# --------------------------------------------------------------
# ---------------   Big Game Play Here =))  --------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

class PlayGame:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.period = GAME_TIME
        self.countdown = self.period
        #self.graves = [(195, 64), (516, 116), (143, 328), (625 , 328), (413, 434), (200 , 540), (571, 596)]
        
        self.cursor_img = background.sword
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
        
        self.spawners = [Spawner(screen)]
        self.gun = Gun(5)
        
        pygame.time.set_timer(self.generate_zombie, self.appear_interval)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.set_timer(self.remove_interval, 1000)
        
        

    
    def handle_click(self,position):
        print('Click at: ', position[0], position[1])
        
        print(self.gun.get_current_ammo())

        if self.gun.fire():
            for spawner in self.spawners:
                if spawner.handle_click(position):
                    self.score += 1
        else:
            print("Out of ammo!")
        

        
    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor_img = background.click_sword
                    click_position = pygame.mouse.get_pos()
                    if self.pause_icon_rect.collidepoint(click_position):
                        self.state.set_state('pause')
                    else:
                        self.handle_click(click_position)
                        # if not TURN_OFF_SOUND:
                        #     sound.turnOn('sword')
            else:
                self.cursor_img = background.sword
                    
           
            if event.type == self.remove_interval:
                # self.removeZombie()
                pass
                
            if event.type == pygame.USEREVENT:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.people.clear()
                    self.state.set_state('game_over')
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.state.set_state('pause')
                if event.key == pygame.K_r:
                    self.gun.reload()
            
            for spawner in self.spawners:
                spawner.update(event)
        
        self.screen.blit(background.background, (0, 0))
        self.screen.blit(self.pause_icon, (740, 15))
        
        # self.displayScore()
        # self.displayMissed()
        # self.displayTime()
        for spawner in self.spawners:
            spawner.draw()
        
        pygame.mouse.set_visible(False)
        self.cursor_rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_rect)
        
        
    
    def reset_game(self):
        pass
        #TODO        