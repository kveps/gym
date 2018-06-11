import numpy as np
import os
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import cv2
import matplotlib.image as mpimg

from pygame.locals import *
from random import randint
import pygame
import time
 
class Apple:
    step = 50
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
  
class Player:
    step = 50
    direction = 0
    length = 3
 
    def __init__(self, length):
       self.x = [100]
       self.y = [100]
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       for i in range(1, self.length-1):
           self.x[i] = self.x[0] - (i * self.step)
           self.y[i] = self.y[0]
 
    def update(self):
 
        # redefine if useless direction
        if self.direction == 0:
            if self.x[1] == self.x[0] + self.step:
                self.direction = 1
        elif self.direction == 1:
            if self.x[1] == self.x[0] - self.step: 
                self.direction = 0
        elif self.direction == 2:
            if self.y[1] == self.y[0] - self.step: 
                self.direction = 3
        elif self.direction == 3:
            if self.y[1] == self.y[0] + self.step: 
                self.direction = 2

        # update previous positions
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update position of head of snake
        if self.direction == 0:
            self.x[0] = self.x[0] + self.step
        if self.direction == 1:
            self.x[0] = self.x[0] - self.step
        if self.direction == 2:
            self.y[0] = self.y[0] - self.step
        if self.direction == 3:
            self.y[0] = self.y[0] + self.step
 
        # print self.x[0], self.y[0] 

    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
 
class SnakeApp:
 
    windowWidth = 500
    windowHeight = 500
    player = 0
    apple = 0
    step = 50
    disp_data = None
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.player = Player(3) 
        self.apple = Apple(5,5)
        self.ate_apple = False
        self.collision = True
        self.on_init()
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode([self.windowWidth,self.windowHeight])
 
        pygame.display.set_caption('Snake game')
        self._running = True
        self._image_surf = pygame.image.load("/home/karthik/gym/gym/envs/snake/small_square_blue.png").convert()
        self._apple_surf = pygame.image.load("/home/karthik/gym/gym/envs/snake/small_square_orange.png").convert()
        
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def get_screen_size(self):
        return (self.windowWidth, self.windowHeight)

    def check_status(self):
        self.player.update()
        self.ate_apple = False
        self.collision = False

        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i]):
                self.apple.x = randint(2,8) * self.step
                self.apple.y = randint(2,8) * self.step
                self.player.length = self.player.length + 1
                self.ate_apple = True
  
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i]):
                self.collision = True
                return self.collision

        # does snake collisde with walls?
        for i in range(0, self.windowHeight):
            if self.isCollision(self.player.x[0],self.player.y[0], 0 - 2 * self.step, i - 2 * self.step) or self.isCollision(self.player.x[0],self.player.y[0], self.windowWidth - self.step, i - 2 * self.step):
                self.collision = True
                return self.collision
        for i in range(0, self.windowWidth):
            if self.isCollision(self.player.x[0],self.player.y[0], i - 2 * self.step, 0 - 2 * self.step) or self.isCollision(self.player.x[0],self.player.y[0], i - 2 * self.step, self.windowHeight - self.step):
                self.collision = True
                return self.collision

        return self.collision

    def isCollision(self,x1,y1,x2,y2,bsize = 1):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.apple.draw(self._display_surf, self._apple_surf)
        self.player.draw(self._display_surf, self._image_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self, action):
        if (action == 0):
            self.player.moveRight()

        if (action == 1):
            self.player.moveLeft()

        if (action == 2):
            self.player.moveUp()

        if (action == 3):
            self.player.moveDown()

        game_over = self.check_status()
        time.sleep (50.0 / 1000.0);

        return game_over

    def get_screen(self):
        return self._display_surf

    def get_screen_state(self):
        self.disp_data = pygame.surfarray.array3d(self._display_surf)
        # pygame.image.save(self._display_surf, "image.jpg")
        # im = cv2.imread("image.jpg")
        # b,g,r = cv2.split(im)  
        # im = cv2.merge([r,g,b])
        self.disp_data.swapaxes(0,1)
        return self.disp_data

    def get_score(self):
        if(self.ate_apple):
            return 1
        elif(self.collision):
            return -1
        else:
            return 0

class SnakeEnv(gym.Env):

    action_set = [0, 1, 2, 3]
    num_actions = len(action_set)

    def __init__(self):
        self.snake_app = SnakeApp()

    def get_num_actions(self):
        return self.num_actions

    def step(self, action):        
        if action not in self.action_set:
            print("Dont have action")
            exit(0)
        episode_over = self.snake_app.on_execute(action)
        reward = self.snake_app.get_score()
        ob = self.snake_app.get_screen_state()
        return ob, reward, episode_over, {}

    def reset(self):
        self.snake_app.on_cleanup()
        self.snake_app = SnakeApp()
        ob = self.snake_app.get_screen_state()
        return ob

    def render(self):
        self.snake_app.on_render()

    def get_state_size(self):
        return self.snake_app.get_screen_size()    
