import pygame,sys,math,time,copy,datetime,json,math,random
import numpy as np

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
ORANGE = (255, 127, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

G = 6.673 * 1e-11
SB_CONSTANT = 5.6696e-8
M_SUN = 1.98892e+30
M_EARTH = 5.9722e+24
R_SUN = 696340
R_EARTH = 6371
AU = 149597870700

camSize = 1

def add_h(arg):
    h = 1e-6
    return int(arg/(camSize+h))

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
        x = math.cos(math.radians(self.theta)) * self.value
        y = math.sin(math.radians(self.theta)) * self.value
        return PVector(x,y)

class Mass:
    def __init__(self, pos, M, force = Vector(0,0), velocity = Vector(0,0)) -> None:
        self.M = M
        self.x = pos[0]
        self.y = pos[1]
        self.velocity = velocity
        self.force = force

    def tick(self,others):
        for other in others:
            r = math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
            degree = math.atan2(self.y-other.y, self.x-other.x)*180/math.pi
            self.force += Vector(degree, -G * other.M / (r**2))
        self.velocity += self.force
        posForce = self.velocity.convert()
        self.x += posForce.x
        self.y += posForce.y

class Sun(Mass):
    def __init__(self, pos, R, M, T, force=Vector(0, 0), velocity=Vector(0, 0)) -> None:
        super().__init__(pos, M, force=force, velocity=velocity)
        self.T = T
        self.R = R
        self.L = 4 * math.pi * (R ** 2) * SB_CONSTANT * (T ** 4)
        
    def draw(self,screen):
        x,y = SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)
        pygame.draw.circle(screen, YELLOW, (x, y), max(5.5,add_h(self.R*1.1)))
        pygame.draw.circle(screen, ORANGE, (x, y), max(5,add_h(self.R)))

class Planet(Mass):
    def __init__(self, pos, R, M, force=Vector(0, 0), velocity=Vector(0, 0)) -> None:
        super().__init__(pos, M, force=force, velocity=velocity)
        self.R = R
    
    def draw(self,screen):
        x,y = SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)
        pygame.draw.circle(screen, BLUE, (x, y),max(1.1,add_h(self.R * 1.1)))
        pygame.draw.circle(screen, GREEN, (x, y), max(1,add_h(self.R))) 

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("EARTH SCIENCE")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    #things = [Planet((-20,-5), 3, 300), Planet((20,5), 3, 300, velocity= Vector(90,0))]
    things = []
    for x in range(10):
        for y in range(10):
            a = random.randint(1,100000000)
            things.append(Planet((x*5,y*5),0.0000001*a,a))
    while True:
        #clock.tick(1000000000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(BLACK)
        pygame.draw.line(screen,WHITE,(0,SCREEN_HEIGHT/2),(SCREEN_WIDTH,SCREEN_HEIGHT/2))
        pygame.draw.line(screen,WHITE,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
        for i in range(len(things)):
            thing = things[i]
            temp = things[:]
            temp.pop(i)
            thing.tick(temp)
            thing.draw(screen)
        pygame.display.update()