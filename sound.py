import pygame
import numpy as np
from pygame.sndarray import array, make_sound

class Sound:
    pygame.mixer.init()
    
    # Danh sách âm thanh
    sounds = {
        "background": pygame.mixer.Sound('sounds/maintrack.mp3'),
        "intro": pygame.mixer.Sound('sounds/typing.wav'),
        "dead": pygame.mixer.Sound('sounds/dead.mp3'),
        "shoot": pygame.mixer.Sound('sounds/shoot.mp3'),
        "reload": pygame.mixer.Sound('sounds/reload_gun.mp3')
    }
    
    # Kênh riêng cho từng loại âm thanh
    channels = {
        "background": pygame.mixer.Channel(0),
        "shoot": pygame.mixer.Channel(1),
        "dead": pygame.mixer.Channel(2),
        "reload": pygame.mixer.Channel(3),
        "effects": pygame.mixer.Channel(4)  # Dùng cho các âm thanh khác như intro
    }

    SOUND_OFF = False  
    VOLUME_BACKGROUND = 0.2
    VOLUME_SHOOT = 0.1
    VOLUME_DEAD = 0.5
    VOLUME_RELOAD = 0.8

    @classmethod
    def set_volume(cls, type, volume):
        """Đặt âm lượng cho một loại âm thanh"""
        if type in cls.sounds:
            cls.sounds[type].set_volume(volume)
        if type == "background":
            cls.VOLUME_BACKGROUND = volume
        elif type == "shoot":
            cls.VOLUME_SHOOT = volume
        elif type == "dead":
            cls.VOLUME_DEAD = volume
        elif type == "reload":
            cls.VOLUME_RELOAD = volume

    @classmethod
    def turnOn(cls, type):
        """Phát âm thanh theo loại với kênh riêng"""
        if cls.SOUND_OFF or type not in cls.sounds:
            return
        
        if type == "background":
            cls.sounds["background"].set_volume(cls.VOLUME_BACKGROUND)
            cls.channels["background"].play(cls.sounds["background"], loops=-1)
        elif type == "shoot":
            cls.sounds["shoot"].set_volume(cls.VOLUME_SHOOT)
            cls.channels["shoot"].play(cls.sounds["shoot"])
        elif type == "dead":
            cls.sounds["dead"].set_volume(cls.VOLUME_DEAD)
            cls.channels["dead"].play(cls.sounds["dead"])
        elif type == "reload":
            cls.sounds["reload"].set_volume(cls.VOLUME_RELOAD)
            cls.channels["reload"].play(cls.sounds["reload"])
        else:
            cls.channels["effects"].play(cls.sounds[type])

    @classmethod
    def turnOff(cls, type):
        """Tắt âm thanh của loại tương ứng"""
        if type in cls.channels:
            cls.channels[type].stop()

    @classmethod
    def play_reload_with_speed(cls, reload_time):
        """Chỉnh tốc độ âm thanh reload theo thời gian nạp đạn"""
        if cls.SOUND_OFF:
            return

        reload_sound = cls.sounds["reload"]
        reload_array = array(reload_sound)
        original_length = len(reload_array)

        playback_speed = original_length / (reload_time * 44.1)
        new_length = int(original_length / playback_speed)

        new_reload_array = np.interp(
            np.linspace(0, original_length, new_length),
            np.arange(original_length),
            reload_array[:, 0]
        ).astype(np.int16)

        new_reload_sound = make_sound(np.column_stack((new_reload_array, new_reload_array)))
        cls.channels["reload"].play(new_reload_sound, loops=0, maxtime=reload_time)
