import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drag-to-Shoot Ball")




class Ball:
    def __init__(self, x, y, gravity):
        self.x=x
        self.y=y
        self.radius = 25
        self.color = (255, 0, 0)
        self.vX=0.1
        self.vY=0.2
        self.gravity=gravity
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        if self.x + self.radius>screen_width or self.x - self.radius<0:
            self.vX*=-1
        if self.y + self.radius>screen_height:
            self.y=screen_height-self.radius
            self.vY*=-1
            self.vY*=0.7
            self.vX*=0.7
        self.vY+=self.gravity
        
        self.x+=self.vX
        self.y+=self.vY
        
    
    def collision(self, tocke):
        ind=1
        ind2=0
        closest_dis=math.sqrt((tocke[1][0]-self.x)**2+(tocke[1][1]-self.y)**2)
        for a in range(2, len(tocke)-1):
            dis=math.sqrt((tocke[a][0]-self.x)**2+(tocke[a][1]-self.y)**2)
            if dis<closest_dis:
                closest_dis=dis
                ind=a
        #if math.sqrt((tocke[a-1][0]-self.x)**2+(tocke[a-1][1]-self.y)**2)<math.sqrt((tocke[a+1][0]-self.x)**2+(tocke[a+1][1]-self.y)**2):
        if math.sqrt((tocke[ind-1][0]-self.x)**2+(tocke[ind-1][1]-self.y)**2)<math.sqrt((tocke[ind+1][0]-self.x)**2+(tocke[ind+1][1]-self.y)**2):
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind-1], 5)
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind], 5)
            ind2=ind-1
            
            ind, ind2=ind2, ind
        else:
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind+1], 5)
            pygame.draw.circle(screen, (255, 0, 0), tocke[ind], 5)
            ind2=ind+1
        v=(tocke[ind][0]-tocke[ind2][0], tocke[ind][1]-tocke[ind2][1])
        vr=(-v[1], v[0])
        pygame.draw.line(screen, (0, 255, 0), tocke[ind], (tocke[ind][0]+vr[0]*10, tocke[ind][1]+vr[1]*10), 2)
        pygame.draw.line(screen, (0, 0, 250), (self.x, self.y), (self.x+self.vX*300, self.y+self.vY*300), 2)
        if closest_dis<=self.radius:
            b=(vr[0]/math.sqrt(vr[0]**2 + vr[1]**2), vr[1]/math.sqrt(vr[0]**2 + vr[1]**2))
            b2=-(b[0]*1.7*self.vX + b[1]*1.7*self.vY)
            b3=(b[0]*b2, b[1]*b2)
            nv=(b3[0]+self.vX, b3[1]+self.vY)
            self.vX=nv[0]
            self.vY=nv[1]
            '''pygame.draw.line(screen, (100,100, 0), (self.x, self.y), (self.x+self.vX*300, self.y+self.vY*300), 2)
            pygame.display.flip()
            while True:
                self.vX=0
                self.vY=0'''
            
        
def getBezierPoint2(t, end1X, end1Y, anc1X, anc1Y, end2X, end2Y):
        x = (1-t)**2 * end1X + 2*(1-t)*t * anc1X + t**2 * end2X
        y = (1-t)**2 * end1Y + 2*(1-t)*t * anc1Y + t**2 * end2Y
        return (x, y)


class Bezierjeva():
    def __init__(self, prev_cont, prev_end, width):
        krivulje.append(self)
        self.start=prev_end
        v=(self.start[0]-prev_cont[0], self.start[1]- prev_cont[1])
        self.control=(self.start[0]+v[0], self.start[1]+v[1])
        self.end=(self.start[0]+width, self.start[1]+random.uniform(-70, 70))
        self.acc=30
        self.points = [(0, 0) for i in range(self.acc+1)]
        for i in range(len(self.points)):
            self.points[i] = getBezierPoint2(i/self.acc, self.start[0], self.start[1], self.control[0], self.control[1], self.end[0], self.end[1])

    def draw(self):
        for i in range(self.acc):
            pygame.draw.line(screen, (255, 255, 255), self.points[i], self.points[i+1], 3)
    
    


krivulje=[]
st_krivulj=random.randint(3, 8)
zac=(0, 400)
kont=(-random.uniform(screen_width/st_krivulj, (screen_width/st_krivulj)/2), 450)
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

ball=Ball(screen_width//2, 100, 0.0001)

strtpos=(0, 0)
run=True
while run:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            strtpos=pygame.mouse.get_pos()
        if event.type==pygame.MOUSEBUTTONUP:
            if ball.y+ball.radius>=screen_height:
                endpos=pygame.mouse.get_pos()
                v=((endpos[0]-strtpos[0])*-0.001,(endpos[1]-strtpos[1])*-0.001)
                ball.vX+=v[0]
                ball.vY+=v[1]
            
            
    if pygame.mouse.get_pressed()[0]:
        mp=pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (ball.x, ball.y), (ball.x-(mp[0]-strtpos[0]), ball.y-(mp[1]-strtpos[1])), 2)
    for krivulja in krivulje:
        krivulja.draw()
    ball.move()
    ball.draw()
    ball.collision(tocke)
    

    pygame.display.flip()





