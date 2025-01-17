import pygame,sys
from pygame.locals import *

from param import SCREEN_WIDTH,SCREEN_HEIGHT,GAME_NAME
from utils import StateManager

from gameState import PlayGame, Intro, Menu, GameOver, PauseGame



class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        
        self.state = StateManager('intro')
        
        self.intro = Intro(self.screen, self.state)
        self.menu = Menu(self.screen, self.state)
        self.play_game = PlayGame(self.screen, self.state)
        self.game_over = GameOver(self.screen, self.state)
        self.pause = PauseGame(self.screen, self.state)
        self.states = {'intro': self.intro, 'menu': self.menu, 'play_game': self.play_game, 'game_over': self.game_over, 'pause': self.pause}
        
    def run(self):
        while True: #loop every 1/60 seconds
            self.states[self.state.get_state()].run()
            pygame.display.update()






if __name__ == "__main__":  
    game = Game()
    game.run()
    
    
        