import pygame
from menu.menu import show_menu
import games.snake.main as snake
import games.spacepunk.main as spacepunk
import games.breakout.main as breakout


def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Arcady")

	running = True
	while running:
		choice = show_menu(screen, ["snake", "spacepunk", "breakout"])
		if choice == "snake":
			snake.run(screen)
		elif choice == "spacepunk":
			spacepunk.run(screen)
		elif choice == "breakout":
			breakout.run(screen)
		elif choice == "quit":
			running = False

	pygame.quit()


if __name__ == "__main__":
	main()
