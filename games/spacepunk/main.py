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
		self.check_wall_colision()

	def check_wall_colision(self):
		if self.pos.x < self.r:
			self.pos.x = self.r 
			self.v.x *= self.k
		if self.pos.x > scrWidth - self.r:
			self.pos.x = scrWidth -  self.r 
			self.v.x *= self.k
		if self.pos.y < self.r:
			self.pos.y = self.r 
			self.v.y *= self.k
		if self.pos.y > scrHeight - self.r:
			self.pos.y = scrHeight - self.r 
			self.v.y *= self.k


class Player(Entity):
	def __init__(self,pos,r,v,a,k):
		self.health = 100
		super().__init__(pos,r,v,a,k)

	def damage(self,x):
		self.health -= x


class Bullet(Entity):
	def __init__(self,pos,r,v,a,k,t, player):
		super().__init__(pos,r,v,a,k)
		self.time = t
		self.player = player

	def tick(self,dt):
		self.time -= dt
		if self.time < 0:
			self.dead = True
			effects.append(Explosion(self.pos,0.2,50,self.player))

	def check_player_colision(self,player):
		if(player.pos - self.pos).length() <= player.r + self.r:
			self.dead = True
			effects.append(Explosion(self.pos,0.2,50,self.player))


class Effect:
	def __init__(self,pos,time):
		self.pos = pos
		self.time = time

	def tick(self,dt):
		self.time -= dt

		
class Explosion(Effect):
	def __init__(self,pos,time,r, player):
		self.r = r
		super().__init__(pos,time)
		if pos.distance_to(player.pos) < r + player.r: 
			player.damage(25)

	def draw(self,screen):
		pygame.draw.circle(screen, "orange", self.pos, self.r)


class Laser(Effect):
	def __init__(self, pos, time, player, start_pos):
		self.start_pos = start_pos
		super().__init__(pos, time)
		if self.start_pos == 0 or self.start_pos == 1:
			if player.pos.x - player.r < self.pos.x < player.pos.x + player.r:
				player.damage(50)
		else:
			if player.pos.y - player.r < self.pos.y < player.pos.y + player.r:
				player.damage(50)

	def draw(self,screen):
		match self.start_pos:
			case 0:
				pygame.draw.line(screen, "red", self.pos, pygame.Vector2(self.pos.x, scrHeight), width=3)
			case 1:
				pygame.draw.line(screen, "red", self.pos, pygame.Vector2(self.pos.x, 0), width=3)
			case 2:
				pygame.draw.line(screen, "red", self.pos, pygame.Vector2(scrWidth, self.pos.y), width=3)
			case 3:
				pygame.draw.line(screen, "red", self.pos, pygame.Vector2(0, self.pos.y), width=3)


class Turret:
	def __init__(self, player):
		self.size = 25
		self.player = player
		self.start_pos = random.randint(0,3)
		self.pos = [pygame.Vector2(scrWidth/2,self.size/2),pygame.Vector2(scrWidth/2,scrHeight-self.size/2),pygame.Vector2(self.size/2,scrHeight/2),pygame.Vector2(scrWidth-self.size/2,scrHeight/2)][self.start_pos]
		self.pos_old = self.pos
		self.target_pos = self.pos
		self.cooldown_time = 7
		self.cooldown = self.cooldown_time 

		self.new_target_pos()

	def shoot(self):
		v = (self.player.pos - self.pos).normalize() * 100
		bullets.append(Bullet(self.pos.copy(), 5, v, pygame.Vector2(0,0), -0.9, 10, self.player))

	def tick(self,dt):
		self.cooldown -= dt
		self.cooldown = max(self.cooldown, 0)
		self.move()

	def draw(self,screen):
		pygame.draw.rect(screen, "darkorchid4", pygame.Rect(self.pos.x-self.size/2,self.pos.y-self.size/2,self.size,self.size))

	def move(self):
		if self.cooldown == 0:
			self.shoot()
			self.new_target_pos()
		self.pos = self.target_pos * (self.cooldown_time - self.cooldown) / self.cooldown_time + self.pos_old * self.cooldown / self.cooldown_time
	
	def new_target_pos(self):
		self.pos_old = self.pos
		self.cooldown = self.cooldown_time
		if self.start_pos == 0 or self.start_pos == 1:
			self.target_pos = pygame.Vector2(random.randint(self.size//2,scrWidth-self.size//2),self.pos.y)
		else:
			self.target_pos = pygame.Vector2(self.pos.x,random.randint(self.size//2,scrHeight-self.size//2))

class LaserTurret(Turret):
	def __init__(self, player):
		super().__init__(player)

	def shoot(self):
		effects.append(Laser(self.pos, 0.2, self.player, self.start_pos))
	
	def draw(self, screen):
		pygame.draw.rect(screen, "brown", pygame.Rect(self.pos.x-self.size/2,self.pos.y-self.size/2,self.size,self.size))

class HealthBar:
	def __init__(self, healthMax):
		self.healthMax = healthMax
		self.width = 150
		self.height = 25
		self.bg = pygame.Rect(scrWidth - self.width - 10, 10, self.width, self.height)
		self.healthR = pygame.Rect(scrWidth - self.width - 10, 10, self.width, self.height)
		self.damageR = pygame.Rect(scrWidth - self.width - 10, 10, self.width, self.height)

	def update(self, health):
		self.healthR.width = health / self.healthMax * self.width
		self.healthR.left = scrWidth -  self.healthR.width/2 - 10 - self.width/2
		self.damageR.width = self.damageR.width * 0.8 + self.healthR.width * 0.2
		self.damageR.left = scrWidth -  self.damageR.width/2 - 10 - self.width/2

	def draw(self, screen):
		pygame.draw.rect(screen, "gray21", self.bg)
		pygame.draw.rect(screen, "firebrick3", self.damageR)
		pygame.draw.rect(screen, "green2", self.healthR)


scrWidth = 750
scrHeight = 750


def run(screen):
	pygame.init()
	menuWidth = screen.get_width()
	menuHeight = screen.get_height()
	screen = pygame.display.set_mode((scrWidth, scrHeight))

	global bullets
	global effects
	bullets = []
	effects = []

	dt = 0
	clock = pygame.time.Clock()
	
	player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),25,pygame.Vector2(0,0),pygame.Vector2(0,0),-0.2)
	turrets = [LaserTurret(player) for i in range(2)] + [ Turret(player) for i in range(2)]
	
	bar = HealthBar(100) 

	running = True


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

		#player
		player.physics(dt)
		if player.health <= 0:
			running = False

		#entities
		for i, bullet in enumerate(bullets):
			bullet.tick(dt)
			bullet.check_player_colision(player)
			if bullet.dead:
				bullets.pop(i)
				continue

			d = (bullet.pos - player.pos).length()
			bullet.a = max((500 - d),0)/500 * player.a
			bullet.physics(dt)
		#health bar
		bar.update(player.health)

		#turrets
		for turret in turrets:
			turret.tick(dt)

		#render
		screen.fill("darkslategray4")
		player.draw(screen)
		for turret in turrets:
			turret.draw(screen)
		for bullet in bullets:
			bullet.draw(screen)
		for i, explosion in enumerate(effects):
			explosion.tick(dt)
			explosion.draw(screen)
			if explosion.time < 0:
				effects.pop(i)
		bar.draw(screen)

		pygame.display.flip()

		dt = clock.tick(60)/1000  # limits FPS to 60

	screen = pygame.display.set_mode((menuWidth, menuHeight))


