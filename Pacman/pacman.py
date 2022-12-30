import pygame

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SPEED = 0.2
RAY = 30
pygame.init()

window = pygame.display.set_mode((640, 480), 0)
x = 10
y = 10
x_speed = SPEED
y_speed = SPEED

while True:
    # Calculate the rules
    x = x + x_speed
    y = y + y_speed

    if x + RAY > 640:
        x_speed = -SPEED
    if x - RAY < 0:
        x_speed = SPEED
    if y + RAY > 480:
        y_speed = -SPEED
    if y - RAY < 0:
        y_speed = SPEED

    # Paint
    window.fill(BLACK)
    pygame.draw.circle(window, YELLOW, (int(x), int(y)), RAY, 0)
    pygame.display.update()

    # Events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
