import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

x = 400
y = 300
vx = 0
vy = 0
ball_radius = 25

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vx = -20
            elif event.key == pygame.K_RIGHT:
                vx = 20
            elif event.key == pygame.K_UP:
                vy = -20
            elif event.key == pygame.K_DOWN:
                vy = 20
        elif event.type == pygame.KEYUP:
            vx = 0
            vy = 0

    x += vx
    y += vy
    
    if x - ball_radius < 0 or x + ball_radius > 800:
        vx = 0
    if y - ball_radius < 0 or y + ball_radius > 600:
        vy = 0
    
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), ball_radius)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()