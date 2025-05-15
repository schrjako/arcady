import pygame
import sys
import math
import random

from vector import Vector

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drag-to-Shoot Ball")


    
class Ball:
    def __init__(self, s, gravity):
        self.s=s
        self.radius = 25
        self.color = (255, 0, 0)
        self.v=Vector(0.1, 0.2)
        self.gravity=gravity
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.s.totuple, self.radius)
    
    def move(self):
        if self.s.x + self.radius>screen_width or self.s.x - self.radius<0:
            self.v.x*=-1
        if self.s.y + self.radius>screen_height:
            self.s.y=screen_height-self.radius
            self.v.y*=-1
            self.v*=0.7
        self.v.y+=self.gravity
        
        self.s+=self.v
        
    
    def collision(self, tocke):
        ind=1
        ind2=0
        closest_dis=(tocke[1]-self.s).magnitude
        for a in range(2, len(tocke)-1):
            dis=(tocke[a]-self.s).magnitude
            if dis<closest_dis:
                closest_dis=dis
                ind=a
                
        if (tocke[ind-1]-self.s).magnitude< (tocke[ind+1]-self.s).magnitude:
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind-1].totuple, 5)
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind].totuple, 5)
            ind2=ind-1
            
            ind, ind2=ind2, ind
        else:
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind+1].totuple, 5)
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind].totuple, 5)
            ind2=ind+1
        v=tocke[ind]-tocke[ind2]
        vr=Vector(-v.y, v.x)
        pygame.draw.line(screen, (0, 255, 0), tocke[ind].totuple,(tocke[ind]+vr*10).totuple, 2)
        pygame.draw.line(screen, (0, 0, 250), self.s.totuple, (self.s+self.v*300).totuple, 2)
        if closest_dis<=self.radius:
            b=vr.normalized
            b2=-1.7*(b*self.v)
            b3=b*b2
            nv=b3+self.v
            self.v=nv
            
        
def getBezierPoint2(t, end1, anc1, end2):
        V = end1*(1-t)**2 + anc1*2*(1-t)*t  + end2*t**2
        return V


class Bezierjeva():
    def __init__(self, prev_cont: Vector, prev_end: Vector, width):
        krivulje.append(self)
        self.start=prev_end
        v=self.start-prev_cont
        self.control=self.start+v
        self.end=Vector(self.start.x+width, self.start.y+random.uniform(-70, 70))
        self.acc=30
        self.points = [Vector(0, 0) for i in range(self.acc+1)]
        for i in range(len(self.points)):
            self.points[i] = getBezierPoint2(i/self.acc, self.start, self.control, self.end)

    def draw(self):
        for i in range(self.acc):
            pygame.draw.line(screen, (255, 255, 255), self.points[i].totuple, self.points[i+1].totuple, 3)
    
    


krivulje=[]
st_krivulj=random.randint(3, 8)
zac=Vector(0, 400)
kont=Vector(-random.uniform(screen_width/st_krivulj, (screen_width/st_krivulj)/2), 450)
for i in range(st_krivulj):
    print(zac, kont)
    bezierjeva=Bezierjeva(kont, zac, screen_width/st_krivulj)
    zac=bezierjeva.end
    kont=bezierjeva.control
    print(zac, kont)
tocke=[]
for krivulja in krivulje:
    for tocka in krivulja.points:
        if len(tocke)==0 or tocke[len(tocke)-1]!=tocka:
            tocke.append(tocka)

ball=Ball(Vector(screen_width//2, 100), 0.0001)

strtpos=Vector(0, 0)
run=True
while run:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            strtpos=Vector(*pygame.mouse.get_pos())
        if event.type==pygame.MOUSEBUTTONUP:
            if ball.s.y+ball.radius>=screen_height:
                endpos=Vector(*pygame.mouse.get_pos())
                v=(endpos-strtpos)*-0.001
                ball.v+=v

            
            
    if pygame.mouse.get_pressed()[0]:
        mp=Vector(*pygame.mouse.get_pos())
        pygame.draw.line(screen, (255, 255, 255), ball.s.totuple, (ball.s-(mp-strtpos)).totuple, 2)
    for krivulja in krivulje:
        krivulja.draw()
    ball.move()
    ball.draw()
    ball.collision(tocke)
    

    pygame.display.flip()





