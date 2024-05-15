import sys, time
import pygame as pg
from settings import Settings 
from ship import Ship
from aliens import Aliens
from vector import Vector
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from barriers import Barriers
from sound import Sound

class LaunchScreen:
  names = ['bunny', 'marshmallow', 'astronaut', 'cat', 'star', 'cube' , 'ufo']
  images = [pg.transform.scale_by(pg.image.load(f'images/aliens_{name}.png')  , 2.5) for name in names] 
  points = [50, 60, 70, 80, 90, 100, "???"]
  space_image = pg.transform.scale_by(pg.image.load('images/space_2.png'), 4)

  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Launch Screen")
    self.screen_rect = self.screen.get_rect()  
    
    self.aliens = None
    self.stats = GameStats(game=self)
    self.sound = Sound()
    self.sb = Scoreboard(game=self)

    self.ship = Ship(game=self)
    self.aliens = Aliens(game=self)  
    self.ship.set_aliens(self.aliens)
    self.ship.set_sb(self.sb)
    self.barriers = Barriers(game=self)
    self.game_active = False              # MUST be before Button is created
    self.first = True
    self.play_button = Button(game=self, text='PLAY GAME', x=self.screen_rect.centerx, y=self.screen_rect.centery + 150)
    self.high_scores_button = Button(game=self, text='HIGH SCORES', x=self.screen_rect.centerx, y=self.screen_rect.centery + 230)  
    self.back_button = Button(game=self, text='GO BACK', x=self.screen_rect.centerx, y=self.screen_rect.centery + 300)        
      
    self.game_active = False
  
    self.text_color = (255, 255, 200)     
    self.font = pg.font.SysFont(None, 120)
    self.small_font = pg.font.SysFont(None, 50)    

    self.prepare_launch_screen()
  
  def check_events(self):
    for event in pg.event.get():
      type = event.type
      if type == pg.QUIT:
        pg.quit()
        sys.exit() 
      elif type == pg.MOUSEBUTTONDOWN: 
        b = self.play_button
        c = self.high_scores_button
        d = self.back_button
        x, y = pg.mouse.get_pos()
        if b.rect.collidepoint(x, y):
          b.press_play()
        if c.rect.collidepoint(x, y):
          c.press_high_score()
        if d.rect.collidepoint(x, y):
          d.press_back()
      elif type == pg.MOUSEMOTION: 
        b = self.play_button
        c = self.high_scores_button
        d = self.back_button
        x, y = pg.mouse.get_pos()
        b.select(b.rect.collidepoint(x, y))
        c.select(c.rect.collidepoint(x, y))
        d.select(d.rect.collidepoint(x, y))

  def activate(self): 
    self.game_active = True
    self.sound.play_music("sounds/mirror_mirror_cut_version.wav")
    g = Game()
    g.play()

  def activate_high_scores(self):
    self.prepare_high_score_screen()
    while True:  
      self.check_events() 
      self.high_score_screen_update()        

  def activate_back(self):
    l = LaunchScreen()
    l.run_launch_screen()

  def high_score_screen_update(self):
    self.screen.fill((0, 0, 0))    
    self.draw_high_scores()
    self.back_button.update()
    pg.display.flip()

  def prepare_high_score_screen(self):
    self.lines = []
    with open("highscore.txt", "r") as file:
      try:
        for line in (file.readlines() [-10:]):
          my_line = line.replace("\n", "")
          self.lines.append(my_line)       
      except:
        print("Error in reading file")
      file.close()
    
    self.lines.sort(reverse=True, key=int)
    self.high_score_images = []
    self.high_score_rects = []
    y_high_score_num = 120
    for line in self.lines:
      high_score_str = line
      high_score_image = self.small_font.render(high_score_str, True, self.text_color)
      high_score_rect = high_score_image.get_rect(centerx=self.screen_rect.centerx, top=self.screen_rect.top + y_high_score_num)
      self.high_score_images.append(high_score_image)
      self.high_score_rects.append(high_score_rect)
      y_high_score_num += 50  

    top_ten_str = "Top 10 HighScores"
    self.top_ten_image = self.font.render(top_ten_str, True, self.text_color)
    self.top_ten_rect = self.top_ten_image.get_rect()
    self.top_ten_rect.centerx = self.screen_rect.centerx
    self.top_ten_rect.top = self.screen_rect.top + 20

  def draw_high_scores(self):
    self.screen.blit(self.top_ten_image, self.top_ten_rect)
    for high_score_image, high_score_rect in zip(self.high_score_images, self.high_score_rects):
      self.screen.blit(high_score_image, high_score_rect)

  def run_launch_screen(self):
    """Start launch screen loop for the game."""
    while True:  
      self.check_events()
      self.update()

  def prepare_launch_screen(self):
    """Prepare all images to be drawn onto launch screen before updating the window."""
    space_invaders_str = "Space Invaders"
    # Prepare the Space Invaders logo
    space_invaders_str = "Space Invaders"
    self.space_invaders_image = self.font.render(space_invaders_str, True, self.text_color)
    self.space_invaders_rect = self.space_invaders_image.get_rect()
    self.space_invaders_rect.centerx = self.screen_rect.centerx
    self.space_invaders_rect.top = self.screen_rect.top + 100

    # Prepare the alien images
    self.image_rects = []
    x_num = 188
    for image in self.images:
        image_rect = image.get_rect(left=x_num, centery=self.screen_rect.centery - 50)
        self.image_rects.append(image_rect)
        x_num += 120

    # Prepare the points each alien is worth
    self.score_images = []
    self.score_rects = []
    x_point_num = 200
    for point in self.points:
        score_str = f'{point}'
        score_image = self.small_font.render(score_str, True, self.text_color)
        score_rect = score_image.get_rect(left=x_point_num, centery=self.screen_rect.centery + 20)
        self.score_images.append(score_image)
        self.score_rects.append(score_rect)
        x_point_num += 120

    self.pts_images = []
    self.pts_rects = []
    x_pts_num = 200
    for point in LaunchScreen.points:
      pts_str = 'pts'
      pts_image = self.small_font.render(pts_str, True, self.text_color)
      pts_rect = pts_image.get_rect(left=x_pts_num, centery=self.screen_rect.centery + 50)
      self.pts_images.append(pts_image)
      self.pts_rects.append(pts_rect)
      x_pts_num += 120

    self.space_image_rect = self.space_image.get_rect()

  def update(self):  
    # Update images on the screen, and flip to the new screen
    self.screen.fill((0, 0, 0))
    
    self.draw()
    self.play_button.update()
    self.high_scores_button.update()
    pg.display.flip()

  def draw(self):
    self.screen.blit(self.space_image, self.space_image_rect)    

    # Draw the space invaders logo
    self.screen.blit(self.space_invaders_image, self.space_invaders_rect)
    
    # Draw the aliens
    for image, image_rect in zip(self.images, self.image_rects):
      self.screen.blit(image, image_rect)

    # Draw the points each alien is worth
    for score_image, score_rect in zip(self.score_images, self.score_rects):
      self.screen.blit(score_image, score_rect)

    for pts_image, pts_rect in zip(self.pts_images, self.pts_rects):
      self.screen.blit(pts_image, pts_rect)


