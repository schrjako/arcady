import pygame
from .player import player
import random
from enum import Enum
path = "./games/subwaysurfers"


class subwaysurfersGame:
	"""
	The main game class handling initialization, game loop, and rendering for the game.
	"""

	class States(Enum):
		NORMAL = 0
		GAME_OVER = 1

	def __init__(
		self,
		screen: pygame.Surface,
		board_radius: int,
		cell_size: float,
	) -> None:
		"""
		Initializes the game by creating the hex board.
		"""
		self.screen: pygame.Surface = screen
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.backgound: tuple[int, int, int] = (26, 27, 38)

		offset: tuple[int, int] = (
			self.screen.get_width() // 2,
			self.screen.get_height() // 2,
		)

		self.player: player = player()

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


				if self.state == self.States.GAME_OVER:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.running = False

			if self.state == self.States.NORMAL:
				# Move player
				self.player.update()

			# Draw everything
			self.screen.fill(self.backgound)

			self.player.draw(self.screen)

			if self.state == self.States.GAME_OVER:
				self.draw_game_over(self.game_over_msg)

			pygame.display.flip()
			self.clock.tick(60)
			frame += 1


def run(screen: pygame.Surface):
	subwaysurfersGame(screen, board_radius=10, cell_size=17).run()


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	run(screen)
