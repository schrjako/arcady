import pygame
from .player import Player
from .obstacles import Obstacle
import random
from enum import Enum
path = "./games/subwaysurfers"


class subwaysurfersGame:
	"""
	The main game class handling initialization, game loop, and rendering for the game.
	
	   .+------+     +------+     +------+     +------+     +------+.
	 .' |    .'|    /|     /|     |      |     |\     |\    |`.    | `.
	+---+--+'  |   +-+----+ |     +------+     | +----+-+   |  `+--+---+
  z |   |  |   |   | |    | |     |      |     | |    | |   |   |  |   |
  ^ | y,+--+---+   | +----+-+     +------+     +-+----+ |   +---+--+   |
  | |.'    | .'    |/     |/      |      |      \|     \|    `. |   `. |
	+------+'      +------+       +------+       +------+      `+------+
	 -> x
	"""

	class States(Enum):
		NORMAL = 0
		GAME_OVER = 1

	def __init__(
		self,
		screen: pygame.Surface,
		board_radius: int) -> None:
		
		self.screen: pygame.Surface = screen
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.background: tuple[int, int, int] = (26, 27, 38)

		offset: tuple[int, int] = (
			self.screen.get_width() // 2,
			self.screen.get_height() // 2,
		)

		self.player: player = Player(350, 400, 100, 100, 1, 1, self.screen)
		self.obstacle: obstacle = Obstacle(0.004, 0.7, 1, 200, 100, self.screen)

		self.running: bool = True
		self.state: playerGame.States = self.States.NORMAL
		self.game_over_msg = ""

	def initiate_game_over(self, message: str) -> None:
		self.state = self.States.GAME_OVER
		self.game_over_msg = message

	def run(self) -> None:
		"""
		Runs the main game loop, handling events and drawing the board.
		"""
		frame = 0

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				#print(event)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_a:
						self.obstacle.y+=0.01
						self.obstacle.y2+=0.01
					if event.key == pygame.K_d:
						self.obstacle.y-=0.01
						self.obstacle.y2-=0.01
					if event.key == pygame.K_RIGHT:
						self.player.vright =15
					if event.key == pygame.K_LEFT:
						self.player.vleft =15
					if self.player.jumps < 2:
						if event.key == pygame.K_UP:
							self.player.vy =28
							self.player.jumps +=1
						'''if event.key == pygame.K_DOWN:
							self.player.y +=30'''


				if self.state == self.States.GAME_OVER:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.running = False

			self.player.jump()
			self.player.move()
			self.obstacle.move()

			if self.state == self.States.NORMAL:
				self.player.update()
				self.obstacle.update()

			# Draw everything
			self.screen.fill(self.background)

			self.player.draw(self.screen)
			self.obstacle.draw(self.screen)

			if self.state == self.States.GAME_OVER:
				self.draw_game_over(self.game_over_msg)

			pygame.display.flip()
			self.clock.tick(60)
			frame += 1


def run(screen: pygame.Surface):
	subwaysurfersGame(screen, board_radius=10).run()


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	run(screen)
