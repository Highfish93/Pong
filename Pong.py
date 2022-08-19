import pygame
from PygameUtils import Button

pygame.init()

FPS = 60
WIDTH, HEIGHT = 700, 500
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
SCORE_FONT = pygame.font.SysFont('comicsans', 50)
BALL_RADIUS = 7
WINNING_SCORE = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.display.set_caption('Pong')


class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f'{left_score}', True, WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}', True, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))
        ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / reduction_factor
                ball.y_vel = y_vel * -1
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / reduction_factor
                ball.y_vel = y_vel * -1


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def mainMenu(win):
    global runMainMenu
    win.fill(BLACK)
    middle_x = WIDTH // 2 - BUTTON_WIDTH // 2
    middle_y = HEIGHT // 2 - BUTTON_HEIGHT
    twoPlayerBtn = Button(win, middle_x, middle_y, BUTTON_WIDTH, BUTTON_HEIGHT, text='2 Player Game')
    twoPlayerBtn.color = (0, 255, 0)
    twoPlayerBtn.hoverColor = (0, 200, 0)
    twoPlayerBtn.onClick = main
    while runMainMenu:
        twoPlayerBtn.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runMainMenu = False
                break
    pygame.quit()


def main():
    global runMainMenu
    runMainMenu = False
    run = True
    clock = pygame.time.Clock()
    paddle_left = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_right = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    score_left = 0
    score_right = 0
    while run:
        clock.tick(FPS)
        draw(WIN, [paddle_left, paddle_right], ball, score_left, score_right)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, paddle_left, paddle_right)
        ball.move()
        handle_collision(ball, paddle_left, paddle_right)
        if ball.x < 0:
            score_right += 1
            paddle_left.reset()
            paddle_right.reset()
            ball.reset()
        elif ball.x > WIDTH:
            score_left += 1
            paddle_left.reset()
            paddle_right.reset()
            ball.reset()
        won = False
        win_text = ""
        if score_left == WINNING_SCORE:
            won = True
            win_text = 'Left Player Won!'
        elif score_right == WINNING_SCORE:
            won = True
            win_text = 'Right Player Won!'
        if won:
            text = SCORE_FONT.render(win_text, True, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.time.delay(5000)
            paddle_left.reset()
            paddle_right.reset()
            ball.reset()
            score_left, score_right = 0, 0
    print('The end is near')
    pygame.quit()


if __name__ == '__main__':
    runMainMenu = True
    mainMenu(WIN)
    pygame.quit()
