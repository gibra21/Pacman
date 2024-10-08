import pygame 
import sys
import random 
import math 

pygame.init()

# Colors 
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
RED = (255,0,0)
PINK = (255,192,203)
CYAN = (0,255,255)
ORANGE = (255,165,0)

# screen dimension 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
CELL_SIZE = 40

# Grid dimensions
GRID_WIDTH = 15
GRID_HEIGHT = 15

# game states
PLAYING = 0
GAME_OVER = 1

# global game state
game_state = PLAYING 

# creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

font = pygame.font.Font(None, 36)

# Game grid
grid = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    
]

pacman = {
    'x' : 1, # pacman current position
    'y' : 1, # 
    'direction': 3, # 0 right, 1: down, 2: left, 3: up
    'mouth_open': False # boolean for mouth of pacman 
} 

ghost = [
    {'x':1, 'y':13, 'color': RED},
    {'x':1, 'y':13, 'color': PINK},
    {'x':1, 'y':13, 'color': CYAN},
    {'x':1, 'y':13, 'color': ORANGE}
]

# score
score = 0


# create the game loop
clock = pygame.time.Clock()
running = True

# Movement Delays
pacman_move_delay = 150 #miliseconds
ghost_move_delay = 300
mouth_anim_delay = 300
# timing variables
last_pacman_move_time = 0
last_ghost_move_time = 0
last_mouth_anim_time = 0

# will handle the movement logic of pacman 
def move_pacman():
    global score
    # uses list of tuples, and it defines the movement in 4 possible directions
    dx, dy = [(1,0), (0,1), (-1, 0), (0, -1)][pacman['direction']]
    # will calulate new position of the pacman
    new_x,new_y = pacman['x'] + dx, pacman['y'] + dy
    # we now have a grid with newx and newy, checks if positon doesnt equal a wall (1), 
    if grid[new_y][new_x] != 1:
        # if the position is valid,we update the new position
        pacman['x'], pacman['y'] = new_x, new_y
        # checks if the grid is 0, so the pacman can move into the space, and it will allow the pacman to eat the pellet
        if grid[new_y][new_x] == 0:
            grid[new_y][new_x] = 2 # Mark as eaten 
            # increasing the score by 10 when the pacman eats a pelet
            score+=10


def move_ghost(ghost):
    directions = [(1,0), (0,1), (-1, 0), (0, -1)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = ghost['x'] + dx, ghost['y'] + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and grid[new_y][new_x] != 1:
            ghost['x'], ghost['y'] = new_x, new_y
            break 

def draw_pacman():
    x = pacman['x'] * CELL_SIZE + CELL_SIZE // 2
    y = pacman['y'] * CELL_SIZE + CELL_SIZE // 2 + 50

    mouth_opening = 45 if pacman['mouth_open'] else 0

    # drawing the pacman 
    pygame.draw.circle(screen, YELLOW, (x,y), CELL_SIZE // 2)

    # getting the angles for the mouth based on direction of pacman
    if pacman['direction'] == 0: # Right
        start_angle = 360 - mouth_opening
        end_angle = mouth_opening / 3
    elif pacman['direction'] == 3:
        start_angle = 90 - mouth_opening / 2
        end_angle = 90 + mouth_opening / 2
    elif pacman['direction'] == 2:
        start_angle = 180 - mouth_opening / 2
        end_angle = 180 + mouth_opening / 2
    else:
        start_angle = 270 - mouth_opening / 2
        end_angle = 270 + mouth_opening / 2

    # Draw the mouth using a pie shape
    pygame.draw.arc(screen, BLACK, 
                    (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE), 
                    math.radians(start_angle), math.radians(end_angle), CELL_SIZE // 2)
    
    # drawing a line from the center to create the slice effects
    mouth_line_end_x = x + math.cos(math.radians(start_angle)) * CELL_SIZE // 2
    mouth_line_end_y = y - math.cos(math.radians(start_angle)) * CELL_SIZE // 2
    pygame.draw.line(screen, BLACK, (x,y), (mouth_line_end_x, mouth_line_end_y), 2)

def draw_ghost(ghost):
    x = ghost['x'] * CELL_SIZE + CELL_SIZE // 2
    y = ghost['y'] * CELL_SIZE + CELL_SIZE // 2 + 50
    pygame.draw.circle(screen, ghost['color'], (x,y), CELL_SIZE // 2)


def reset_game():
    global pacman, ghost, score, grid, game_state
    pacman = {
    'x' : 1, # pacman current position
    'y' : 1, # 
    'direction': 3, # 0 right, 1: down, 2: left, 3: up
    'mouth_open': False # boolean for mouth of pacman 
} 

ghost = [
    {'x':1, 'y':13, 'color': RED},
    {'x':1, 'y':13, 'color': PINK},
    {'x':1, 'y':13, 'color': CYAN},
    {'x':1, 'y':13, 'color': ORANGE}
]

score = 0
grid = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    
]

game_state = PLAYING

def draw_game_over():
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 48)
    restart_text = pygame.font.Font(None, 36)

    game_over_text = game_over_font.render("GAME OVER", True, RED)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    restart_text = restart_text.render("Press SPACE to restart", True, YELLOW)


    screen.blit(game_over_text, (SCREEN_WIDTH // 2 // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))


# Main game loop 
running = True
clock = pygame.time.Clock()

while running:
    current_timr = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                if event.key == pygame.K_UP:
                    pacman['direction'] = 3
                elif event.key == pygame.K_DOWN:
                    pacman['direction'] = 1
                elif event.key == pygame.K_LEFT:
                    pacman['direction'] = 2
                elif event.key == pygame.K_RIGHT:
                    pacman['direction'] = 0
            elif game_state == GAME_OVER:
                if event.ley == pygame.K_SPACE:
                    reset_game()

    if game_state == PLAYING:
        # moving pacman only if there has bee enough time passed
        if current_timr - last_pacman_move_time > pacman_move_delay:
            for ghosts in ghost:
                move_ghost(ghosts)
            last_ghost_move_time = current_timr
        # Getting the pacman mouth animation 
        if current_timr - last_mouth_anim_time > mouth_anim_delay:
            pacman['mouth_open'] = not pacman['mouth_open']
            last_mouth_anim_time = current_timr

        #clearing the screen 
        screen.fill(BLACK)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x*CELL_SIZE, y*CELL_SIZE+50, CELL_SIZE, CELL_SIZE))
                elif grid[y][x] == 0:
                    pygame.draw.circle(screen, YELLOW, (x*CELL_SIZE+CELL_SIZE // 2, y*CELL_SIZE+CELL_SIZE//2+50), 3)
        
        # drawing the pacman
        draw_pacman()

        # drawing the ghost
        for ghosts in ghost:
            draw_ghost(ghosts)
        
        # displaying the score
        score_text = font.render(f"score: {score}", True, WHITE)
        screen.blit(score_text, (10,10))

        # checking for collision
        for ghosts in ghost:
            if pacman['x'] == ghosts['x'] and pacman['y'] == ghosts['y']:
                game_state = GAME_OVER
    elif game_state == GAME_OVER:
        draw_game_over()
    
    # update the display
    pygame.display.flip()


    #cap frame rate
    clock.tick(60)


pygame.quit()

sys.exit()
