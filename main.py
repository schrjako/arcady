import pygame
from menu.menu import show_menu

import games.snake.main as snake
import games.spacepunk.main as spacepunk
import games.KnifeHit.main as knifehit
import games.game_2048.main as game_2048


def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Arcady")

	running = True
	while running:
		choice = show_menu(screen, ["snake", "spacepunk", "knifehit", "2048 game"])
		if choice == "snake":
			snake.run(screen)
		elif choice == "spacepunk":
			spacepunk.run(screen)
		elif choice == "knifehit":
			knifehit.run(screen)
		elif choice == "2048 game":
			game_2048.run(screen)
		elif choice == "quit":
			running = False

	pygame.quit()


if __name__ == "__main__":
	main()
