from os import write
import pygame,sys,math,time,copy,datetime,json,math,random,colour
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
M_MARS = 6.39e+23
R_SUN = 696340
R_EARTH = 6371
R_MARS = 3389.5
AU = 149597870.700
PC = 1/math.tan(math.pi/648000)*AU
C = 299792458

camSize = 0.5 * AU

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
            self.velocity += Vector(degree, -G * other.M / (r**2))
        #self.velocity += self.force
        posForce = self.velocity.convert()
        self.x += posForce.x
        self.y += posForce.y

class Sun(Mass):
    def __init__(self, pos, R, M, T, force=Vector(0, 0), velocity=Vector(0, 0)) -> None:
        super().__init__(pos, M, force=force, velocity=velocity)
        self.T = T
        self.wave = 2.898 * 10**(-3) / T
        self.waveObsv = self.wave
        self.R = R
        self.L = 4 * math.pi * (R ** 2) * SB_CONSTANT * (T ** 4)
        
    def draw(self,screen):
        blackBody = {
   1000 : "#ff3800", 
   1200 : "#ff5300", 
   1400 : "#ff6500", 
   1600 : "#ff7300", 
   1800 : "#ff7e00", 
   2000 : "#ff8912", 
   2200 : "#ff932c", 
   2400 : "#ff9d3f", 
   2600 : "#ffa54f", 
   2800 : "#ffad5e", 
   3000 : "#ffb46b", 
   3200 : "#ffbb78", 
   3400 : "#ffc184", 
   3600 : "#ffc78f", 
   3800 : "#ffcc99", 
   4000 : "#ffd1a3", 
   4200 : "#ffd5ad", 
   4400 : "#ffd9b6", 
   4600 : "#ffddbe", 
   4800 : "#ffe1c6", 
   5000 : "#ffe4ce", 
   5200 : "#ffe8d5", 
   5400 : "#ffebdc", 
   5600 : "#ffeee3", 
   5800 : "#fff0e9", 
   6000 : "#fff3ef", 
   6200 : "#fff5f5", 
   6400 : "#fff8fb", 
   6600 : "#fef9ff", 
   6800 : "#f9f6ff", 
   7000 : "#f5f3ff", 
   7200 : "#f0f1ff", 
   7400 : "#edefff", 
   7600 : "#e9edff", 
   7800 : "#e6ebff", 
   8000 : "#e3e9ff", 
   8200 : "#e0e7ff", 
   8400 : "#dde6ff", 
   8600 : "#dae4ff", 
   8800 : "#d8e3ff", 
   9000 : "#d6e1ff", 
   9200 : "#d3e0ff", 
   9400 : "#d1dfff", 
   9600 : "#cfddff", 
   9800 : "#cedcff", 
  10000 : "#ccdbff", 
  10200 : "#cadaff", 
  10400 : "#c9d9ff", 
  10600 : "#c7d8ff", 
  10800 : "#c6d8ff", 
  11000 : "#c4d7ff", 
  11200 : "#c3d6ff", 
  11400 : "#c2d5ff", 
  11600 : "#c1d4ff", 
  11800 : "#c0d4ff", 
  12000 : "#bfd3ff", 
  12200 : "#bed2ff", 
  12400 : "#bdd2ff", 
  12600 : "#bcd1ff", 
  12800 : "#bbd1ff", 
  13000 : "#bad0ff", 
  13200 : "#b9d0ff", 
  13400 : "#b8cfff", 
  13600 : "#b7cfff", 
  13800 : "#b7ceff", 
  14000 : "#b6ceff", 
  14200 : "#b5cdff", 
  14400 : "#b5cdff", 
  14600 : "#b4ccff", 
  14800 : "#b3ccff", 
  15000 : "#b3ccff", 
  15200 : "#b2cbff", 
  15400 : "#b2cbff", 
  15600 : "#b1caff", 
  15800 : "#b1caff", 
  16000 : "#b0caff", 
  16200 : "#afc9ff", 
  16400 : "#afc9ff", 
  16600 : "#afc9ff", 
  16800 : "#aec9ff", 
  17000 : "#aec8ff", 
  17200 : "#adc8ff", 
  17400 : "#adc8ff", 
  17600 : "#acc7ff", 
  17800 : "#acc7ff", 
  18000 : "#acc7ff", 
  18200 : "#abc7ff", 
  18400 : "#abc6ff", 
  18600 : "#aac6ff", 
  18800 : "#aac6ff", 
  19000 : "#aac6ff", 
  19200 : "#a9c6ff", 
  19400 : "#a9c5ff", 
  19600 : "#a9c5ff", 
  19800 : "#a9c5ff", 
  20000 : "#a8c5ff", 
  20200 : "#a8c5ff", 
  20400 : "#a8c4ff", 
  20600 : "#a7c4ff", 
  20800 : "#a7c4ff", 
  21000 : "#a7c4ff", 
  21200 : "#a7c4ff", 
  21400 : "#a6c3ff", 
  21600 : "#a6c3ff", 
  21800 : "#a6c3ff", 
  22000 : "#a6c3ff", 
  22200 : "#a5c3ff", 
  22400 : "#a5c3ff", 
  22600 : "#a5c3ff", 
  22800 : "#a5c2ff", 
  23000 : "#a4c2ff", 
  23200 : "#a4c2ff", 
  23400 : "#a4c2ff", 
  23600 : "#a4c2ff", 
  23800 : "#a4c2ff", 
  24000 : "#a3c2ff", 
  24200 : "#a3c1ff", 
  24400 : "#a3c1ff", 
  24600 : "#a3c1ff", 
  24800 : "#a3c1ff", 
  25000 : "#a3c1ff", 
  25200 : "#a2c1ff", 
  25400 : "#a2c1ff", 
  25600 : "#a2c1ff", 
  25800 : "#a2c1ff", 
  26000 : "#a2c0ff", 
  26200 : "#a2c0ff", 
  26400 : "#a1c0ff", 
  26600 : "#a1c0ff", 
  26800 : "#a1c0ff", 
  27000 : "#a1c0ff", 
  27200 : "#a1c0ff", 
  27400 : "#a1c0ff", 
  27600 : "#a1c0ff", 
  27800 : "#a0c0ff", 
  28000 : "#a0bfff", 
  28200 : "#a0bfff", 
  28400 : "#a0bfff", 
  28600 : "#a0bfff", 
  28800 : "#a0bfff", 
  29000 : "#a0bfff", 
  29200 : "#a0bfff", 
  29400 : "#9fbfff", 
  29600 : "#9fbfff", 
  29800 : "#9fbfff"
  }
        color = colour.hex2rgb(blackBody[round(self.T/100)*100])
        color = tuple(map(lambda x: x*255,color))
        x,y = SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)
        pygame.draw.circle(screen, color, (x, y), max(2.2,add_h(self.R*1.1)))
        pygame.draw.circle(screen, color, (x, y), max(2,add_h(self.R)))

