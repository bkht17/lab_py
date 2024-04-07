import pygame
import sys
import random

pygame.init()

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def head_inside(self):
        return 0 <= self.x <= count_blocks - 1 and 0 <= self.y <= count_blocks - 1

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

class Food:
    def __init__(self, x, y, weight, time_to_live):
        self.x = x
        self.y = y
        self.weight = weight
        self.time_to_live = time_to_live

def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [block_size + column * block_size + margin * (column + 1),
                                     header_margin + block_size + row * block_size + margin * (row + 1),
                                     block_size, block_size])

def random_food():
    x = random.randint(0, count_blocks - 1)
    y = random.randint(0, count_blocks - 1)
    weight = random.randint(1, 3)
    time_to_live = random.randint(20, 40)
    new_food = Food(x, y, weight, time_to_live)
    while SnakeBlock(new_food.x, new_food.y) in snake_list:
        new_food.x = random.randint(0, count_blocks - 1)
        new_food.y = random.randint(0, count_blocks - 1)
    return new_food

def draw_food(food):
    # Define colors for different weights
    colors = {
        1: (255, 0, 0),  # Red for weight 1
        2: (255, 100, 0),  # Green for weight 2
        3: (255, 0, 100)   # Blue for weight 3
    }
    color = colors.get(food.weight, (255, 255, 255))  # Default to white if weight not in colors
    draw_block(color, food.x, food.y)


block_size = 40
header_margin = 70
margin = 1
count_blocks = 10
size = [block_size * count_blocks + 2 * block_size + margin * count_blocks,
        block_size * count_blocks + 2 * block_size + margin * count_blocks + header_margin]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("SnakeGame")

icon = pygame.image.load("lab8/task2/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

snake_list = [SnakeBlock(1, 2), SnakeBlock(1, 3)]
d_row = buf_row = 0
d_col = buf_col = 1
apples = [random_food() for _ in range(1)]
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

    screen.fill((104, 33, 133))  # bg color
    pygame.draw.rect(screen, (169, 13, 191), [0, 0, size[0], header_margin])

    score = font.render(f"Score: {body}", True, (255, 255, 255))
    speed_text = font.render(f"Speed: {speed}", True, (255, 255, 255))

    screen.blit(score, (block_size, block_size))
    screen.blit(speed_text, (block_size + 200, block_size))

    for r in range(count_blocks):
        for c in range(count_blocks):
            color_block = (45, 236, 229) if (r + c) % 2 == 0 else (26, 140, 238)
            draw_block(color_block, r, c)

    head = snake_list[-1]
    if not head.head_inside():
        run = False
        pygame.quit()
        sys.exit()
        

    # Draw and update food
    # Inside the game loop, after processing events

    # Update and draw food
    # Inside the main game loop, replace the food drawing logic
    for food in apples[:]:  # Loop through a copy of the list
        food.time_to_live -= 1
        if food.time_to_live <= 0:
            apples.remove(food)
            apples.append(random_food())  # Replace the disappeared food
        else:
            draw_food(food)  # Draw food using the new function that colors based on weight


    # Check for collisions with any apple
    for food in apples[:]:  # Make a copy of the list to iterate over
        if food.x == head.x and food.y == head.y:
            body += food.weight  # Increase body size by the weight of the food
            speed = body // 5 + 1  # Update speed based on the new body length
            apples.remove(food)  # Remove the eaten food
            apples.append(random_food())  # Add new food to keep the food count consistent

            if body % 5 == 0:  # Optionally, add an extra food item every 5 points to increase difficulty
                apples.append(random_food())

    # Move snake
    # Inside the main game loop, after updating the snake's position

    # Move snake
    d_row, d_col = buf_row, buf_col
    new_head = SnakeBlock(head.x + d_row, head.y + d_col)

    # Check if the new head position collides with the snake's body
    if any(block.__eq__(new_head) for block in snake_list[:-1]):  # Exclude the tail from the check
        run = False
        pygame.quit()
        sys.exit()

    # Add the new head to the snake
    snake_list.append(new_head)
    if len(snake_list) > body:
        snake_list.pop(0)

    # Draw snake
    for snake in snake_list:
        draw_block((0, 200, 0) if snake == new_head else (0, 255, 0), snake.x, snake.y)

    pygame.display.flip()
    clock.tick(2 + speed)