import pygame, sys, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 800
WINDOWHEIGHT = 800
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Collision Detection')

# Set up the colors.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the player and food data structures.
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20
player = pygame.Rect(375, 375, 10, 10)
foods = [pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE) for _ in range(20)]

# Set up movement variables.
moveLeft = moveRight = moveUp = moveDown = False
MOVESPEED = 4

stopRight = False
stopLeft = False
stopUp = False
stopDown = False

score = 0

# Set up walls
walls = [
    # Outer walls
    pygame.Rect(50, 50, 700, 10),
    pygame.Rect(50, 740, 600, 10),
    pygame.Rect(50, 50, 10, 700),
    pygame.Rect(740, 50, 10, 700),

    # Inner walls
    pygame.Rect(100, 100, 200, 10),
    pygame.Rect(400, 100, 300, 10),
    pygame.Rect(100, 100, 10, 200),
    pygame.Rect(100, 400, 10, 300),
    pygame.Rect(100, 690, 600, 10),
    pygame.Rect(690, 100, 10, 300),
    pygame.Rect(690, 400, 10, 300),

    pygame.Rect(200, 200, 300, 10),
    pygame.Rect(200, 200, 10, 300),
    pygame.Rect(200, 600, 10, 100),
    pygame.Rect(500, 200, 10, 300),

    pygame.Rect(300, 300, 100, 10),
    pygame.Rect(300, 300, 10, 100),
    pygame.Rect(300, 490, 200, 10),
    pygame.Rect(490, 300, 10, 200),

    pygame.Rect(400, 400, 100, 10),
    pygame.Rect(400, 400, 10, 100),
    pygame.Rect(400, 590, 200, 10),
    pygame.Rect(590, 400, 10, 200)
]

font = pygame.font.SysFont(None, 36)

def draw_text(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_message():
    draw_text('Você encostou na borda!', font, windowSurface, 250, 350, RED)

# Run the game loop.
while True:
    # Check for events.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Change the keyboard variables.
            if event.key in (K_LEFT, K_a) and not stopLeft:
                moveRight = False
                moveLeft = True
            if event.key in (K_RIGHT, K_d) and not stopRight:
                moveLeft = False
                moveRight = True
            if event.key in (K_UP, K_w) and not stopUp:
                moveDown = False
                moveUp = True
            if event.key in (K_DOWN, K_s) and not stopDown:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key in (K_LEFT, K_a):
                moveLeft = False
            if event.key in (K_RIGHT, K_d):
                moveRight = False
            if event.key in (K_UP, K_w):
                moveUp = False
            if event.key in (K_DOWN, K_s):
                moveDown = False
            if event.key == K_x:
                player.topleft = (random.randint(0, WINDOWWIDTH - player.width), random.randint(0, WINDOWHEIGHT - player.height))

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    foodCounter += 1
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

    # Draw the white background onto the surface.w
    windowSurface.fill(WHITE)

    # Move the player.
    if moveDown:
        player.top += MOVESPEED
    if moveUp:
        player.top -= MOVESPEED
    if moveLeft:
        player.left -= MOVESPEED
    if moveRight:
        player.right += MOVESPEED

    # Wrap around logic
    if player.left < 6 or player.right > WINDOWWIDTH or player.top < 6 or player.bottom > WINDOWHEIGHT:
        draw_message()
        print("Você encostou na borda!")

    # Wrap around logic for player
    if player.left < 3:
        player.right = WINDOWWIDTH - 15
    if player.right > WINDOWWIDTH:
        player.left = 10
    if player.top < 3:
        player.bottom = WINDOWHEIGHT - 15
    if player.bottom > WINDOWHEIGHT:
        player.top = 10

    pygame.draw.rect(windowSurface, BLACK, player)

    for wall in walls:
        pygame.draw.rect(windowSurface, BLACK, wall)
        if player.colliderect(wall):
            if moveDown and player.bottom > wall.top:
                player.top -= MOVESPEED
            if moveUp and player.top < wall.bottom:
                player.bottom += MOVESPEED
            if moveLeft and player.left < wall.right:
                player.right += MOVESPEED
            if moveRight and player.right > wall.left:
                player.left -= MOVESPEED

    # Check whether the player has intersected with any food squares.
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            if (player.width < 50 ):
                player.width += 2
                player.height += 2
            player.center = (player.centerx, player.centery)
            score += 1
            print(f"Score: {score}")

    # Draw the food.
    for food in foods:
        pygame.draw.rect(windowSurface, GREEN, food)

    # Draw the score on the screen
    draw_text(f'Score: {score}', font, windowSurface, 10, 10, BLACK)

    # Draw the window onto the screen.
    pygame.display.update()
    mainClock.tick(60)