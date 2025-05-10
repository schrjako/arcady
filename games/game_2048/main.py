import pygame
import random

pygame.init()

# variables
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.SysFont("comicsans", 40)
CHOICES = [2, 4, 8]

# Will be set by run
screen: pygame.Surface

# colors
BACKGROUND_COLOR = (187, 173, 160)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048") # title


# grid dispay
def draw_grid(grid, score):
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE), border_radius = 10)
            pygame.draw.rect(screen, (150, 140, 130), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), width = 2, border_radius = 10)
            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(col*TILE_SIZE + TILE_SIZE//2, row*TILE_SIZE + TILE_SIZE//2))
                screen.blit(text, text_rect)
                
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, HEIGHT - 40))
    
    pygame.display.update()
                
 
def add_new(grid, score):
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if grid[row][col] == 0:
            break
        
    value = 2
    grid[row][col] = value
    draw_grid(grid, score)
 
                
def  if_win(grid):
    # check if win
    c = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            if value != 0:
                c+=1
                
            if value == 2048:
                return "end_win"
            
    if c == GRID_SIZE*GRID_SIZE:
        return "game_over"



def move_left(grid):
    score_gain = 0
    moved = False
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                current_col = col
                while current_col > 0 and grid[row][current_col-1] == 0:
                    grid[row][current_col-1] = grid[row][current_col]
                    grid[row][current_col] = 0
                    current_col -=1
                    moved = True

    # merge if nessesery
        for col in range(1, GRID_SIZE):
            if grid[row][col-1] == grid[row][col] and grid[row][col-1] != 0:
                grid[row][col-1] *= 2
                score_gain += grid[row][col-1]
                grid[row][col] = 0
                moved = True
    
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                current_col = col
                while current_col > 0 and grid[row][current_col-1] == 0:
                    grid[row][current_col-1] = grid[row][current_col]
                    grid[row][current_col] = 0
                    current_col -=1
    
    return moved, score_gain


def move_right(grid):
    score_gain = 0
    moved = False
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE-2, -1, -1):
            if grid[row][col] != 0:
                current_col = col
                while current_col < GRID_SIZE -1 and grid[row][current_col+1] == 0:
                    grid[row][current_col+1] = grid[row][current_col]
                    grid[row][current_col] = 0
                    current_col +=1
                    moved = True

    # merge if nessesery
        for col in range(1, GRID_SIZE):
            if grid[row][col-1] == grid[row][col] and grid[row][col-1] != 0:
                grid[row][col-1] *= 2
                score_gain += grid[row][col-1]
                grid[row][col] = 0
                moved = True
    
        
        for col in range(GRID_SIZE-2, -1, -1):
            if grid[row][col] != 0:
                current_col = col
                while current_col < GRID_SIZE -1 and grid[row][current_col+1] == 0:
                    grid[row][current_col+1] = grid[row][current_col]
                    grid[row][current_col] = 0
                    current_col +=1
                    
    
    return moved, score_gain


def move_up(grid):
    score_gain = 0
    moved = False
    for col in range(GRID_SIZE):
        for row in range(1, GRID_SIZE):
            if grid[row][col] != 0:
                current_row = row
                while current_row > 0 and grid[current_row-1][col] == 0:
                    grid[current_row-1][col] = grid[current_row][col]
                    grid[current_row][col] = 0
                    current_row -=1
                    moved = True

    # merge if nessesery
        for row in range(1, GRID_SIZE):
            if grid[row][col] == grid[row-1][col] and grid[row][col] != 0:
                grid[row-1][col] *= 2
                score_gain += grid[row][col]
                grid[row][col] = 0
                moved = True
    
        for row in range(1, GRID_SIZE):
            if grid[row][col] != 0:
                current_row = row
                while current_row > 0 and grid[current_row-1][col] == 0:
                    grid[current_row-1][col] = grid[current_row][col]
                    grid[current_row][col] = 0
                    current_row -=1

    return moved, score_gain


def move_down(grid):
    score_gain = 0
    moved = False
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE-2, -1, -1):
            if grid[row][col] != 0:
                current_row = row
                while current_row < GRID_SIZE-1 and grid[current_row+1][col] == 0:
                    grid[current_row+1][col] = grid[current_row][col]
                    grid[current_row][col] = 0
                    current_row +=1
                    moved = True

    # merge if nessesery
        for row in range(GRID_SIZE-2, -1, -1):
            if grid[row][col] == grid[row+1][col] and grid[row][col] != 0:
                grid[row+1][col] *= 2
                score_gain += grid[row][col]
                grid[row][col] = 0
                moved = True
    
        for row in range(GRID_SIZE-2, -1, -1):
            if grid[row][col] != 0:
                current_row = row
                while current_row < GRID_SIZE-1 and grid[current_row+1][col] == 0:
                    grid[current_row+1][col] = grid[current_row][col]
                    grid[current_row][col] = 0
                    current_row +=1
                    
    return moved, score_gain


def show_center_message(message, color=(255, 255, 255)):
    text = FONT.render(message, True, color)
    text_r = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_r)
    
    pygame.display.update()
    pygame.time.wait(3000)
    


def main():
    score = 0
    grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    # setup
    positions = random.sample([(r, c) for r in range(4) for c in range(4)], 2)

    for pos in positions:
        row, col = pos
        value = random.choice(CHOICES)
        grid[row][col] = value
        
    draw_grid(grid, score)    
        
        
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    moved, score_gain = move_left(grid)
                if event.key == pygame.K_RIGHT:
                    moved, score_gain = move_right(grid)
                if event.key == pygame.K_UP:
                    moved, score_gain = move_up(grid)
                if event.key == pygame.K_DOWN:
                    moved, score_gain = move_down(grid)
                    
                
                if moved:
                    score += score_gain
                    draw_grid(grid, score)
                    add_new(grid, score)
                    
        if if_win(grid) == "end_win":
            draw_grid(grid, score)
            show_center_message("You Win!", (255, 215, 0))
            running = False
            
        if if_win(grid) == "game_over":
            draw_grid(grid, score)
            show_center_message("Game Over!", (255, 0, 0)) # red
            running = False

            
        pygame.time.delay(100)
        
        
def run(screen_in: pygame.Surface):
	global screen

	# Save old data
	old_dimensions = screen_in.get_size()
	old_title = pygame.display.get_caption()

	# Resize screen and set new caption
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("2048")

	# Run the game
	main()

	# Set the screen back to the starting stage
	screen_in = pygame.display.set_mode(old_dimensions)
	pygame.display.set_caption(*old_title)


# If ran directly (not through menu), this will trigger
if __name__ == "__main__":
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("2048")  # title

	main()  # main function

	pygame.quit()
    