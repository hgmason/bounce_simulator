import pygame, sys
from pygame.locals import *
import time
import random
import colorsys

#constants
height = 500
width = 700
MOUSE_DOWN = MOUSEBUTTONDOWN
MOUSE_UP = MOUSEBUTTONUP
MOUSE_MOVE = MOUSEMOTION
recent = 50
tic = 10
KeyDown = KEYDOWN

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 56, 215)

class Ball:
    def __init__(self, ballpos, init_speed = 0, horz_speed = 0, size = 20, color = WHITE):
        self.ballpos = ballpos
        self.size = size
        self.anim = False
        self.x = 0
        self.init_speed = init_speed
        self.current_speed = 0
        self.init_posit = ballpos[1]
        self.scalar = .85
        self.horz_speed = horz_speed
        self.count = 0
        self.color = color
        self.friction = .995
    def update(self):
        #The equation is: s = ut + (1/2)a t^2
        #where s is position, u is velocity at t=0, t is time and a is a constant acceleration.
        a = height/2000
        self.ballpos[1] = int(self.init_speed*self.x + .5*a*self.x**2) + self.init_posit
        self.current_speed = a*self.x + self.init_speed
        if (self.ballpos[1] >= (height - self.size//2)):
            self.init_posit = (height - self.size//2)
            self.init_speed = -1*self.current_speed*self.scalar
            self.x = 0
        if self.horz_speed > 0:
            self.ballpos[0] = int((self.ballpos[0] + self.horz_speed)%width)
        else:
            self.ballpos[0] = int((self.ballpos[0] + self.horz_speed)%width)
        #print(self.ballpos[0])
        self.x = self.x + 1
        self.horz_speed = self.horz_speed * self.friction
        if abs(self.horz_speed) < .3:
            self.horz_speed = 0
        return
    def draw(self):
        pygame.draw.circle(windowSurface, self.color, self.ballpos, self.size, 0)
        None

def millis():
    return time.time()*1000

def get_random_color():
    R = random.randint(0,255)
    G = random.randint(0,255)
    B = random.randint(0,255)
    H,L,S = colorsys.rgb_to_hls(R, G, B)
    S = abs(S)
    good = (S > .5) and (L > 70)
    if not good:
        return get_random_color()
    else:
        return (R,G,B)

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('bouncey')

# draw the background onto the surface
windowSurface.fill(BLACK)

# draw the window onto the screen
pygame.display.update()

start = millis()
mouse_moved = millis()

pressed = False
horz_speed = 0
init_speed = 0
balls = []
current_pos = [0,0]
current_size = random.randint(25,35)
current_color = get_random_color()

print("------------------------------------------------------")
print("  Welcome to the Bounce Simulator. Click and drag to")
print("  spawn and throw a ball. Press space to randomly")
print("  agitate all existing balls. Watch the simulation!")
print("  ~created by @hgmason on github~")
print("------------------------------------------------------")

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == KeyDown:
            #print(event.key)
            if event.key == 32:
                for ball in balls:
                    ball.init_speed = ball.init_speed + random.randint(1,10) * ball.current_speed/abs(ball.current_speed)
                    try:
                        ball.horz_speed = ball.horz_speed + random.randint(1,10) * ball.horz_speed/abs(ball.horz_speed)
                    except:
                        ball.horz_speed = random.randint(-10,10)
            if event.key == 27:
                balls = []
        if event.type == MOUSE_MOVE and pressed:
            rel = event.rel
            horz_speed = rel[0]/5
            init_speed = rel[1]/5
            mouse_moved = millis()
            current_pos = event.pos
        if event.type == MOUSE_DOWN:
            pressed = True
            current_pos = event.pos
        if event.type == MOUSE_UP:
            pressed = False
            ballpos = [event.pos[0],event.pos[1]]
            if (millis() - mouse_moved) > recent:
                horz_speed = 0
                init_speed = 0
            balls.append(Ball(ballpos, init_speed, horz_speed, current_size, current_color))
            current_size = random.randint(10,50)
            current_color = get_random_color()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if (millis() - start >= tic):
    #if True:
        windowSurface.fill(BLACK)
        start = millis()
        if pressed:
            pygame.draw.circle(windowSurface, current_color, current_pos, current_size, 0)
        for ball in balls:
            ball.update()
            ball.draw()
        pygame.display.update()
# draw a circle onto the surface
#pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)
