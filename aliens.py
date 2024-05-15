import pygame as pg
import sys
from pygame.sprite import Sprite
from vector import Vector 
from random import randint
from lasers import Lasers
from ufo import Ufo
from timer import Timer
import time

class Alien(Sprite):
  #names = ['bunny', 'pig', 'stalk_eyes', 'w_heart', 'w_pigtails', 'wild_tentacles']
  names = ['bunny', 'marshmallow', 'astronaut', 'cat', 'star', 'cube']
  #points = [10, 25, 300, 35, 100, 600]
  points = [50, 60, 70, 80, 90, 100]
  #images = [pg.image.load(f'images/alien_{name}.png') for name in names] 
  images = [pg.transform.scale_by(pg.image.load(f'images/aliens_{name}.png'), 2) for name in names] 

  ufo_image = pg.transform.scale_by(pg.image.load(f'images/aliens_ufo.png'), 2)

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
    
  # nameslen = len(names)
  # choices = [randint(0, nameslen) for _ in range(nameslen)]

  #li = [x * x for x in range(1, 11)]

  def __init__(self, game, row, alien_no, is_ufo=False):
    super().__init__()
    self.game = game 
    self.screen = game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = game.settings

    self.reg_timer = Timer(Alien.images, start_index=randint(0, len(Alien.images) - 1), delta=20)
    self.ufo_timer = Timer(Alien.ufo_image, delta=20)
    self.fifty_explosion_timer = Timer(image_list=Alien.fifty_explosion_images, delta=5, looponce=True)
    self.sixty_explosion_timer = Timer(image_list=Alien.sixty_explosion_images, delta=5, looponce=True)
    self.seventy_explosion_timer = Timer(image_list=Alien.seventy_explosion_images, delta=5, looponce=True)
    self.eighty_explosion_timer = Timer(image_list=Alien.eighty_explosion_images, delta=5, looponce=True)
    self.ninety_explosion_timer = Timer(image_list=Alien.ninety_explosion_images, delta=5, looponce=True)
    self.hundred_explosion_timer = Timer(image_list=Alien.hundred_explosion_images, delta=5, looponce=True)
    self.alien_timers = [self.fifty_explosion_timer, self.sixty_explosion_timer, 
                        self.seventy_explosion_timer, self.eighty_explosion_timer, self.ninety_explosion_timer, self.hundred_explosion_timer]

    self.timer = self.reg_timer    

    # Load the alien image and set its rect attribute
    self.image = Alien.images[row % len(Alien.names)]
    self.alien_no = alien_no
    # self.image = Alien.images[randint(0, 5)]
    # self.image = Alien.images[Alien.choices[row % len(Alien.names)]]
    self.rect = self.image.get_rect()

    # Start each new alien near the top left of the screen
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height 

    # Store the alien's exact position
    self.x = float(self.rect.x)
    self.is_dying = False
    self.really_dead = False 


  def laser_offscreen(self, rect): return rect.bottom > self.screen_rect.bottom  

  def laser_start_rect(self):
    rect = self.rect
    rect.midbottom = self.rect.midbottom
    return rect.copy()

  def fire(self, lasers):
    # print(f'Alien {self.alien_no} firing laser')
    lasers.add(owner=self)

  # Returns true if alien is at the edge of screen
  def check_edges(self):
    r = self.rect 
    sr = self.screen_rect
    return r.right >= sr.right or r.left < 0
  
  def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom 
  
  # Moves alien right or left
  def update(self, v, delta_y):
    if (self.is_dying and self.timer.finished()): # when hit the timer should be the explosion timer
      #print("Alien Update - alien is really dead")
      self.kill()
      self.really_dead = True
      self.timer = self.reg_timer  # reset the timer back to regular timer 

    self.x += v.x
    self.rect.x = self.x
    self.rect.y += delta_y
    self.draw()

  def draw(self):    
    if not self.really_dead:
      self.image = self.timer.current_image()          
      self.screen.blit(self.image, self.rect)


