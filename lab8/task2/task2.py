import pygame
import sys
import random

pygame.init()

#класс для создание змеи
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def head_inside(self):
        return 0<=self.x<=count_blocks-1 and 0<=self.y<=count_blocks-1
    def __eq__ (self, other):
        return isinstance (other, SnakeBlock) and self.x == other.x and self.y == other.y

#создание блока
def draw_block(color, row, column):
    pygame.draw.rect(screen,color,[block_size+column*block_size + margin*(column+1), header_margin + block_size +row*block_size + margin*(row+1), block_size, block_size])

#создание рандомной ягоды
def random_block():
    x = random.randint(0, count_blocks - 1)
    y = random.randint(0, count_blocks - 1)
    empty_block = SnakeBlock(x,y)
    while empty_block in snake_list:
        empty_block.x = random.randint(0, count_blocks - 1)
        empty_block.y = random.randint(0, count_blocks - 1)
    return empty_block


block_size = 40
header_margin = 70
margin = 1
count_blocks = 10
size = [block_size*count_blocks + 2*block_size + margin*count_blocks, block_size*count_blocks + 2*block_size + margin*count_blocks + header_margin]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("SnakeGame")

icon = pygame.image.load("lab8/task2/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

snake_list = [SnakeBlock(1,2), SnakeBlock(1,3)]

d_row = buf_row = 0
d_col = buf_col = 1

apples = [random_block() for _ in range(1)]  # Start with 1 apple

body = 2
speed = 1

font = pygame.font.SysFont('Times New Roman', 36)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col != 0:
                buf_row = -1
                buf_col = 0
            elif event.key == pygame.K_DOWN and d_col != 0:
                buf_row = 1
                buf_col = 0
            elif event.key == pygame.K_LEFT and d_row != 0:
                buf_row = 0
                buf_col = -1
            elif event.key == pygame.K_RIGHT and d_row != 0:
                buf_row = 0
                buf_col = 1

    screen.fill((104, 33, 133))#bg color
    pygame.draw.rect(screen, (169, 13, 191), [0,0,size[0], header_margin])

    score = font.render(f"Score: {body}", 0, (255,255,255))
    speed_text = font.render(f"Speed: {speed}", 0, (255,255,255))

    screen.blit(score, (block_size,block_size))
    screen.blit(speed_text, (block_size + 200,block_size))


    #drawing board    
    for r in range(count_blocks):
        for c in range(count_blocks):
            if (r + c)%2 == 0:
                color_block = (45,236,229)
            else:
                color_block = (26,140,238)
            
            draw_block(color_block, r, c)

    head = snake_list[-1]
    if not head.head_inside():
        run = False
        pygame.quit()
        sys.exit()

    for apple in apples:
        draw_block((255,0,0), apple.x, apple.y)
    #creating long snake
    for index, snake in enumerate(snake_list):
        if index == len(snake_list) - 1:  # Check if it is the head of the snake
            draw_block((0, 200, 0), snake.x, snake.y)  # A darker green for the head
        else:
            draw_block((0, 255, 0), snake.x, snake.y)  # Original green for the body

    pygame.display.flip()
    
    # Draw all apples
    for apple in apples:
        draw_block((255,0,0), apple.x, apple.y)

# Check for collisions with any apple
    for apple in apples[:]:  # Make a copy of the list to iterate over
        if apple == head:
            body += 1
            snake_list.append(apple)
            speed = body // 5 + 1
            apples.remove(apple)  # Remove the eaten apple
            apples.append(random_block())  # Add a new apple to replace the eaten one
            if body % 8 == 0:
                apples.append(random_block())  # Add an additional apple every 8 points

    d_row = buf_row
    d_col = buf_col
    new = SnakeBlock(head.x + d_row, head.y + d_col)

    if new in snake_list:
        pygame.quit()
        sys.exit()

    snake_list.append(new)
    snake_list.pop(0)

    clock.tick(2 + speed)