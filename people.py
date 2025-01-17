import pygame
from enum import Enum

from animationFrame import AnimationFrame


class PeopleState(Enum):
    SPAWN = 0
    IDLE = 1
    RUN = 2
    DEAD = 3
    ESCAPE = 4
    NONE = 5

class People:
    def __init__ (self, x, y, screen, frame,  life_time = 15):
        self.state = PeopleState.SPAWN
        self.x = x
        self.y = y
        self.screen = screen
        self.hit_time = 0
        self.escape_time = 0
        self.life_time = life_time  # scecond
        self.current_spawn_frame = 0
        self.current_idle_frame = 0
        self.current_dead_frame = 0
        self.current_escape_frame = 0
    
    def changeState(self, new_state):
        self.state = new_state
        
    def update(self):
        #TODO
            # update postion if needed
            
        self.draw()    
        pass
            
    def draw(self): # call by update function
                    # for draw anmation only
        #TODO
        
        
        pass
    def canEscape(self):
        if self.life_time ==  0:
            return True
        self.life_time -= 1

class Thief1(People):  # Do not harm the player
    pass

class Thief2(People):  # Does damage to the player
    pass

class Citizen(People):
    pass
    
    