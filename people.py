import pygame
from enum import Enum
import random

from animationFrame import PeopleAnimationFrame
from param import IMAGE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT

from Sprite.spriteSheet import Spritesheet

thiefSpriteSheet = Spritesheet(f'Sprite/thief/npc_thief-sheet.png')
civilianSpriteSheet = Spritesheet(f'Sprite/civilian/npcs-civilian-sheet.png')

thief_spawn_frames = [
    thiefSpriteSheet.parse_sprite('spawn1'),
    thiefSpriteSheet.parse_sprite('spawn2'),
    thiefSpriteSheet.parse_sprite('spawn3'),
]

thief_idle_frames = [
    thiefSpriteSheet.parse_sprite('idle1'),
    thiefSpriteSheet.parse_sprite('idle2'),
]

thief_right_run_frames = [
    thiefSpriteSheet.parse_sprite('right_run1'),
    thiefSpriteSheet.parse_sprite('right_run2'),
    thiefSpriteSheet.parse_sprite('right_run3'),
    thiefSpriteSheet.parse_sprite('right_run4'),
]

thief_left_run_frames = [
    thiefSpriteSheet.parse_sprite('left_run1'),
    thiefSpriteSheet.parse_sprite('left_run2'),
    thiefSpriteSheet.parse_sprite('left_run3'),
    thiefSpriteSheet.parse_sprite('left_run4'),
]

thief_dead_frames = [
    thiefSpriteSheet.parse_sprite('dead1'),
    thiefSpriteSheet.parse_sprite('dead2'),
    thiefSpriteSheet.parse_sprite('dead3'),
    thiefSpriteSheet.parse_sprite('dead4'),
    thiefSpriteSheet.parse_sprite('dead5'),
    thiefSpriteSheet.parse_sprite('dead6'),
]

civilian_spawn_frames = [
    civilianSpriteSheet.parse_sprite('spawn1'),
    civilianSpriteSheet.parse_sprite('spawn2'),
    civilianSpriteSheet.parse_sprite('spawn3'),
]

civilian_idle_frames = [
    civilianSpriteSheet.parse_sprite('idle1'),
    civilianSpriteSheet.parse_sprite('idle2'),
]

civilian_right_run_frames = [
    civilianSpriteSheet.parse_sprite('right_run1'),
    civilianSpriteSheet.parse_sprite('right_run2'),
    civilianSpriteSheet.parse_sprite('right_run3'),
    civilianSpriteSheet.parse_sprite('right_run4'),
]

civilian_left_run_frames = [
    civilianSpriteSheet.parse_sprite('left_run1'),
    civilianSpriteSheet.parse_sprite('left_run2'),
    civilianSpriteSheet.parse_sprite('left_run3'),
    civilianSpriteSheet.parse_sprite('left_run4'),
]

civilian_dead_frames = [
    civilianSpriteSheet.parse_sprite('dead1'),
    civilianSpriteSheet.parse_sprite('dead2'),
    civilianSpriteSheet.parse_sprite('dead3'),
    civilianSpriteSheet.parse_sprite('dead4'),
    civilianSpriteSheet.parse_sprite('dead5'),
    civilianSpriteSheet.parse_sprite('dead6'),
]

class PeopleState(Enum):
    SPAWN = 0
    IDLE = 1
    RUN = 2
    DEAD = 3
    ESCAPE = 4
    NONE = 5

