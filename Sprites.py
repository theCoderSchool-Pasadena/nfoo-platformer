import pygame, sys
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, w, h):
    #constructor
    super().__init__()
    self.rect = pygame.Rect(x, y, w, h)
    self.change_x = 0
    self.change_y = 0
    self.on_ground = True
    self.won_game = False
    self.font = pygame.font.SysFont("Ariel", 50)
    self.text = self.font.render("You win!", False ,"green")
    # Mario walking
    self.image = pygame.image.load("./Mario-recreated.png")
    self.image = pygame.transform.scale(self.image, (40, 40))
    self.imagex = self.image.copy()
    self.imagex = pygame.transform.flip(self.image, True, False)
    self.facingright = True

    # Mario jumping
    self.imageJ = pygame.image.load("./MarioJump.png")
    self.imageJ = pygame.transform.scale(self.imageJ, (40, 40))
    self.imageJx = self.imageJ.copy()
    self.imageJx = pygame.transform.flip(self.imageJx, True, False)
    
 
  def draw(self, screen):
    if self.won_game == True:
      pygame.draw.rect(screen, "green", self.rect)
      screen.blit(self.text,(200, 250))
      self.on_ground = True
    
    elif self.on_ground == True:
      # print(self.change_x)

      # Moving Left
      if self.change_x < 0:
        screen.blit(self.imagex, self.rect)
        self.facingright = False
      # Moving right
      elif self.change_x > 0:
        screen.blit(self.image, self.rect)
        self.facingright = True
      # Still direction
      elif self.change_x == 0:
        if self.facingright == True:
          screen.blit(self.image, self.rect)
        else:
          screen.blit(self.imagex, self.rect)
      # pygame.draw.rect(screen, "red", self.rect)
    else:
      #pygame.draw.rect(screen, "blue", self.rect)
      # screen.blit(self.image, self.rect)
      if self.facingright:
          screen.blit(self.imageJ, self.rect)
      else:
          screen.blit(self.imageJx, self.rect)
    
  def update(self):
    # gravity
    if self.change_y == 0:
      self.change_y = 1
    else:
      self.change_y += 0.35
    # detect on ground
    if self.rect.y >= 500 - self.rect.height and self.change_y >= 0:
      self.change_y = 0
      self.rect.y = 500 - self.rect.height  
      self.on_ground = True
    self.rect.y += self.change_y
  
    
    # movement
    self.rect.x += self.change_x 

  def platform_collide(self, platform):
    if self.rect.colliderect(platform.rect):
      # If Player hits left of platform
      if platform.rect.x <= self.rect.x + self.rect.width <= platform.rect.x + 5:
        self.rect.x = platform.rect.x - self.rect.width
      elif platform.rect.x + platform.rect.width -5 <= self.rect.x <= platform.rect.x+platform.rect.width:
        self.rect.x = platform.rect.x + platform.rect.width
      else:
        # reset position of block based on jump/fall
        # falling reset position
        if self.change_y > 0:
          self.rect.y = platform.rect.y - self.rect.height
          self.on_ground = True
        # jumping reset position
        elif self.change_y < 0:
          self.rect.y = platform.rect.y + platform.rect.height
          
        # set gravity to 0
        self.change_y = 0

  def coin_collide(self, goal):
    if self.rect.colliderect(goal.rect):
        return True
    else:
        return False
  
class Platform(pygame.sprite.Sprite):
  def __init__(self, x, y, w, h):
    #constructor
    super().__init__()
    self.platform = pygame.image.load("./block.png")
    self.platform = pygame.transform.scale(self.platform, (20, 20))
    self.rect = pygame.Rect(x, y, w, h)

  def draw(self, screen):
    pygame.draw.rect(screen, "black", self.rect)
    screen.blit(self.platform, self.rect)
    for i in range(self.rect.width // 20):
      destination = pygame.Rect(self.rect.x + (i) * 20,self.rect.y, 20, 20)
      screen.blit(self.platform, destination)
    
class Coin(pygame.sprite.Sprite):
  def __init__(self, x, y, w, h):
    #constructor
    super().__init__()
    self.rect = pygame.Rect(x, y, w, h)
    self.visible = True
    self.image = pygame.image.load("star_coin.png")
    self.image = pygame.transform.scale(self.image, (w, h))
    
  def draw(self, screen):
    if self.visible == True:
      screen.blit(self.image, self.rect)

class Bg(pygame.sprite.Sprite):
  def __init__(self):
    #constructor
    super().__init__()
    self.bg = pygame.image.load("./mario_bg.png")
    self.bg = pygame.transform.scale(self.bg, (500, 500))

  def draw(self, screen):
    screen.blit(self.bg, self.bg.get_rect())

