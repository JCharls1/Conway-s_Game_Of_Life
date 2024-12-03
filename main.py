import pygame
import random

CELL_SIZE = 10  
FPS = 10  

ALIVE_COLOR = (0, 255, 0)
DEAD_COLOR = (0, 0, 0)
GRID_COLOR = (50, 50, 50)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 200, 255)
TEXT_COLOR = (255, 255, 255)

TITLE_COLOR = (255, 255, 255)
TITLE_FONT_SIZE = 48
BUTTON_TEXT_FONT_SIZE = 32
BUTTON_ROUND_RADIUS = 10
SHADOW_OFFSET = 5
SHADOW_COLOR = (20, 20, 20)
GRADIENT_START_COLOR = (50, 50, 100)
GRADIENT_END_COLOR = (10, 10, 40)

def draw_gradient_background(screen, color1, color2):
    width, height = screen.get_size()
    for i in range(height):
        r = color1[0] + (color2[0] - color1[0]) * i // height
        g = color1[1] + (color2[1] - color1[1]) * i // height
        b = color1[2] + (color2[2] - color1[2]) * i // height
        pygame.draw.line(screen, (r, g, b), (0, i), (width, i))


def create_initial_grid(rows, cols):
    return [[random.randint(0, 7) == 0 for _ in range(cols)] for _ in range(rows)]

def create_empty_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def get_live_neighbors(row, col, rows, cols, grid):
    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                life_sum += grid[(row + i) % rows][(col + j) % cols]
    return life_sum

def create_next_grid(rows, cols, grid):
    return [
        [
            1 if (live_neighbors := get_live_neighbors(row, col, rows, cols, grid)) == 3 or 
                 (grid[row][col] == 1 and live_neighbors == 2)
            else 0
            for col in range(cols)
        ]
        for row in range(rows)
    ]

def draw_grid(screen, grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            color = ALIVE_COLOR if grid[row][col] else DEAD_COLOR
            pygame.draw.rect(
                screen,
                color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )

def toggle_cell(grid, x, y):
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    grid[row][col] = 1 - grid[row][col]

def main1():
    rows, cols = 50, 50
    pygame.init()
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Random Grid")
    clock = pygame.time.Clock()

    grid = create_initial_grid(rows, cols)
    running = True

    while running:
        screen.fill(DEAD_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    grid = create_initial_grid(rows, cols)  

        draw_grid(screen, grid, rows, cols)
        pygame.display.flip()
        grid = create_next_grid(rows, cols, grid)
        clock.tick(FPS)

    pygame.quit()

def main2():
    rows, cols = 50, 50
    pygame.init()
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Grid")
    clock = pygame.time.Clock()

    grid = create_empty_grid(rows, cols)
    running = True
    editing = True  

    while running:
        screen.fill(DEAD_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if editing and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    toggle_cell(grid, *event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    editing = not editing  

        draw_grid(screen, grid, rows, cols)
        pygame.display.flip()

        if not editing:
            grid = create_next_grid(rows, cols, grid)
            clock.tick(FPS)

    pygame.quit()

def menu():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Menu")
    
    font_title = pygame.font.Font(None, TITLE_FONT_SIZE)
    font_button = pygame.font.Font(None, BUTTON_TEXT_FONT_SIZE)

    button1_rect = pygame.Rect(100, 120, 200, 50)
    button2_rect = pygame.Rect(100, 200, 200, 50)

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_gradient_background(screen, GRADIENT_START_COLOR, GRADIENT_END_COLOR)

        title_text = font_title.render("Conway's Game of Life", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(200, 60))
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(screen, SHADOW_COLOR, button1_rect.move(SHADOW_OFFSET, SHADOW_OFFSET), border_radius=BUTTON_ROUND_RADIUS)
        pygame.draw.rect(screen, SHADOW_COLOR, button2_rect.move(SHADOW_OFFSET, SHADOW_OFFSET), border_radius=BUTTON_ROUND_RADIUS)

        button1_color = BUTTON_HOVER_COLOR if button1_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        button2_color = BUTTON_HOVER_COLOR if button2_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button1_color, button1_rect, border_radius=BUTTON_ROUND_RADIUS)
        pygame.draw.rect(screen, button2_color, button2_rect, border_radius=BUTTON_ROUND_RADIUS)

        text1 = font_button.render("Random Grid", True, TEXT_COLOR)
        text2 = font_button.render("Editable Grid", True, TEXT_COLOR)
        screen.blit(text1, text1.get_rect(center=button1_rect.center))
        screen.blit(text2, text2.get_rect(center=button2_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(mouse_pos):
                    print("Press 'R' to restart the grid")
                    main1()
                if button2_rect.collidepoint(mouse_pos):
                    print("Left CLick to Draw/Remove a Pixel")
                    print("Space to Run the Simulation")
                    main2()

if __name__ == "__main__":
    menu()
