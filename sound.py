import pygame as pg
from pygame import mixer 
import time


class Sound:
    def __init__(self):
        mixer.init() 
        self.phaser_sound = mixer.Sound("sounds/my_laser.wav")
        self.explosion_sound = mixer.Sound("sounds/explosion.wav")
        self.new_level_sound = mixer.Sound("sounds/new_level.wav")
        self.ufo_sound = mixer.Sound("sounds/pac_man.wav")
        self.volume = 0.1
        self.set_volume(self.volume)        
    
    def set_volume(self, volume=0.3):
        mixer.music.set_volume(1.2) 
        self.phaser_sound.set_volume(2 * volume)
        self.explosion_sound.set_volume(1)
        self.new_level_sound.set_volume(0.6)
        self.ufo_sound.set_volume(0.2)

    def play_music(self, filename): 
        self.stop_music()
        mixer.music.load(filename) 
        mixer.music.play(loops=-1) 
 
    def pause_music(self): 
        mixer.music.pause()

    def unpause_music(self):
        mixer.music.unpause()      

    def stop_music(self): 
        mixer.music.stop() 
 
    def play_phaser(self): 
        mixer.Sound.play(self.phaser_sound) 

    def play_explosion(self):
        mixer.Sound.play(self.explosion_sound)

    def play_new_level(self):
        mixer.Sound.play(self.new_level_sound)

    def play_ufo(self):
        #mixer.Sound.play(self.ufo_sound, loops=-1)
        mixer.Sound.play(self.ufo_sound)

    def play_game_over(self):
        self.stop_music()
        self.play_music("sounds/red_like_roses.wav")
        mixer.music.fadeout(10000)
        #self.mixer.music.fadeout(5000)  # 5 seconds
        #time.sleep(6.5)
        time.sleep(10)
        self.stop_music()
    
    def stop_ufo(self):
        self.ufo_sound.stop()