class Planet(Mass):
    def __init__(self, pos, R, M, force=Vector(0, 0), velocity=Vector(0, 0)) -> None:
        super().__init__(pos, M, force=force, velocity=velocity)
        self.R = R
    
    def draw(self,screen):
        x,y = SCREEN_WIDTH/2+add_h(self.x), SCREEN_HEIGHT/2+add_h(self.y)
        pygame.draw.circle(screen, BLUE, (x, y),max(1.1,add_h(self.R * 1.1)))
        pygame.draw.circle(screen, YELLOW, (x, y), max(1,add_h(self.R))) 

num = 0
sums = 0
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("EARTH SCIENCE")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    #things = [Planet((-20,-5), 3, 300), Planet((20,5), 3, 300, velocity= Vector(90,0))]
    things = []
    #for x in range(2):
    #    for y in range(2):
    #        a = random.randint(1,1000)
    things.append(Sun((0,0),R_SUN,M_SUN,5800))
    a = 1 * AU #EARTH
    things.append(Planet((0,a),R_EARTH,M_EARTH,velocity=Vector(180, math.sqrt(1*G*M_SUN/a))))
    b = 1.52 * AU #MARS
    things.append(Planet((0,b),R_MARS,M_MARS,velocity=Vector(180, math.sqrt(1*G*M_SUN/b))))
    c = 0.387 * AU #MERCURY
    things.append(Planet((0,c),R_EARTH * 0.383,M_EARTH * 0.055,velocity=Vector(180, math.sqrt(1*G*M_SUN/c))))
    d = 0.72333199 * AU #VINUS
    things.append(Planet((0,d),R_EARTH * 0.949,M_EARTH * 0.815,velocity=Vector(180, math.sqrt(1*G*M_SUN/d))))
    e = 4.950429 * AU #Jupiter
    things.append(Planet((0,e),139822/2,1.8986e+27,velocity=Vector(180, math.sqrt(1*G*M_SUN/e))))
    e = 9.554909 * AU #s
    things.append(Planet((0,e),9.449 * R_EARTH,95.162 * M_EARTH,velocity=Vector(180, math.sqrt(1*G*M_SUN/e))))
    e = 19.19126393 * AU #s
    things.append(Planet((0,e),51118/2,8.6832e+25,velocity=Vector(180, math.sqrt(1*G*M_SUN/e))))
    e = 30.11 * AU #s
    things.append(Planet((0,e),24,622,1.02413e+26,velocity=Vector(180, math.sqrt(1*G*M_SUN/e))))
    file = open('./result.txt','a')
    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            camSize /= 1.01
        if pressed[pygame.K_s]:
            camSize *= 1.01
        if pressed[pygame.K_SPACE]:
            file.close()
        screen.fill(BLACK)
        pygame.draw.line(screen,WHITE,(0,SCREEN_HEIGHT/2),(SCREEN_WIDTH,SCREEN_HEIGHT/2))
        pygame.draw.line(screen,WHITE,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
        preMove = things[0].y
        for i in range(len(things)):
            thing = things[i]
            temp = things[:]
            temp.pop(i)
            thing.tick(temp)
            thing.draw(screen)
        #print(things[1].force.theta,things[1].force.value,things[1].velocity.theta,things[1].velocity.value)
        #print(things[0].x,things[0].y,"/",things[0].x-preMove[0],-things[0].y+preMove[1])
        v = things[0].y-preMove
        wave = (-v/(-v-C))*things[0].wave
        things[0].waveObsv = wave
        #file.write(str(things[0].waveObsv)+"\n")
        #print(v[1],wave/things[0].wave * C)
        pygame.display.update()