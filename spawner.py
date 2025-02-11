import pygame
import random

from people import Thief1, PeopleState, Citizen
from object import Door, DoorState

class SpawnPoint:
    def __init__(self, screen, x, y, slot=1):
        self.screen = screen  
        self.x = x
        self.y = y
        self.max_slot = slot
        self.slot = []  
        self.door = Door(self.screen, x, y, 45, 65)    
        self.door_state = DoorState.CLOSE 

    def not_full(self):
        return len(self.slot) < self.max_slot

    def add_slot(self, person):
        if self.not_full():
            self.slot.append(person)
            self.open_door()  # Mở cửa khi nhân vật xuất hiện

    def remove_slot(self, person):
        if person in self.slot:
            self.slot.remove(person)

    def get_people(self):
        return self.slot

    def open_door(self):
        self.door_state = DoorState.OPEN

    def close_door(self):
        self.door_state = DoorState.CLOSE

    def is_person_near_door(self):
        """Kiểm tra xem có nhân vật nào vẫn còn gần cửa không."""
        for person in self.slot:
            if abs(person.x - self.x) <= 50:  # Khoảng cách nhỏ => vẫn gần cửa
                return True
        return False

    def update_door_state(self):
        """Đóng cửa nếu không còn nhân vật nào đứng gần."""
        if not self.is_person_near_door():
            self.close_door()

    def draw(self):
        self.door.draw(self.door_state)
        for person in self.slot:
            person.update()
        self.update_door_state()  # Kiểm tra và đóng cửa nếu cần

    def get_coordinates(self):
        return self.x, self.y
    
class Spawner:
    def __init__(self, screen, floor=0, spawn_min_interval=3000, spawn_max_interval=2000, remove_interval=10000):
        self.screen = screen
        
        self.min_interval = spawn_min_interval
        self.max_interval = spawn_max_interval
        self.remove_interval = remove_interval
        self.remove_event = pygame.USEREVENT + 2
        self.spawn_event = pygame.USEREVENT + 1
        
        if floor == 0:
            self.spawnpoints = [
                SpawnPoint(screen, 333, 495),
                SpawnPoint(screen, 623, 495),
                SpawnPoint(screen, 912, 495)
            ]
        elif floor == 1:
            self.spawnpoints = [
                SpawnPoint(screen, 333, 305),
                SpawnPoint(screen, 623, 305),
                SpawnPoint(screen, 912, 305)
            ]
        else:
            print("Invalid floor") 
        
        
       

    def draw(self):
        for point in self.spawnpoints:
            point.draw()

    def spawn(self):
        valid_point = self.get_valid_spawnpoint()
        if not valid_point: 
            return
        
        x, y = valid_point.get_coordinates()
        
        ran = random.randint(1,5)
        if ran == 5:
            person = Citizen(self.screen, x, y, self.screen)
        else: person = Thief1(self.screen, x, y, self.screen)
        
        valid_point.add_slot(person)

    def get_valid_spawnpoint(self):
        points = [point for point in self.spawnpoints if point.not_full()]
        if points:
            return random.choice(points)
        return None

    def remove(self):
        for point in self.spawnpoints:
            for person in point.get_people():
                if person.is_escape():
                    point.remove_slot(person)
                    if type(person) is Thief1:
                        print("Thief escape")
                        return True
                    else: return False

    
    def update(self, event):
        if event.type == self.spawn_event:
            self.spawn()
        if event.type == self.remove_event:
            if self.remove(): return True
        return False
    
    def handle_click(self, position):
        for point in self.spawnpoints:
            for person in point.get_people():
                if person.check_colision(position):
                    point.remove_slot(person)
                    if type(person) is Thief1:
                        return 1
                    else:
                        print("citizen")
                        return 2
        return 0
    
    def reset(self):
        """Xóa tất cả nhân vật và đóng cửa."""
        for point in self.spawnpoints:
            point.slot.clear()  # Xóa tất cả nhân vật
            point.close_door()  # Đóng cửa lại
