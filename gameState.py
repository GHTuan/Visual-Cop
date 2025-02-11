import pygame
import sys
import random

from param import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, IMAGE_PATH
from utils import image_loader



from gun import Gun

from UI import Button, HealthBar, ScoreDisplay, MissDisplay
from sound import Sound

BLACK = (0, 0, 0)
WHITE = (255,255,255)
BLUE = (0,0,160)

GAME_TIME = 30

SCREEN_SIZE = ((SCREEN_WIDTH, SCREEN_HEIGHT))

window = pygame.display.set_mode(SCREEN_SIZE)

from spawner import Spawner

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
   
    # Begin Test

    # End Test

    def run(self):
              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Begin Test

            # End Test

        self.screen.blit(background.menu, (0, 0))
        self.screen.blit(background.logo, (400, 100))

        if self.playButton.draw():
            self.state.set_state('play_game')

        self.volumeButton.drawVolumeButton()

        if self.quitButton.draw():
            pygame.quit()
            sys.exit()
        
        window.blit(self.screen, (0,0))


    # Begin Test

    # End Test


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
            self.play_game.reset_game()
            self.state.set_state('play_game')

        if self.menuButton.draw():
            self.play_game.reset_game()
            self.state.set_state('menu')

        
# Please fix
        score_text = self.font.render("Score: " + str(self.play_game.get_score()), True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        missed_text = self.font.render("Missed: " + str(self.play_game.get_miss()), True, WHITE)
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
            self.play_game.reset_game()
            self.state.set_state('menu')
        


        
        
# --------------------------------------------------------------
# ---------------   Big Game Play Here =))  --------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

class PlayGame:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

        self.graves = [(195, 64), (516, 116), (143, 328), (625 , 328), (413, 434), (200 , 540), (571, 596)]
        
        self.cursor_img = background.crosshair
        self.cursor_rect = self.cursor_img.get_rect()
        self.pause_icon = background.pause
        self.pause_icon_rect = self.pause_icon.get_rect(topleft=(1240, 15))
        
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.score = 0
        self.miss = 0
        self.people = []
        self.spawn_event = pygame.USEREVENT + 1
        self.remove_event = pygame.USEREVENT + 2
        self.appear_interval = 2000
        self.escape_count = 0
        self.max_heart = 3

        self.heartBar = HealthBar(self.screen,self.max_heart)         
        self.spawners = [Spawner(screen), Spawner(screen, floor=1)]
        self.gun = Gun(screen, ammo_capacity=10)
        self.score_display = ScoreDisplay(screen)
        self.miss_display = MissDisplay(screen)
        
        pygame.time.set_timer(self.spawn_event, self.appear_interval)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.set_timer(self.remove_event, 1000)
        


    
    def handle_click(self,position):
        if self.gun.fire():
            for spawner in self.spawners:
                check = spawner.handle_click(position)
                if check == 1:
                    self.score += 1
                    return
                elif check == 2:
                    self.heartBar.set_current_hearts(self.heartBar.get_current_hearts() - 1)
                    self.check_gameover()
                    return
            self.miss += 1


    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_position = pygame.mouse.get_pos()
                    if self.pause_icon_rect.collidepoint(click_position):
                        self.state.set_state('pause')
                    else:
                        self.handle_click(click_position)
                        # if not TURN_OFF_SOUND:
                        #     sound.turnOn('crosshair')

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.gun.reload()

            else:
                self.cursor_img = background.crosshair
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.state.set_state('pause')
                if event.key == pygame.K_r:
                    self.gun.reload()
            
            for spawner in self.spawners:
                if spawner.update(event):
                    self.handle_escape()
        
        self.screen.blit(background.background, (0, 0))


        screen_rect = self.screen.get_rect()
        building_rect = background.building.get_rect()

        # Tính toán tọa độ để đặt building chính giữa screen
        building_rect.center = screen_rect.center

        # Vẽ hình ảnh building vào screen
        self.screen.blit(background.building, building_rect.topleft)

        # Vẽ heart bar and ammo
        self.heartBar.draw()
        self.gun.draw_ammo()

        self.screen.blit(self.pause_icon, (1240, 15))
        
        self.score_display.draw(self.score)
        self.miss_display.draw(self.miss)
        
        for spawner in self.spawners:
            spawner.draw()
        
        pygame.mouse.set_visible(False)
        self.cursor_rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_rect)
        
        
    
    def reset_game(self):
        """Reset toàn bộ trạng thái của trò chơi."""
        for spawner in self.spawners:
            spawner.reset()

        self.score = 0
        self.escape_count = 0
        self.gun.reload()
        self.heartBar.set_current_hearts(self.max_heart)
    def handle_escape(self):
        self.heartBar.set_current_hearts(self.heartBar.get_current_hearts() - 1)
        self.check_gameover()
    def check_gameover(self):
        if self.heartBar.get_current_hearts() <= 0:
            self.state.set_state('game_over')
    def get_score(self):
        return self.score
    def get_miss(self):
        return self.miss