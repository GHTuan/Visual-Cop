import pygame
from enum import Enum

from animationFrame import PeopleAnimationFrame


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
        self.life_time = life_time  # scecond
        self.annimation = PeopleAnimationFrame()
        self.screen = screen
    
    def change_state(self, new_state):
        self.state = new_state
        
    def check_colision(self, position):
        #TODO
        image_size = self.annimation.get_curent_state().get_current_frame().get_size()
        # margin = (self.image_size[0] / 2 ,self.image_size[1])
        # center = (self.x + margin[0], self.y + margin[1])
        if position[0] > self.x and position[1] > self.y and position[0] < self.x + image_size[0] and position[1] < self.y + image_size[1]:
            print("Hit")
        else:
            print("Miss")
        
        
    def update(self):
        #TODO
            # update postion if needed
            
        self.draw()    
        pass
            
    def draw(self): # call by update function
                    # for draw anmation only
        #TODO
        if self.state == PeopleState.SPAWN:
            # if self.current_spawn_frame < len(spawn_frames):
                
                self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
                self.annimation.get_curent_state().next_frame()
                
            # else:
            #     self.changeState(PeopleState.IDLE)
        
        pass
    def canEscape(self):
        if self.life_time ==  0:
            return True
        self.life_time -= 1

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
    
    