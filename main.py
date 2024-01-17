import pygame, sys, random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(8, 10), Vector2(9, 10)]  # starting snake
        self.direction = Vector2(-1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.sound = pygame.mixer.Sound("Sound/crunch.wav")

    def draw_snake(self):
        self.update_head()
        self.update_tail()
        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)

            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)

            else:
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif(previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)
                    elif(previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif(previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)

    def update_head(self):
        diff = self.body[1] - self.body[0]
        if diff == Vector2(1, 0):
            self.head = self.head_left
        elif diff == Vector2(-1, 0):
            self.head = self.head_right
        elif diff == Vector2(0, 1):
            self.head = self.head_up
        elif diff == Vector2(0, -1):
            self.head = self.head_down

    def update_tail(self):
        diff = self.body[-2] - self.body[-1]
        if diff == Vector2(1, 0):
            self.tail = self.tail_left
        elif diff == Vector2(-1, 0):
            self.tail = self.tail_right
        elif diff == Vector2(0, 1):
            self.tail = self.tail_up
        elif diff == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block is True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_num-1)
        self.y = random.randint(0, cell_num-1)
        self.pos = Vector2(self.x, self.y)

    def randomise(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        screen.blit(apple, fruit_rect)

        # create coordinates to place fruit
        # draw square


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.munch()
        self.fail_test()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def munch(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise()
            self.snake.add_block()
            self.snake.play_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()

    def fail_test(self):
        if not (0 <= self.snake.body[0].x <= cell_num) or not (0 <= self.snake.body[0].y <= cell_num):
            self.game_over()
        for i in self.snake.body[1:]:
            if self.snake.body[0] == i:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_colour = (167, 209, 61)
        for row in range(cell_num):
            if row % 2 == 0:
                for col in range(cell_num):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)

            elif row % 2 == 1:
                for col in range(cell_num):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size*cell_num - 60)
        score_y = int(cell_size*cell_num - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,apple_rect.width+score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)



pygame.init()
cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_num*cell_size, cell_num*cell_size))
clock = pygame.time.Clock()
test_surface = pygame.Surface((100, 200))
test_surface.fill((0, 0, 255))

apple = pygame.image.load("Graphics/apple.png").convert_alpha()

game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    screen.fill((175, 215, 70))
    main_game.draw_elements()  # draw all elements
    pygame.display.update()
    clock.tick(60)
