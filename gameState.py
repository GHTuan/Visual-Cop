import pygame
import sys


class Intro:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        # self.background = image_loader("intro_background.png")
        # self.start_game_button = image_loader("start_game_button.png")
        # self.menu_button = image_loader("menu_button.png")
    def run(self):
        self.state.set_state('play_game')
    
class Menu:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        # self.background = image_loader("menu_background.png")
        # self.start_game_button = image_loader("start_game_button.png")
        # self.exit_game_button = image_loader("exit_game_button.png")
    def run(self):
        pass

class PlayGame:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

class GameOver:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        # self.background = image_loader("game_over_background.png")
        # self.menu_button = image_loader("menu_button.png")
        # self.exit_game_button = image_loader("exit_game_button.png")
    def run(self):
        pass

class PauseGame:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        # self.background = image_loader("pause_game_background.png")
        # self.resume_game_button = image_loader("resume_game_button.png")
        # self.menu_button = image_loader("menu_button.png")
        # self.exit_game_button = image_loader("exit_game_button.png")
    def run(self):
        pass