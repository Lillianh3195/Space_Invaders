import pygame as pg
import sys
from pygame.sprite import Sprite
from vector import Vector 
from random import randint
from lasers import Lasers
from timer import Timer
import time
from pygame import mixer 

class Ufo(Sprite):
  points = [50, 60, 70, 80, 90, 100]

  image = pg.transform.scale_by(pg.image.load(f'images/aliens_ufo.png'), 2)

  fifty_explosion_image_files = [f'images/50_explosion/50_explosion_{x}.png' for x in range(1, 11)] 
  fifty_explosion_images = [pg.transform.scale_by(pg.image.load(x), 2) for x in fifty_explosion_image_files]

  sixty_explosion_image_files = [f'images/60_explosion/60_explosion_{x}.png' for x in range(1, 11)] 
  sixty_explosion_images = [pg.transform.scale_by(pg.image.load(x), 2) for x in sixty_explosion_image_files]

  seventy_explosion_image_files = [f'images/70_explosion/70_explosion_{x}.png' for x in range(1, 11)] 
  seventy_explosion_images = [pg.transform.scale_by(pg.image.load(x), 2) for x in seventy_explosion_image_files]
  
  eighty_explosion_image_files = [f'images/80_explosion/80_explosion_{x}.png' for x in range(1, 11)] 
  eighty_explosion_images = [pg.transform.scale_by(pg.image.load(x), 2) for x in eighty_explosion_image_files]

  ninety_explosion_image_files = [f'images/90_explosion/90_explosion_{x}.png' for x in range(1, 11)] 
  ninety_explosion_images = [pg.transform.scale_by(pg.image.load(x), 2) for x in ninety_explosion_image_files]

  hundred_explosion_image_files = [f'images/100_explosion/100_explosion_{x}.png' for x in range(1, 11)] 
  hundred_explosion_images = [pg.transform.scale_by(pg.image.load(x), 2) for x in hundred_explosion_image_files]

  def __init__(self, game):
    super().__init__()
    self.game = game 
    self.screen = game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = game.settings
    self.v = Vector(self.settings.ufo_speed, 0)
    
    '''
    self.ufo_sound = pg.mixer.Sound('sounds/pac_man.wav')
    self.ufo_sound.play(loops=-1)
    self.sound = game.sound
    self.sound.play_ufo()
    '''

    self.fifty_explosion_timer = Timer(image_list=Ufo.fifty_explosion_images, delta=5, looponce=True)
    self.sixty_explosion_timer = Timer(image_list=Ufo.sixty_explosion_images, delta=5, looponce=True)
    self.seventy_explosion_timer = Timer(image_list=Ufo.seventy_explosion_images, delta=5, looponce=True)
    self.eighty_explosion_timer = Timer(image_list=Ufo.eighty_explosion_images, delta=5, looponce=True)
    self.ninety_explosion_timer = Timer(image_list=Ufo.ninety_explosion_images, delta=5, looponce=True)
    self.hundred_explosion_timer = Timer(image_list=Ufo.hundred_explosion_images, delta=5, looponce=True)

    self.explosion_timers = [self.fifty_explosion_timer, self.sixty_explosion_timer, 
                        self.seventy_explosion_timer, self.eighty_explosion_timer, self.ninety_explosion_timer, self.hundred_explosion_timer]

    self.ufo_timer = Timer([Ufo.image, Ufo.image], delta=20)
    self.timer = self.ufo_timer   

    # Set UFO's rect attribute
    self.rect = self.image.get_rect()

    # Start each new UFO beyond the top left of the screen
    self.rect.x = self.screen_rect.left 
    self.rect.y = self.screen_rect.top + 100

    # Store the UFO's exact position
    self.x = float(self.rect.x)
    self.is_dying = False
    self.really_dead = False     
    

  def laser_offscreen(self, rect): return rect.bottom > self.screen_rect.bottom  

  def laser_start_rect(self):
    rect = self.rect
    rect.midbottom = self.rect.midbottom
    return rect.copy()

  def fire(self, lasers):
    lasers.add(owner=self)
  
  # Move UFO right
  def update(self):
    if (self.is_dying and self.timer.finished()): 
      self.kill()
      #self.ufo_sound.stop()
      self.really_dead = True
      #self.sound.stop_sound("sounds/pac_man.wav")
      #print("ufo is dead, stopping the sound")
    self.x += self.v.x
    self.rect.x = self.x
    if (self.rect.x > self.screen_rect.right): 
      self.kill()    # delete off-screen UFOs
      #self.ufo_sound.stop()
      #print("offscreen ufo is deleted!")
    self.draw()

  def draw(self): 
    if (self.is_dying):
        self.image = self.timer.current_image()          
    self.screen.blit(self.image, self.rect)


if __name__ == '__main__':
  print("\nERROR: ufo.py is the wrong file! Run play from alien_invasions.py\n")