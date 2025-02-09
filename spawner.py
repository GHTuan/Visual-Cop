import pygame
import random

from people import Thief1 
from object import Door, DoorState



class SpawnPoint:
    def __init__(self, screen, x, y, slot = 1):
        self.screen = screen  
        self.x = x
        self.y = y
        self.max_slot = slot
        self.slot = [] 
        self.open = DoorState.OPEN
        self.door = Door(self.screen, x, y, 45, 65)    
    def not_full(self):
        return len(self.slot) < self.max_slot
    def add_slot(self, person):
        self.slot.append(person)
    def get_people(self):
        return self.slot
    def remove_slot(self, person):
        self.slot.remove(person)
    def draw(self):
        self.door.draw(self.open)
        #TODO
    def get_cordinates(self):
        return self.x, self.y
    
class Spawner:
    def __init__(self,screen , floor = 0, spawn_min_interval = 3000, spawn_max_interval = 2000, remove_interval = 10000):
        self.screen = screen
        
        self.min_interval = spawn_min_interval
        self.max_interval = spawn_max_interval
        self.remove_interval = remove_interval
        if floor == 0:
            self.spawnpoint = [SpawnPoint(screen, 333, 495),SpawnPoint(screen, 623, 495),SpawnPoint(screen, 912, 495)]
        elif floor == 1:
            self.spawnpoint = [SpawnPoint(screen, 333, 305),SpawnPoint(screen, 623, 305),SpawnPoint(screen, 912, 305)]
        else:
            print("Invalid floor") 
        
        
        self.spawn_event = pygame.USEREVENT + 1
        
    def drawPeople(self):
        for point in self.spawnpoint:
            for person in point.get_people():
                person.update()    
    
    def drawDoor(self):
        for point in self.spawnpoint:
            point.draw()
    
    def draw(self):  #
        self.drawPeople()
        self.drawDoor()
    
    def spawn(self):
        valid_point = self.get_valid_spawnpoint()
        if not valid_point: 
            return
        
        x,y = valid_point.get_cordinates()
        
        valid_point.add_slot(Thief1(self.screen , x, y, self.screen))
        
        

    def get_valid_spawnpoint(self):
        points = [point for point in self.spawnpoint if point.not_full()]
        if points == []:
            return False
        return random.choice(points)
    
    def remove(self):
        # Check if People is dead or escaped
        
        #...
        pass
    
    
    def update(self, event):
        if event.type == self.spawn_event:
            self.spawn()
                    
    def handle_click(self, position):
        for point in self.spawnpoint:
            for person in point.get_people():
                if person.check_colision(position):
                    point.remove_slot(person)
                    return True
        return False
    
    def reset(self):
        pass
        
        