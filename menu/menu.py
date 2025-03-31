import pygame as pg

def draw_text(screen: pg.Surface, text: str, pos: tuple[int, int], font: pg.font.Font, selected: bool) -> None:
	colour = (255, 0, 0) if selected else (255, 255, 255)
	rendered = font.render(text, True, colour)
	screen.blit(rendered, pos)

def show_menu(screen: pg.Surface, options: list[str]) -> str:
	font = pg.font.SysFont(None, 48)

	clock = pg.time.Clock()
	options = options + ["quit"]
	selected = 0

	while True:
		screen.fill((0, 0, 0))

		for i, option in enumerate(options):
			draw_text(screen, option, (300, 200 + (i - selected) * 60), font, i == selected)

		pg.display.flip()
		clock.tick(30)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				return "quit"
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					selected = (selected - 1) % len(options)
				elif event.key == pg.K_DOWN:
					selected = (selected + 1) % len(options)
				elif event.key == pg.K_RETURN:
					return options[selected].lower()