import pygame

class Sound:    
    pygame.mixer.init()
    background = pygame.mixer.Sound('sounds/maintrack.mp3')
    intro = pygame.mixer.Sound('sounds/typing.wav')
    dead = pygame.mixer.Sound('sounds/dead.mp3')
    shoot = pygame.mixer.Sound('sounds/shoot.mp3')
    reload = pygame.mixer.Sound('sounds/reload_gun.mp3')

    # SOUND_OFF = False
    SOUND_OFF = True

    @classmethod
    def turnOn(cls, type):
        if cls.SOUND_OFF:
            return
        if type == 'background':
            cls.background.play(-1)
        if type == 'intro':
            cls.intro.play()
        if type == 'dead':
            cls.dead.play()
        if type == 'shoot':
            cls.shoot.play()
        if type == 'reload':
            cls.reload.play()
            
    @classmethod
    def turnOff(cls, type):
        if type == 'background':
            cls.background.stop()
        if type == 'intro':
            cls.intro.stop()

