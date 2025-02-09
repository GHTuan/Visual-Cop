import pygame
from enum import Enum
import random

from animationFrame import PeopleAnimationFrame
from param import IMAGE_PATH

from Sprite.spriteSheet import Spritesheet

# thiefSpriteSheet = Spritesheet(f'{IMAGE_PATH}thief/npc_thief-sheet.png')


class PeopleState(Enum):
    SPAWN = 0
    IDLE = 1
    RUN = 2
    DEAD = 3
    ESCAPE = 4
    NONE = 5

class People:
    def __init__ (self, screen, x, y, life_time = 15):
        self.state = PeopleState.SPAWN
        self.x = x
        self.y = y
        # self.screen = screen
        self.hit_time = 0
        self.escape_time = 0
        self.life_time = life_time  # second
        self.annimation = PeopleAnimationFrame()
        self.screen = screen
        self.is_dead = False
        self.state_timer_start = 0
        self.state_timer_end = random.randint(2000, 5000)
        self.check_x_moved = False
        self.check_y_moved = False
        self.direction = random.choice([-1, 1])
        self.target_x = 0
        self.target_y = 0
        self.move_speed = 2 
        self.in_road = False
    
    def change_state(self, new_state):
        self.state = new_state
        
    def check_colision(self, position):
        #TODO
        if self.is_dead:  # already dead
            return False
        
        image_size = self.annimation.get_curent_state().get_current_frame().get_size()
        # margin = (self.image_size[0] / 2 ,self.image_size[1])
        # center = (self.x + margin[0], self.y + margin[1])
        if position[0] > self.x and position[1] > self.y and position[0] < self.x + image_size[0] and position[1] < self.y + image_size[1]:
            print("Hit")
            self.change_state(PeopleState.DEAD)
            self.is_dead = True
            return True
        else:
            print("Miss")
            return False
        
        
    def update(self):
        if self.state == PeopleState.RUN:
            if not self.check_y_moved:
                if self.y >= 426:  # Floor 1
                    self.target_y = 630
                    self.check_y_moved = True
                else:  # Floor 2
                    self.target_y = 385
                    if self.check_x_moved:
                        self.target_y = 630
                    else:
                        if self.x >= 174 and self.x <= 1100:
                            if self.direction == -1:
                                self.target_x = 174
                            elif self.direction == 1:
                                self.target_x = 1100
                            # self.check_x_moved = True 
            if self.x <= 174 or self.x >= 1100:                
                self.target_y = 630 
            if self.y ==  630:
                self.in_road = True     
            else:

            #For render movement
                if self.y < self.target_y:
                    self.y += self.move_speed
                    if self.y > self.target_y:  
                        self.y = self.target_y
                elif self.x < self.target_x:
                    self.x += self.move_speed
                    if self.x > self.target_x:  
                        self.x = self.target_x
                elif self.x > self.target_x:
                    self.x -= self.move_speed
                    if self.x < self.target_x:  
                        self.x = self.target_x
                else:
                    self.in_road = True

            if self.check_y_moved and self.in_road:
            # Move left or right
                self.x += self.direction * 2 

        self.draw()
            
    def draw(self): # call by update function
                    # for draw anmation only
        #TODO

        current_clock_time = pygame.time.get_ticks()

        if self.state == PeopleState.SPAWN:
            # if self.annimation.get_curent_state().get_current_frame() < len(self.annimation.spawn_frame):
            self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.annimation.get_curent_state().next_frame()
                
            # else:
            # if self.annimation.get_curent_state().timer > 3000:
            if self.state_timer_start == 0:
                self.state_timer_start = current_clock_time

            if current_clock_time - self.state_timer_start >= self.state_timer_end:
            # if current_clock_time - self.state_timer_start >= 999000:
                self.change_state(PeopleState.IDLE)
                self.annimation.set_idle_frame()
                self.state_timer_start = 0

        elif self.state == PeopleState.IDLE:
            ###
            self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

            # if self.annimation.get_curent_state().timer > 2000:
            self.change_state(PeopleState.RUN)
            self.annimation.set_run_frame()
        
        elif self.state == PeopleState.RUN:
            ###
            self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

        elif self.state == PeopleState.DEAD:
            ###
            if not self.is_dead: 
                self.annimation.set_dead_frame()
                self.is_dead = True

            self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

        elif self.state == PeopleState.ESCAPE:
            ###
            self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

            if self.is_escape():
                print("Escaped!")

            pass
                        
        pass
    def is_escape(self):
        if self.life_time ==  0:
            return True
        self.life_time -= 1
        return False

class Thief1(People):  # Do not harm the player
    def __init__(self, screen, x, y, life_time = 15):
        super().__init__(screen, x, y, life_time)
        #TODO
            # self.annimation.set_spawn_frame(...)
            # self.annimation.set_dead_frame(...)
            # self.annimation.set_idle_frame(...)
            # ...

        pass
    

class Thief2(People):  # Does damage to the player
    pass

class Citizen(People):
    pass
    
    