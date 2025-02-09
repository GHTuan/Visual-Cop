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
        self.life_time = life_time  # second
        self.annimation = PeopleAnimationFrame()
        self.screen = screen
        self.is_dead = False
    
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
            return False
        
        
    def update(self):
        #TODO
        if self.state == PeopleState.RUN:
            # i need to change self.position here!!!
            self.x += 10

        self.draw()
            
    def draw(self): # call by update function
                    # for draw anmation only
        #TODO
        if self.state == PeopleState.SPAWN:
            # if self.annimation.get_curent_state().get_current_frame() < len(self.annimation.spawn_frame):
            self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.annimation.get_curent_state().next_frame()
                
            # else:
            # if self.annimation.get_curent_state().timer > 3000:
            self.change_state(PeopleState.IDLE)
            self.annimation.set_idle_frame()

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
    
    