######################################################################################################
class Aliens():
  laser_image_files = [f'images/alien_laser_0{x}.png' for x in range(2)]
  laser_images = [pg.transform.scale(pg.image.load(x), (50, 50)) for x in laser_image_files]

  def __init__(self, game):
    self.game = game
    self.screen = game.screen
    self.settings = game.settings 
    self.stats = game.stats
    self.sb = game.sb
    self.aliens_created = 0
    self.v = Vector(self.settings.alien_speed, 0)
    self.laser_timer = Timer(image_list=Aliens.laser_images, delta=10)
    self.lasers = Lasers(game=game, v=Vector(0, 1) * self.settings.laser_speed, 
                         timer=self.laser_timer, owner=self)

    self.alien_group = pg.sprite.Group()
    self.ufo_group = pg.sprite.Group()

    self.ship = game.ship
    self.alien_firing_now = 0
    self.fire_every_counter = 0
    self.create_fleet()
    
    self.ufo_counter = 0
    self.ufo_created = False
    self.sound = game.sound
    #self.ufo_sound = pg.mixer.Sound('sounds/pac_man.wav')
  
    
  def create_alien(self, x, y, row, alien_no):
    # Create an alien and place it in the row
    alien = Alien(self.game, row, alien_no)
    alien.x = x
    alien.rect.x, alien.rect.y = x, y
    self.alien_group.add(alien)

  def add_ufo(self):
    #self.sound.play_ufo()    
    ufo = Ufo(self.game)   
    #self.ufo_sound = pg.mixer.Sound('sounds/pac_man.wav')   
    #self.ufo_sound.play(loops=-1)
    self.ufo_group.add(ufo)   
 

  def empty(self): 
    self.alien_group.empty()
    self.ufo_group.empty()

  def reset(self):
    self.alien_group.empty()
    self.ufo_group.empty()
    self.lasers.empty()
    self.create_fleet() 
  
  def create_fleet(self):
    self.fire_every_counter = 0
    alien = Alien(self.game, row=0, alien_no=-1)
    alien_width, alien_height = alien.rect.size 

    x, y, row = alien_width, alien_height, 0
    self.aliens_created = 0
    #while y < (self.settings.screen_height - 3 * alien_height):
    while y < (self.settings.screen_height - 4 * alien_height):   # available y space
      while x < (self.settings.screen_width - 2 * alien_width):   # available x space
        # Add extra space on top to leave room for ufo
        if row == 0:    
          y = self.settings.alien_spacing * alien_height * 2
        self.create_alien(x=x, y=y, row=row, alien_no=self.aliens_created)
        x += self.settings.alien_spacing * alien_width
        self.aliens_created += 1
      x = alien_width
      y += self.settings.alien_spacing * alien_height
      row += 1

  def check_edges(self):
    for alien in self.alien_group.sprites():
      if alien.check_edges(): 
        return True
    return False

  def check_bottom(self):
    for alien in self.alien_group.sprites():
      if alien.check_bottom(): return True
    return False

  # Drop fleet down and change its direction
  def update(self): 
    # Add ufo every time you kill 40 aliens.    
    if self.ufo_counter > 40:
      self.add_ufo()   
      self.ufo_counter = 0 

    delta_y = 0
    if self.check_edges():
      delta_y = self.settings.fleet_drop
      self.v.x *= -1
    # if alien fleet reaches bottom of screen, ship gets hit 
    if self.check_bottom(): self.ship.hit()
    
    #Ufo is hit! Ship lasers taking out ufo
    ufo_collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.ufo_group, True, False)
    if len(ufo_collisions) > 0:
      print("ufo collision!")
      #pg.mixer.Sound.stop(self.ufo_sound)
      #self.ufo_sound.stop()
      #self.stop_ufo()
      for ufo_list in ufo_collisions.values():
        for ufo in ufo_list:          
          ufo.is_dying = True
          ufo_index = randint(0, 5)
          points = Alien.points[ufo_index]
          print("Added " + str(points) + " points!")
          self.stats.score += points
          explosion_timer = ufo.explosion_timers[ufo_index]
          ufo.timer = explosion_timer
          print("set ufo timer to explosion timer")
      self.sb.prep_score()
      self.sb.check_high_score()    

    # Alien is hit! Ship lasers taking out aliens, so get rid of the laser and alien
    collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.alien_group, True, False)   # since alien dies before animation is finished, must keep it alive
    if len(collisions) > 0:      
      for alien_list in collisions.values():
        for alien in alien_list:
          self.ufo_counter += 1
          alien.is_dying = True
          alien_index = alien.timer.current_index()
          #print(alien_index)
          if alien_index < len(alien.images):
            points = Alien.points[alien_index]
            #print("Added " + str(points) + " points!")
            self.stats.score += points
            explosion_timer = alien.alien_timers[alien_index]
            alien.timer = explosion_timer
            self.sound.play_explosion()     
      '''
      for alien in collisions:    # laser sprite, NOT an alien cuz { laser sprite: [alien sprite] }
        index = alien.timer.current_index()
        points = Alien.points[index]
        self.stats.score += points
        '''
        # self.stats.score += self.settings.alien_points
      self.sb.prep_score()
      self.sb.check_high_score()

    # laser-laser collisions
    collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.lasers.lasergroup(), 
                                        True, True)

    for alien in self.alien_group.sprites():
      alien.update(self.v, delta_y)    

    for ufo in self.ufo_group.sprites():
      ufo.update()  

    # must have aliens to fire at the ship
    if self.alien_group and self.fire_every_counter % self.settings.aliens_fireevery == 0:
      n = randint(0, len(self.alien_group) - 1)
      self.alien_group.sprites()[n].fire(lasers=self.lasers)
    self.fire_every_counter += 1

    # update the positions of all of the aliens' lasers (the ship updates its own lasers)
    self.lasers.update()

    # no more aliens -- time to re-create the fleet
    if not self.alien_group:
      self.sound.play_new_level()
      self.lasers.empty()
      self.create_fleet()
      self.settings.increase_speed()
      self.stats.level += 1
      self.sb.prep_level()

    # aliens hitting the ship
    if pg.sprite.spritecollideany(self.ship, self.alien_group):
      self.ship.hit()

    # alien lasers taking out the ship
    if pg.sprite.spritecollideany(self.ship, self.lasers.lasergroup()):
      self.ship.hit()


if __name__ == '__main__':
  print("\nERROR: aliens.py is the wrong file! Run play from alien_invasions.py\n")
