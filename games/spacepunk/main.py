import pygame
import random


class Entity:
	def __init__(self,pos,r,v,a,k):
		self.pos = pos
		self.r = r
		self.v = v
		self.a = a
		self.k = k
		self.dead = False
	def draw(self,screen):
		pygame.draw.circle(screen, "red", self.pos, self.r)
		self.draw_arrow(screen)
	def draw_arrow(self, screen):
		pygame.draw.line(screen, "black", self.pos, self.pos + self.v//3, width=3)
		pygame.draw.line(screen, "green", self.pos, self.pos + self.a//3, width=3)
	def physics(self,dt):
		self.v += self.a * dt
		self.pos += self.v * dt
		self.check_ship_colision()
	def check_ship_colision(self):
		if self.pos.x < space_ship_pos.x + self.r:
			self.pos.x = space_ship_pos.x + self.r 
			self.v.x *= self.k
		if self.pos.x > space_ship_size.x + space_ship_pos.x -self.r:
			self.pos.x = space_ship_size.x + space_ship_pos.x -self.r 
			self.v.x *= self.k
		if self.pos.y < space_ship_pos.y + self.r:
			self.pos.y = space_ship_pos.y + self.r 
			self.v.y *= self.k
		if self.pos.y > space_ship_size.y + space_ship_pos.x -self.r:
			self.pos.y = space_ship_size.y + space_ship_pos.x -self.r 
			self.v.y *= self.k

class Player(Entity):
	def __init__(self,pos,r,v,a,k):
		self.life = 100
		super().__init__(pos,r,v,a,k)
	def take_damage(self,x):
		self.life -= x

class Bullet(Entity):
	def __init__(self,pos,r,v,a,k,t):
		super().__init__(pos,r,v,a,k)
		self.time = t
	def tick(self,dt):
		self.time -= dt
		if self.time < 0:
			self.dead = True
	def check_player_colision(self,player):
		if(player.pos - self.pos).length() <= player.r + self.r:
			self.dead = True

class Effect:
	def __init__(self,pos,time,r):
		self.pos = pos
		self.time = time
		self.r = r
	def tick(self,dt):
		self.time -= dt
	def draw(self,screen):
		pygame.draw.circle(screen, "orange", self.pos, self.r)
		
class Explosion(Effect):
	def __init__(self,pos,time,r):
		super().__init__(pos,time,r)

class Turret:
	def __init__(self,bullets, player):
		self.size = 25
		self.bullets = bullets
		self.player = player
		self.start_pos = random.randint(0,3)
		self.pos = [pygame.Vector2(scrWidth/2,self.size/2),pygame.Vector2(scrWidth/2,scrHeight-self.size/2),pygame.Vector2(self.size/2,scrHeight/2),pygame.Vector2(scrWidth-self.size/2,scrHeight/2)][self.start_pos]
		self.target_pos = pygame.Vector2(0,0)
		self.cooldown = 0 
		self.cooldown_time = 7 
	def shoot(self):
		v = (self.player.pos - self.pos).normalize() * 100
		self.bullets.append(Bullet(self.pos.copy(), 5, v, pygame.Vector2(0,0), -0.9,10))
		self.cooldown = self.cooldown_time
	def tick(self,dt):
		self.cooldown -= dt
		self.move()
		if self.cooldown < 0:
			self.shoot()
	def draw(self,screen):
		pygame.draw.rect(screen, "darkorchid4", pygame.Rect(self.pos.x-self.size/2,self.pos.y-self.size/2,self.size,self.size))
	def move(self):
		if self.cooldown < 0:
			if self.start_pos == 0 or self.start_pos == 1:
				self.target_pos = pygame.Vector2(random.randint(self.size//2,scrWidth-self.size//2),self.pos.y)
			else:
				target_pos = pygame.Vector2(self.pos.x,random.randint(self.size//2,scrHeight-self.size//2)) 
		self.pos = self.pos * (self.cooldown_time - self.cooldown) / self.cooldown_time + self.target_pos * self.cooldown / self.cooldown_time



scrWidth = 1000
scrHeight = 800

def run(screen):
	pygame.init()
	menuWidth = screen.get_width()
	menuHeight = screen.get_height()
	screen = pygame.display.set_mode((scrWidth, scrHeight))

	running = True
	dt = 0
	clock = pygame.time.Clock()
	
	player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),25,pygame.Vector2(0,0),pygame.Vector2(0,0),-0.2)
	global space_ship_pos
	global space_ship_size
	space_ship_pos = pygame.Vector2(30, 30)
	space_ship_size = pygame.Vector2(scrWidth-60, scrHeight-60)
	space_ship = pygame.Rect(space_ship_pos.x, space_ship_pos.y,space_ship_size.x, space_ship_size.y) 

	bullets = []
	explosions = []
	turrets = [Turret(bullets, player)]


	while running:
		#events
		for event in pygame.event.get():
			 if event.type == pygame.QUIT:
				 running = False
		#inputs
		keys = pygame.key.get_pressed()
		if keys[pygame.K_s]:player.a = pygame.Vector2(0,98)
		if keys[pygame.K_w]:player.a = pygame.Vector2(0,-98)
		if keys[pygame.K_d]:player.a = pygame.Vector2(98,0)
		if keys[pygame.K_a]:player.a = pygame.Vector2(-98,0)
		#physics
		player.physics(dt)
		#entities
		for i, bullet in enumerate(bullets):
			bullet.tick(dt)
			bullet.check_player_colision(player)
			if bullet.dead:
				explosions.append(Explosion(bullet.pos,0.2,50))
				bullets.pop(i)
				continue

			d = (bullet.pos - player.pos).length()
			bullet.a = max((500 - d),0)/500 * player.a
			bullet.physics(dt)

		#turrets
		for turret in turrets:
			turret.tick(dt)
		#render
		screen.fill("green")
		pygame.draw.rect(screen, "blue", space_ship)
		player.draw(screen)
		for turret in turrets:
			turret.draw(screen)
		for bullet in bullets:
			bullet.draw(screen)
		for i, explosion in enumerate(explosions):
			explosion.tick(dt)
			explosion.draw(screen)
			if explosion.time < 0:
				explosions.pop(i)

		pygame.display.flip()

		dt = clock.tick(60)/1000  # limits FPS to 60
	screen = pygame.display.set_mode((menuWidth, menuHeight))


