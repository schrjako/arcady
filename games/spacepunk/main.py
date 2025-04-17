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
		super().__init__(self,pos,r,v,a,k)
class Turet:
	def __init__(self,pos):
		pass

def check_bullet_colision(player,bullets):
	for bullet in bullets:
		if(player.pos - bullet.pos).length() <= player.r + bullet.r:
			bullet.dead = True

def run(screen):
	pygame.init()
	menuWidth = screen.get_width()
	menuHeight = screen.get_height()
	scrWidth = 1000
	scrHeight = 800
	screen = pygame.display.set_mode((scrWidth, scrHeight))

	running = True
	dt = 0
	clock = pygame.time.Clock()
	
	player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),25,pygame.Vector2(0,0),pygame.Vector2(0,0),-0.2)
	global space_ship_pos
	global space_ship_size
	space_ship_pos = pygame.Vector2(30, 30)
	space_ship_size = pygame.Vector2(screen.get_width()-60, screen.get_height()-60)
	space_ship = pygame.Rect(space_ship_pos.x, space_ship_pos.y,space_ship_size.x, space_ship_size.y) 

	bullets = []
	explosions = []
	for i in range(10):
		e_pos = pygame.Vector2(random.randint(0,screen.get_width()-1),random.randint(0,screen.get_height()-1))
		e_r = 10
		e_v = pygame.Vector2(random.randint(0,100),random.randint(0,100))
		e_a = pygame.Vector2(0,0)
		bullets.append(Entity(e_pos,e_r,e_v,e_a,-0.9))


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
		check_bullet_colision(player,bullets)
		#entities
		for i, bullet in enumerate(bullets):
			if bullet.dead:
				explosions.append([bullet.pos,0.1])
				bullets.pop(i)
				continue

			d = (bullet.pos - player.pos).length()
			bullet.a = max((500 - d),0)/500 * player.a
			bullet.physics(dt)

		#render
		screen.fill("green")
		pygame.draw.rect(screen, "blue", space_ship)
		player.draw(screen)
		for bullet in bullets:
			bullet.draw(screen)
		for i, explosion in enumerate(explosions):
			pygame.draw.circle(screen, "orange", explosion[0], 100)
			explosion[1] -= dt
			if explosion[1] < 0:
				explosions.pop(i)

		pygame.display.flip()

		dt = clock.tick(60)/1000  # limits FPS to 60
	screen = pygame.display.set_mode((menuWidth, menuHeight))


