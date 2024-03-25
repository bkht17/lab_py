import pygame
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode((800, 800))

bg_img = pygame.image.load("lab7/task1/mainclock.png")
min_img = pygame.image.load("lab7/task1/rightarm.png")
sec_img = pygame.image.load("lab7/task1/leftarm.png")

rect = bg_img.get_rect(center=(400, 400))

running = True
while running:
    screen.fill((255, 255, 255))
    bg_x = (screen.get_width() - bg_img.get_width()) / 2
    bg_y = (screen.get_height() - bg_img.get_height()) / 2
    screen.blit(bg_img, (bg_x, bg_y))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False

    time = datetime.now().time()
    sec_ang = -(time.second * 6)
    new_sec_img = pygame.transform.rotate(sec_img, sec_ang)
    sec_rect = new_sec_img.get_rect(center=rect.center)
    screen.blit(new_sec_img, sec_rect.topleft)

    min_ang = -(time.minute * 6)
    new_min_img = pygame.transform.rotate(min_img, min_ang)
    min_rect = new_min_img.get_rect(center=rect.center)
    screen.blit(new_min_img, min_rect.topleft)

    pygame.display.flip()