class Game:
  key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}
       
  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Alien Invasion")
    self.screen_rect = self.screen.get_rect() 

    self.aliens = None
    self.stats = GameStats(game=self)
    self.sound = Sound()
    self.sb = Scoreboard(game=self)
    

    self.ship = Ship(game=self)
    self.aliens = Aliens(game=self)  
    self.ship.set_aliens(self.aliens)
    self.ship.set_sb(self.sb)
    self.barriers = Barriers(game=self)
    #self.game_active = False              # MUST be before Button is created
    self.game_active = True
    self.first = True
    self.play_button = Button(game=self, text='Play')

  def check_events(self):
    for event in pg.event.get():
      type = event.type
      if type == pg.KEYUP: 
        key = event.key            
        if key == pg.K_SPACE: self.ship.cease_fire()
        elif key in Game.key_velocity: self.ship.all_stop()
      elif type == pg.QUIT: 
        pg.quit()
        sys.exit()
      elif type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_SPACE: 
          self.ship.fire_everything()
        elif key == pg.K_p: 
          self.play_button.select(True)
          self.play_button.press_play()
        elif key in Game.key_velocity: 
          self.ship.add_speed(Game.key_velocity[key])
      elif type == pg.MOUSEBUTTONDOWN:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        if b.rect.collidepoint(x, y):
          b.press_play()
      elif type == pg.MOUSEMOTION:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        b.select(b.rect.collidepoint(x, y))
    
  def restart(self):
    self.screen.fill(self.settings.bg_color)
    self.ship.reset()
    self.aliens.reset()
    self.barriers.reset()
    self.settings.initialize_dynamic_settings()

  def save_highscore(self):
    # last highscore is at the end of the file
    with open("highscore.txt", "r") as file:
      try:
        lines = file.readlines()
        self.last_high_score = lines[-1]
        #print("Last high score: " + self.last_high_score)
      except:
        print("Error in reading file")
      file.close()

    # check if current high score is greater than the highscore in the file, if yes, save it
    with open("highscore.txt", "a") as file:
      try:
        if self.stats.high_score > int(self.last_high_score):
          high_score_str = str(self.stats.high_score)
          file.write('\n' + high_score_str)
      except:
        print("There was an error in writing to the file")  
      file.close()   
                 

  def game_over(self):
    print('Game Over !')
    pg.mouse.set_visible(True)
    self.play_button.change_text('Play again?', x=self.screen_rect.centerx, y=self.screen_rect.centery)
    self.play_button.show()
    print(self.stats.high_score)
    self.save_highscore()
    self.first = True
    self.game_active = False
    self.stats.reset()
    self.restart()
    self.sound.play_game_over()

  def activate(self): 
    self.game_active = True
    self.first = False
    self.sound.play_music("sounds/mirror_mirror_cut_version.wav")

  def play(self):
    finished = False
    self.screen.fill(self.settings.bg_color)

    while not finished:
      self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS

      if self.game_active or self.first:
        self.first = False
        self.screen.fill(self.settings.bg_color)
        self.ship.update()
        self.aliens.update()   # when we have aliens
        self.barriers.update()
        self.sb.update()
      else:
        self.play_button.update()  
      
      pg.display.flip()
      time.sleep(0.02)


if __name__ == '__main__':
  l = LaunchScreen()
  l.run_launch_screen()

