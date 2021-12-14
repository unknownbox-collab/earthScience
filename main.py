import pygame,sys,math,time,copy,datetime,json,math
import numpy as np

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

WHITE = (255, 255, 255)
ORANGE = (255, 127, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

G = 6.673 * 1e-11
SB_CONSTANT = 5.6696e-8

class PVector:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def __add__(self,other):
        x,y = self.x + other.x , self.y + other.y
        return PVector(x,y)

    def __sub__(self,other):
        x,y = self.x - other.x , self.y - other.y
        return PVector(x,y)
    
    def convert(self):
        theta = math.atan2(self.y,self.x) * 180 / math.pi
        value = (self.x**2 + self.y**2)**0.5
        return Vector(theta,value)

class Vector:
    def __init__(self,theta,value) -> None:
        self.theta = theta
        self.value = value
    
    def __add__(self,other):
        S = self.convert()
        O = other.convert()
        return (S+O).convert()
    
    def __sub__(self,other):
        S = self.convert()
        O = other.convert()
        return (S-O).convert()
    
    def convert(self):
        x = math.cos(self.theta) * self.value
        y = math.sin(self.theta) * self.value
        return PVector(x,y)

class Mass:
    def __init__(self, pos, M, force = Vector(0,0), velocity = Vector(0,0)) -> None:
        self.M = M
        self.x = pos[0]
        self.y = pos[1]
        self.velocity = velocity
        self.force = force

    def tick(self,others):
        for other in range(len(others)):
            r = math.sqrt((other.x - self.x) ** 2 + (other - self.y) ** 2)
            self.force += G * self.M * other.M / (r**2)
        self.velocity += self.force
        posForce = self.velocity.convert()
        self.x, self.y += posForce.x, posForce.y

class Sun(Mass):
    def __init__(self, pos, R, M, T, force=Vector(0, 0), velocity=Vector(0, 0)) -> None:
        super().__init__(pos, M, force=force, velocity=velocity)
        self.T = T
        self.R = R
        self.L = 4 * math.pi * (R ** 2) * SB_CONSTANT * (T ** 4)
        
    def draw(self,screen):
        pygame.draw.circle(screen, ORANGE, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), add_h(55))
        pygame.draw.circle(screen, RED, (SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)), add_h(50)) 

class Planet(Mass):
    def __init__(self, pos, R, M, force=Vector(0, 0), velocity=Vector(0, 0)) -> None:
        super().__init__(pos, M, force=force, velocity=velocity)
        self.R = R

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("EARTH SCIENCE")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sun = Sun((0,0), 1000, 100, 100)
    planet = Planet((10000,0), 10, 10, velocity = Vector(0,10))
    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            