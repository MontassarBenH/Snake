import pygame
import random
import pickle

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 100, 0)
brown = (139, 69, 19)
gray = (128, 128, 128)

snake_block = 20
snake_speed = 15

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)

def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1: 
            pygame.draw.rect(window, green, [x[0], x[1], snake_block, snake_block])
            pygame.draw.rect(window, dark_green, [x[0], x[1], snake_block, snake_block], 2)
            
            # Eyes
            eye_radius = 3
            left_eye = (x[0] + 5, x[1] + 5)
            right_eye = (x[0] + snake_block - 5, x[1] + 5)
            pygame.draw.circle(window, white, left_eye, eye_radius)
            pygame.draw.circle(window, white, right_eye, eye_radius)
        else:
            pygame.draw.rect(window, green, [x[0], x[1], snake_block, snake_block])
            pygame.draw.rect(window, dark_green, [x[0], x[1], snake_block, snake_block], 1)

def draw_apple(x, y, size):
    pygame.draw.circle(window, red, (x + size//2, y + size//2), size//2)
    pygame.draw.rect(window, brown, [x + size//2 - 2, y, 4, 6])
    leaf_points = [(x + size//2, y), (x + size//2 + 6, y - 6), (x + size//2 + 12, y)]
    pygame.draw.polygon(window, green, leaf_points)

def message(msg, color, y_displace=0):
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(width/2, height/2 + y_displace))
    window.blit(mesg, text_rect)

def get_user_name():
    user_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode
        
        window.fill(black)
        message("New Best Score! Enter your name:", white, -50)
        name_surface = font.render(user_name, True, white)
        name_rect = name_surface.get_rect(center=(width/2, height/2))
        window.blit(name_surface, name_rect)
        pygame.display.update()
    
    return user_name

def load_best_score():
    try:
        with open("best_score.pkl", "rb") as f:
            return pickle.load(f)
    except:
        return (0, "N/A")

def save_best_score(score, name):
    with open("best_score.pkl", "wb") as f:
        pickle.dump((score, name), f)

def gameLoop():

    global snake_speed

    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    score = 0
    level = 1

    best_score, best_player = load_best_score()

    while not game_over:

        while game_close:
            window.fill(black)
            message("You Lost! Press Y-Play Again or N-Quit", white, -50)
            message(f"Your Score: {score}", white, 0)
            message(f"Best Score: {best_score} by {best_player}", white, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_y:
                        return gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        window.fill(black)
        pygame.draw.rect(window, gray, [0, 0, width, height], 2)  
        draw_apple(foodx, foody, snake_block)
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)

        score_text = font.render(f"Score: {score}", True, white)
        window.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {level}", True, white)
        window.blit(level_text, (width - 100, 10))

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            score += 10

            if score % 50 == 0:
                level += 1
                snake_speed += 2

        clock.tick(snake_speed)

    if score > best_score:
        best_player = get_user_name()
        save_best_score(score, best_player)

    pygame.quit()
    quit()

gameLoop()
