import pygame, sys
from pygame.locals import *
import time
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

title ="Snake"

BLACK = (0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)

LEFT = (-25, 0)
RIGHT = (25, 0)
UP = (0, -25)
DOWN = (0, 25)


class Fruit:
    def __init__(self):
        self.x = random.randint(0, 19) * 25
        self.y = random.randint(0, 19) * 25
        self.color = RED

class Body:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        pygame.init()
        self.fruit = []
        self.fruit.append(Fruit())
        self.snake_parts = [Body(250, 250)]
        self.direction = UP
        self.timer = 0
        self.DISPLAY=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        self.DISPLAY.fill(BLACK)
        self.TARGET_FPS = 120
        self.prev_time = time.time()
        self.menu_loop()

    def updateFPS(self):
        curr_time = time.time()
        diff = curr_time - self.prev_time
        delay = max(1.0/self.TARGET_FPS - diff, 0) 
        time.sleep(delay)
        fps = 1.0/(delay + diff)
        self.prev_time = curr_time
        return fps


    def moveSnake(self):
        # Update Elements
        if self.timer % 30 == 0:
            for i, part in reversed(list(enumerate(self.snake_parts))):
                if i == 0:
                    part.x += self.direction[0]
                    part.y += self.direction[1]
                else:
                    part.x = self.snake_parts[i-1].x
                    part.y = self.snake_parts[i-1].y


    def detectInputs(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.direction == RIGHT:
            self.direction = LEFT
        elif keys[pygame.K_d] and not self.direction == LEFT:
            self.direction = RIGHT
        elif keys[pygame.K_w] and not self.direction == DOWN:
            self.direction = UP
        elif keys[pygame.K_s] and not self.direction == UP:
            self.direction = DOWN

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

    def detectCollisions(self):
        # Out of bounds
        c = self.snake_parts[0]
        if (c.x < 0 or c.x >= WINDOW_WIDTH or c.y < 0 or c.y >= WINDOW_HEIGHT):
            font = pygame.font.SysFont(None, 25)
            img = font.render('You are die', True, WHITE)
            self.DISPLAY.blit(img, (200, 200))
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        # Test for hit tail
        c = self.snake_parts[0]
        for i, part in list(enumerate(self.snake_parts)):
            if (i != 0 and part.x == c.x and part.y == c.y):
                pygame.quit()
                sys.exit()

        for f in self.fruit:
            # Fruit Eatten
            if f.x == self.snake_parts[0].x and f.y == self.snake_parts[0].y:
                self.fruit.remove(f)
                self.fruit.append(Fruit())
                self.snake_parts.append(Body(self.snake_parts[len(self.snake_parts)-1].x + tuple([-1*x for x in self.direction])[0], self.snake_parts[len(self.snake_parts)-1].y + tuple([-1*x for x in self.direction])[1]))

    def draw(self):
        self.DISPLAY.fill(BLACK)
        # Draw and process fruit
        for f in self.fruit:
            pygame.draw.rect(self.DISPLAY, f.color, (f.x, f.y, 25, 25))

        # Drawing Snake
        for b in self.snake_parts:
            pygame.draw.rect(self.DISPLAY,WHITE,(b.x,b.y,25,25))

    def mainloop(self):
        while True:
            # Handle WASD Events
            self.detectInputs()
            self.moveSnake()
            self.detectCollisions()
            self.draw()

            fps = self.updateFPS()
            pygame.display.set_caption("{0} {1:.2f}".format(title, fps))
            pygame.display.update()
            self.timer += 1

    def menu_loop(self):
        while True:
            self.mainloop()

if __name__ == '__main__':
    snake_run = Snake()
