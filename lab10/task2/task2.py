# importing needed modules
import pygame, sys, random, time
import psycopg2
from pygame.math import Vector2
from configparser import ConfigParser


def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


config = load_config()
conn = psycopg2.connect(**config)
cur = conn.cursor()

# Creating table
cur.execute(
    """CREATE TABLE IF NOT EXISTS SnakeGame(
    user_name VARCHAR(255),
    score INTEGER,
    level INTEGER
);
"""
)


def insert_snakegame(user_name, score, level):
    """Insert a new entry into the snakegame table"""
    sql = """INSERT INTO SnakeGame(user_name, score, level)
             VALUES(%s, %s, %s);"""

    try:
        # execute the INSERT statement
        cur.execute(sql, (user_name, score, level))

        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_data():
    """Retrieve data from the snakegame table"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_name, score, level FROM SnakeGame ORDER BY score"
                )
                rows = cur.fetchall()

                print("The number of users: ", cur.rowcount)
                for row in rows:
                    print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


username = input("Your username:")


# announcing class fruit
class Fruit:
    # initialization
    def __init__(self):
        self.randomize()

    # method for drawing apple
    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size,
            cell_size,
        )
        screen.blit(sized_apple, fruit_rect)

    # randomly placing apple
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# announcing banana class
class Banana:  # same with fruit
    def __init__(self):
        self.randomize()

    def draw_banana(self):
        banana_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size,
            cell_size,
        )
        screen.blit(sized_banana, banana_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# announcing peach class
class Peach:  # same with fruit
    def __init__(self):
        self.randomize()

    def draw_peach(self):
        peach_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size,
            cell_size,
        )
        screen.blit(sized_peach, peach_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# announcing snake class
class Snake:
    # initialization
    def __init__(self):
        self.body = [
            Vector2(5, 10),
            Vector2(4, 10),
            Vector2(3, 10),
        ]  # first three blocks
        self.direction = Vector2(1, 0)  # direction
        self.new_block = False

    # for drawing snake
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (51, 51, 255), block_rect)

    # method for moving snake
    def move_snake(self):
        if self.new_block == True:  # if we need new block
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:  # stays same, just moves around
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    # method for adding block in the back
    def add_block(self):
        self.new_block = True


# main game
class Main:
    def __init__(self):
        self.user_name = username
        self.snake = Snake()  # add snake
        self.fruit = Fruit()  # add fruit
        self.banana = Banana()  # Add Banana instance
        self.peach = Peach()  # Add Peach instance
        self.fruits_eaten = 0  # number of eaten fruits
        self.score = 0
        self.timer_interval = 150  # speed of the game
        self.level = 1  # level of the game
        self.fruit_disappear_time = (
            pygame.time.get_ticks()
        )  # Initialize fruit disappear time
        self.fruit_disappear_interval = (
            6000  # Set the interval for fruit disappearance (in milliseconds)
        )

    def update(self):
        self.snake.move_snake()  # moving snake
        self.check_collision()  # check collision with apple, banana, peach
        self.check_fail()  # check if snake exits the screen
        self.manage_fruit_disappearance()  # disappearance and appearance of fruits

    def manage_fruit_disappearance(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fruit_disappear_time >= self.fruit_disappear_interval:
            self.fruit.randomize()  # placing apple
            self.banana.randomize()  # placing banana
            self.peach.randomize()  # Randomize the position of the peach
            self.fruit_disappear_time = (
                current_time  # Update the last disappearance time
            )

    def draw_elements(self):
        self.draw_grass()  # drawing grass, playing ground
        self.fruit.draw_fruit()  # drawing apple
        self.banana.draw_banana()  # Draw Banana
        self.peach.draw_peach()  # Draw Peach
        self.snake.draw_snake()  # draw snake
        self.draw_score()  # draw scores on the screen
        self.draw_level()  # drawing level on the screen

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()  # adding block to snake
            self.fruits_eaten += 1  # fruits eaten
            self.score += 1
            if (
                self.fruits_eaten // 6 > 0
                and self.fruits_eaten != 0
                and self.timer_interval >= 45
            ):
                self.decrease_timer_interval()
                self.level += 1  # making game faster
                self.fruits_eaten = self.fruits_eaten % 6
        # Collision with Banana
        if self.banana.pos == self.snake.body[0]:
            self.banana.randomize()
            self.snake.add_block()  # adding block to snake
            self.fruits_eaten += 2  # fruits eaten
            self.score += 2
            if (
                self.fruits_eaten // 6 > 0
                and self.fruits_eaten != 0
                and self.timer_interval >= 45
            ):
                self.decrease_timer_interval()
                self.level += 1  # making game faster
                self.fruits_eaten = self.fruits_eaten % 6
        # Collision with Peach
        if self.peach.pos == self.snake.body[0]:
            self.peach.randomize()
            self.snake.add_block()  # adding block to snake
            self.fruits_eaten += 4  # fruits eaten
            self.score += 4
            if (
                self.fruits_eaten // 6 > 0
                and self.fruits_eaten != 0
                and self.timer_interval >= 45
            ):
                self.decrease_timer_interval()
                self.level += 1  # making game faster
                self.fruits_eaten = self.fruits_eaten % 6

    def decrease_timer_interval(self):
        self.timer_interval -= 15
        pygame.time.set_timer(
            SCREEN_UPDATE, self.timer_interval
        )  # increasing speed of game

    def check_fail(self):  # if sanke exits the screen
        if (
            not 0 <= self.snake.body[0].x < cell_number
            or not 0 <= self.snake.body[0].y < cell_number
        ):
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        time.sleep(1.2)
        insert_snakegame(self.user_name, self.score, self.level)
        get_data()
        pygame.quit()
        sys.exit()

    def pause_game(self):
        print("Game Paused")
        insert_snakegame(self.user_name, self.score, self.level)
        print(f"Current score: {self.score}, Current level: {self.level}")

    def draw_grass(self):  # drawing grass
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(
                            column * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for column in range(cell_number):
                    if column % 2 == 1:
                        grass_rect = pygame.Rect(
                            column * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):  # drawing score on screen
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = sized_apple.get_rect(
            midright=(score_rect.left, score_rect.centery)
        )
        screen.blit(score_surface, score_rect)
        screen.blit(sized_apple, apple_rect)

    def draw_level(self):  # drawing level on screen
        level_text = "Level: " + str(self.level)
        level_surface = game_font.render(level_text, True, (56, 74, 12))
        level_x = int(cell_size * cell_number - 60)
        level_y = int(cell_size * cell_number - 640)
        level_rect = level_surface.get_rect(center=(level_x, level_y))
        screen.blit(level_surface, level_rect)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size)
)  # getting screen size
pygame.display.set_caption("Snake Game")
fps = pygame.time.Clock()  # frames per second
apple = pygame.image.load(
    "images/snake_apple.png"
).convert_alpha()  # getting apple image
sized_apple = pygame.transform.scale(
    apple, (40, 40)
)  # resizing it to the size of the cell
banana = pygame.image.load("images/banana.png").convert_alpha()  # getting apple image
sized_banana = pygame.transform.scale(
    banana, (40, 40)
)  # resizing it to the size of the cell
peach = pygame.image.load("images/peach.png").convert_alpha()  # getting apple image
sized_peach = pygame.transform.scale(
    peach, (40, 40)
)  # resizing it to the size of the cell

# getting size of the game font
game_font = pygame.font.Font(None, 40)
# getting the interval in which the game will be updated
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
# main game object
main_game = Main()

running = True
while running:
    for event in pygame.event.get():
        # for ending the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()  # updating the screen
        if event.type == pygame.KEYDOWN:
            # changing the direction of snake
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_p:
                main_game.game_pause()
    # color of screen
    screen.fill((175, 215, 70))
    # drawing game elements onto the screen
    main_game.draw_elements()

    pygame.display.update()
    fps.tick(120)

# Retrieve data from the Phonebook table