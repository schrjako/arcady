import pygame
from menu.menu import show_menu
from scores.scores import Scores

import games.snake.main as snake
import games.spacepunk.main as spacepunk
import games.breakout.main as breakout
import games.KnifeHit.main as knifehit
import games.game_2048.main as game_2048


def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Arcady")

	scores = Scores()

	running = True
	while running:
		choice = show_menu(screen, ["snake", "spacepunk", "knifehit", "2048 game", "breakout"])
		scores.set_game(choice)

		if choice == "snake":
			snake.run(screen, scores)
		elif choice == "spacepunk":
			spacepunk.run(screen, scores)
		elif choice == "breakout":
			breakout.run(screen, scores)
		elif choice == "knifehit":
			knifehit.run(screen, scores)
		elif choice == "2048 game":
			game_2048.run(screen, scores)
		elif choice == "quit":
			running = False

	pygame.quit()


if __name__ == "__main__":
	main()
