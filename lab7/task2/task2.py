import pygame
import os

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

button_size = 60
play_button = pygame.transform.scale(pygame.image.load(os.path.normpath('lab7/task2/images/play.png')), (button_size, button_size))
pause_button = pygame.transform.scale(pygame.image.load(os.path.normpath('lab7/task2/images/pause.png')), (button_size, button_size))

current_song_index = 0
songs = ['lab7/task2/music/2024.mp3', 'lab7/task2/music/evilj0rdan.mp3', 'lab7/task2/music/h00dbyair.mp3']
pygame.mixer.music.load(os.path.normpath(songs[current_song_index]))
pygame.mixer.music.play()

covers = ['lab7/task2/images/2024.jpg', 'lab7/task2/images/carti.jpg', 'lab7/task2/images/iammusic.jpg']
album_cover_size = 275
album_cover = pygame.transform.scale(pygame.image.load(os.path.normpath(covers[current_song_index])), (album_cover_size, album_cover_size))

play = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        play = not play
        if play:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
    
    if pressed[pygame.K_LEFT]: 
        current_song_index = (current_song_index - 1) % len(songs)
        pygame.mixer.music.load(songs[current_song_index])
        pygame.mixer.music.play()
        play = True
        x = 0
        album_cover = pygame.transform.scale(pygame.image.load(covers[current_song_index]), (album_cover_size, album_cover_size))
            
    if pressed[pygame.K_RIGHT]: 
        current_song_index = (current_song_index + 1) % len(songs)
        pygame.mixer.music.load(songs[current_song_index])
        pygame.mixer.music.play()
        play = True
        album_cover = pygame.transform.scale(pygame.image.load(covers[current_song_index]), (album_cover_size, album_cover_size))
        

    screen.fill((255, 255, 255))    
    
    screen.blit(album_cover, (270, 65))
   
    if play:
        screen.blit(pause_button, (380, 365))
    else:
        screen.blit(play_button, (380, 365))
    
    pygame.display.update()
    clock.tick(10)

pygame.quit()