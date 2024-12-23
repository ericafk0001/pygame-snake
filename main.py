import os
import sys
import pygame
import random

pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    try:
      base_path = sys._MEIPASS
    except Exception:
      base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

snake_head_img = pygame.image.load(resource_path("assets/snake_head.png"))
eat_sound = pygame.mixer.Sound(resource_path("assets/eat.wav"))
death_sound = pygame.mixer.Sound(resource_path("assets/death.mp3"))
pygame.mixer.music.load(resource_path("assets/monday.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

eat_sound.set_volume(0.2)
death_sound.set_volume(0.2)

DARK_GREEN = (19, 66, 13)
GREEN = (0, 255, 0)

SW, SH = 1000, 1000
BLOCK_SIZE = 50
FONT= pygame.font.Font(resource_path("assets/PixelifySans-Regular.ttf"), BLOCK_SIZE*2)

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
#checkboard grid
def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0:
                color = "#53c449"  
            else:
                color = "#308f25" 
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, color, rect)


class Snake: 
  def __init__(self):
    self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
    self.xdir = 1
    self.ydir = 0
    self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
    self.dead = False

  def update(self):
    global apple

    for square in self.body: 
      if self.head.x == square.x and self.head.y == square.y:
        self.dead = True
      if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
        self.dead = True

    if self.dead:
      death_sound.play()
      self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
      self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
      self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
      self.xdir = 1
      self.ydir = 0
      self.dead = False
      apple = Apple()
  
    self.body.append(self.head)
    for i in range(len(self.body)-1):
      self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
    self.head.x += self.xdir * BLOCK_SIZE
    self.head.y += self.ydir * BLOCK_SIZE
    self.body.remove(self.head)

class Apple:
  def __init__(self):
    self.images = [
      pygame.image.load(resource_path("assets/8.png")),
      pygame.image.load(resource_path("assets/17.png")),
      pygame.image.load(resource_path("assets/24.png")),
      pygame.image.load(resource_path("assets/65.png")),
      pygame.image.load(resource_path("assets/85.png"))
    ]
    self.image = random.choice(self.images)
    self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

    #randomize food position
    self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
    self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
    self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

  def update(self):
    screen.blit(self.image, (self.x, self.y))

score = FONT.render("0", True, "white")
score_rect = score.get_rect(center=(SW/2, SH/20))

drawGrid()
snake = Snake()
apple = Apple()

#game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_DOWN:
        snake.ydir = 1
        snake.xdir = 0
      elif event.key == pygame.K_UP:
        snake.ydir = -1
        snake.xdir = 0
      elif event.key == pygame.K_RIGHT:
        snake.ydir = 0
        snake.xdir = 1
      elif event.key == pygame.K_LEFT:
        snake.ydir = 0
        snake.xdir = -1

  snake.update()
  screen.fill("black")
  drawGrid()
  apple.update()
  score = FONT.render(f"{len(snake.body)-1}", True, "white")

  if snake.xdir == 1:  
    rotated_image = pygame.transform.rotate(snake_head_img, 0)
  elif snake.xdir == -1:  
      rotated_image = pygame.transform.rotate(snake_head_img, 180)
  elif snake.ydir == -1:  
      rotated_image = pygame.transform.rotate(snake_head_img, 90)
  elif snake.ydir == 1:
      rotated_image = pygame.transform.rotate(snake_head_img, -90)

  screen.blit(rotated_image, (snake.head.x, snake.head.y))

  for index, square in enumerate(snake.body):
     color = DARK_GREEN if index % 2 == 0 else GREEN
     pygame.draw.rect(screen, color, square)

  screen.blit(score, score_rect)

  if snake.head.x == apple.x and snake.head.y == apple.y:
    eat_sound.play()
    snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
    apple = Apple()

  pygame.display.update()
  clock.tick(10)