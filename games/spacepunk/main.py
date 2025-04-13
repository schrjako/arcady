import pygame
class Entity:
	def __init__(self,pos,r,v,a):
		self.pos = pos
		self.r = r
		self.v = v
		self.a = a
	def draw(self,screen):
		pygame.draw.circle(screen, "red", self.pos, self.r)
	def physics(self,dt):
		self.v += self.a * dt
		self.pos += self.v * dt
		if self.pos.x < space_ship_pos.x + self.r:
			self.pos.x = space_ship_pos.x + self.r 
			self.v.x *= -0.25
		if self.pos.x > space_ship_size.x + space_ship_pos.x -self.r:
			self.pos.x = space_ship_size.x + space_ship_pos.x -self.r 
			self.v.x *= -0.25
		if self.pos.y < space_ship_pos.y + self.r:
			self.pos.y = space_ship_pos.y + self.r 
			self.v.y *= -0.25
		if self.pos.y > space_ship_size.y + space_ship_pos.x -self.r:
			self.pos.y = space_ship_size.y + space_ship_pos.x -self.r 
			self.v.y *= -0.25

def run(screen):
	# pygame setup
	pygame.init()
	running = True
	dt = 0
	clock = pygame.time.Clock()
	
	pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
	r = 40
	a = pygame.Vector2(0,0)
	v = pygame.Vector2(0,0)
	global space_ship_pos
	global space_ship_size
	space_ship_pos = pygame.Vector2(30, 30)
	space_ship_size = pygame.Vector2(screen.get_width()-60, screen.get_height()-60)
	space_ship = pygame.Rect(space_ship_pos.x, space_ship_pos.y,space_ship_size.x, space_ship_size.y) 

	while running:
		#events
		for event in pygame.event.get():
			 if event.type == pygame.QUIT:
				 running = False
		#inputs
		keys = pygame.key.get_pressed()
		if keys[pygame.K_s]:a = pygame.Vector2(0,98)
		if keys[pygame.K_w]:a = pygame.Vector2(0,-98)
		if keys[pygame.K_d]:a = pygame.Vector2(98,0)
		if keys[pygame.K_a]:a = pygame.Vector2(-98,0)
		#physics
		v += a * dt
		pos += v * dt
		if pos.x < space_ship_pos.x + r:
			pos.x = space_ship_pos.x + r 
			v.x *= -0.25
		if pos.x > space_ship_size.x + space_ship_pos.x -r:
			pos.x = space_ship_size.x + space_ship_pos.x -r 
			v.x *= -0.25
		if pos.y < space_ship_pos.y + r:
			pos.y = space_ship_pos.y + r 
			v.y *= -0.25
		if pos.y > space_ship_size.y + space_ship_pos.x -r:
			pos.y = space_ship_size.y + space_ship_pos.x -r 
			v.y *= -0.25

		#render
		screen.fill("green")
		pygame.draw.rect(screen, "blue", space_ship)
		pygame.draw.circle(screen, "red", pos, r)

		pygame.display.flip()

		dt = clock.tick(60)/1000  # limits FPS to 60