class People:
    def __init__(self, screen, x, y, life_time=15):
        self.state = PeopleState.SPAWN
        self.x = x
        self.y = y
        self.hit_time = 0
        self.escape_time = 0
        self.life_time = life_time  # seconds
        self.annimation = PeopleAnimationFrame()
        self.screen = screen
        self.is_dead = False
        self.state_timer_start = 0
        self.state_timer_end = random.randint(2000, 5000)
        self.check_x_moved = False
        self.check_y_moved = False
        self.direction = random.choice([-1, 1])
        # self.direction_in_road = random.choice([-1, 1])
        self.target_x = 0
        self.target_y = 0
        self.move_speed = 2
        self.in_road = False

    def change_state(self, new_state):
        self.state = new_state

    def check_colision(self, position):
        if self.is_dead:  # already dead
            return False

        image_size = self.annimation.get_curent_state().get_current_frame().get_size()
        # margin = (self.image_size[0] / 2 ,self.image_size[1])
        # center = (self.x + margin[0], self.y + margin[1])
        if position[0] > self.x and position[1] > self.y and position[0] < self.x + image_size[0] and position[1] < self.y + image_size[1]:
            self.change_state(PeopleState.DEAD)
            self.is_dead = True
            self.annimation.set_dead_frame()
            return True
        else:
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
            if self.x <= 174 or self.x >= 1100:
                self.target_y = 630
            if self.y == 630:
                self.in_road = True
            else:
                # For render movement
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

    def draw(self):  # called by update function
        current_clock_time = pygame.time.get_ticks()

        if self.state == PeopleState.SPAWN:
            # self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.screen.blit(pygame.transform.scale(self.annimation.get_curent_state().get_current_frame(), (48, 48)), 
            (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

            if self.state_timer_start == 0:
                self.state_timer_start = current_clock_time

            if current_clock_time - self.state_timer_start >= self.state_timer_end:
                self.change_state(PeopleState.IDLE)
                self.annimation.set_idle_frame()
                self.state_timer_start = 0

        elif self.state == PeopleState.IDLE:
            # self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.screen.blit(pygame.transform.scale(self.annimation.get_curent_state().get_current_frame(), (48, 48)), 
            (self.x, self.y))
            self.annimation.get_curent_state().next_frame()
            self.change_state(PeopleState.RUN)
            self.annimation.set_run_frame()

        elif self.state == PeopleState.RUN:
            # self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.screen.blit(pygame.transform.scale(self.annimation.get_curent_state().get_current_frame(), (48, 48)), 
            (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

        elif self.state == PeopleState.DEAD:
            # if not self.is_dead:
            #     self.annimation.set_dead_frame()
            #     self.is_dead = True

            # self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.screen.blit(pygame.transform.scale(self.annimation.get_curent_state().get_current_frame(), (48, 48)), 
            (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

        elif self.state == PeopleState.ESCAPE:
            # self.screen.blit(self.annimation.get_curent_state().get_current_frame(), (self.x, self.y))
            self.screen.blit(pygame.transform.scale(self.annimation.get_curent_state().get_current_frame(), (48, 48)), 
            (self.x, self.y))
            self.annimation.get_curent_state().next_frame()

            if self.is_escape():
                print("Escaped!")

    def is_escape(self):
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return True
        return False


# class Thief1(People):  # Does not harm the player
#     def __init__(self, screen, x, y, life_time=15):
#         super().__init__(screen, x, y, life_time)
#         self.annimation.set_spawn_frame()
#         self.annimation.set_idle_frame()
#         self.annimation.set_run_frame()
#         self.annimation.set_dead_frame()
#         self.annimation.set_escape_frame()


class Thief1(People):
    def __init__(self, screen, x, y, life_time=15):
        super().__init__(screen, x, y, life_time)

        self.annimation = PeopleAnimationFrame(
            spawn_frame=thief_spawn_frames,
            idle_frame=thief_idle_frames,
            run_frame=thief_right_run_frames if self.direction == 1 else thief_left_run_frames,
            dead_frame=thief_dead_frames
        )
class Citizen(People):
    def __init__(self, screen, x, y, life_time=15):
        super().__init__(screen, x, y, life_time)
        self.annimation = PeopleAnimationFrame(
            spawn_frame=civilian_spawn_frames,
            idle_frame=civilian_idle_frames,
            run_frame=civilian_right_run_frames if self.direction == 1 else civilian_left_run_frames,
            dead_frame=civilian_dead_frames
        )