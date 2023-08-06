# Breakout16
# Ron Ferentini
# 08/03/2023

import pygame
from pygame.locals import *
import random

# brick types
NORMAL = 0
INVINCIBLE = 1
COUNTDOWN = 2
FALLING = 3


# all the classes
class Brick:
    """ This class defines a brick
        the attributes for the brick are as follows
        rect - rectangle
        color = color of the brick
        points - how many points the brick in worth
    """

    # constructor make the object
    def __init__(self, rect, color, points, kind=NORMAL):
        self.rect = rect
        self.color = color
        self.points = points
        self.kind = kind
        self.countdown = 0
        self.ShowText = False
        self.falling = False
        if self.kind == COUNTDOWN:
            self.ShowText = True
            self.countdown = 5
            self.BrickText = TextBox(self.rect[0] + 12, self.rect[1] + 3, 25,
                                     pygame.Color("black"), self.color)
        if self.kind == FALLING:
            self.ShowText = True
            self.BrickText = TextBox(self.rect[0] + 4, self.rect[1] + 3, 25,
                                     pygame.Color("black"), self.color)

    @property
    def __str__(self):
        return f"Brick: {self.rect} {self.color} {self.points}"

    def draw(self, s):
        temp = pygame.draw.rect(s, self.color, self.rect)
        if self.kind == COUNTDOWN:
            self.BrickText.draw(s, f"{self.countdown}")
        if self.kind == FALLING:
            self.BrickText.y = self.rect[1] + 3
            self.BrickText.draw(s, f"{self.points}")
        return temp


class TextBox:
    def __init__(self, x, y, size,
                 color=pygame.Color("white"),
                 bg_color=pygame.Color("black")):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)
        self.color = color
        self.bg_color = bg_color

    def draw(self, s, text):
        text_bitmap = self.font.render(text, True, self.color, self.bg_color)
        s.blit(text_bitmap, (self.x, self.y))


# functions
def make_bricks(rows: object, cols: object) -> object:
    my_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    my_bricks = []
    brick_width = 35
    brick_height = 20
    brick_spacing = 5
    brick_initial_shift = 20

    for r in range(rows):
        for c in range(cols):
            brick_rect = (c * (brick_width + brick_spacing) + brick_initial_shift,
                          r * (brick_height + brick_spacing) + brick_initial_shift,
                          brick_width, brick_height)
            rnd = random.randint(1, 100)
            if rnd >= 95:
                new_brick = Brick(brick_rect, pygame.Color("gray"), 0, INVINCIBLE)
            elif rnd >= 90:
                new_brick = Brick(brick_rect, my_colors[r], 50, COUNTDOWN)
            elif rnd >= 85:
                new_brick = Brick(brick_rect, pygame.Color("hotpink"), 100, FALLING)
            else:
                new_brick = Brick(brick_rect, my_colors[r], (rows - r) * 10)
            my_bricks.append(new_brick)
    return my_bricks


def no_more_bricks(bricks):
    if len(bricks) == 0:
        return True
    else:
        for b in bricks:
            if b.kind != INVINCIBLE:
                return False
        return True


# initialize pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60

# defining the screen
ScreenHeight = 600
ScreenWidth = 800
pygame.display.set_caption("Breakout")
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

# defining the paddle
PaddleX = 400
PaddleY = 530
PaddleW: int = 80
PaddleH: int = 20
PaddleDX = 0
PaddleCounter = 0
PaddleLocation = (PaddleX, PaddleY, PaddleW, PaddleH)

# defining the ball
BallRadius: int = 6
BallX: int = PaddleX + PaddleW // 2
BallY: int = PaddleY - 10
BallLocation: tuple[int, int] = (BallX, BallY)
dx = 0
dy = 0

# making the breaks
bricks = []
#make_bricks(6, 19)

# initial drawing commands
# draw the ball
BallRect = pygame.draw.circle(screen, pygame.Color("White"), BallLocation, BallRadius)
# draw the paddle
PaddleRect = pygame.draw.rect(screen, pygame.Color("blue"), PaddleLocation)

score = 0
txtScore = TextBox(20, 560, 30)
balls = 5
txtBallCount = TextBox(700, 560, 30)
txtMessage = TextBox(300, 560, 30, pygame.Color("black"), pygame.Color("white"))

FirstGame = True
NewGame = True
NewBall = False
GameRunning = True
while GameRunning:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                GameRunning = False
            if event.key == K_RIGHT:
                PaddleDX = 7
            if event.key == K_LEFT:
                PaddleDX = -7
            if event.key == K_n and NewGame:
                dx = random.choice([6, -6])
                dy = -6
                score = 0
                balls = 5
                bricks = make_bricks(6, 19)
                PaddleW = 80
                NewGame = False
                if FirstGame:
                    FirstGame = False
            if event.key == K_SPACE and NewBall:
                dx = 6
                dy = -6
                PaddleW = 80
                NewBall = False
        if event.type == pygame.KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                PaddleDX = 0

    # check for ball / brick interaction
    for b in bricks:
        if pygame.Rect.colliderect(BallRect, b.rect):
            dy *= -1
            if b.kind == NORMAL:
                score += b.points
                bricks.remove(b)
            elif b.kind == COUNTDOWN:
                score += b.points
                b.countdown -= 1
                if b.countdown == 0:
                    bricks.remove(b)
            elif b.kind == FALLING:
                b.falling = True
            else:
                # must be an invisible brick
                pass

            if no_more_bricks(bricks):
                NewBall = True
                dx = 0
                dy = 0
                BallX = PaddleX + PaddleW // 2
                BallY = PaddleY - 10
                bricks = make_bricks(6, 19)
            break

    # check if the ball hits the top, bottom, left side or right side of the window
    # then change the direction
    # right side of the screen
    if BallX > ScreenWidth - BallRadius:
        dx *= -1
        BallX = ScreenWidth - BallRadius
    # left side of the screen
    if BallX < BallRadius:
        dx *= -1
        BallX = BallRadius
    # top of the screen
    if BallY < BallRadius:
        dy *= -1
    # ball hit the bottom of the screen so the player loses a ball
    # reset the ball over the paddle
    if BallY > ScreenHeight - BallRadius:
        balls -= 1
        dx = 0
        dy = 0
        BallX = PaddleX + PaddleW // 2
        BallY = PaddleY - 10
        if balls == 0:
            NewGame = True
        else:
            NewBall = True

    # check if the ball collides with the Paddle
    dx_list = [-7, -5, -3, 3, 5, 7]
    temp_width = PaddleRect.w // 6
    for i in range(6):
        temp_rect = PaddleRect.copy()
        temp_rect.w = temp_width
        temp_rect.x = temp_rect.x + temp_width * i
        if pygame.Rect.colliderect(BallRect, temp_rect):
            dy *= -1
            dx = dx_list[i]
            break

    # brick / paddle interaction
    for b in bricks:
        if b.kind == FALLING and b.falling:
            if pygame.Rect.colliderect(PaddleRect, b.rect):
                score += b.points
                PaddleW *= 2
                PaddleCounter = 300
                bricks.remove(b)
            else:
                b.rect = (b.rect[0], b.rect[1] + 5, b.rect[2], b.rect[3])
                if b.rect[1] > ScreenHeight:
                    bricks.remove(b)

    # move the ball
    if NewBall or NewGame:
        BallX = PaddleX + PaddleW // 2
        BallY = PaddleY - 10
    else:
        BallX += dx
        BallY += dy
    BallLocation = (BallX, BallY)

    # update the paddle position
    PaddleX += PaddleDX
    PaddleCounter -= 1
    if PaddleCounter < 0:
        PaddleW = 80
    # check if the paddle goes off the screen and stop it
    if PaddleX > ScreenWidth - PaddleW:
        PaddleX = ScreenWidth - PaddleW
    if PaddleX < 0:
        PaddleX = 0
    PaddleLocation = (PaddleX, PaddleY, PaddleW, PaddleH)

    # drawing commands
    screen.fill(pygame.Color("black"))
    # draw the ball
    BallRect = pygame.draw.circle(screen, pygame.Color("White"), BallLocation, BallRadius)
    # draw the paddle
    PaddleRect = pygame.draw.rect(screen, pygame.Color("blue"), PaddleLocation)

    txtScore.draw(screen, f"Score: {score}")
    txtBallCount.draw(screen, f"Balls: {balls}")
    if NewGame:
        txtMessage.draw(screen, f"Press N for new game")
    if NewBall:
        txtMessage.draw(screen, f"Press SPACEBAR for new ball")

    if balls == 0:
        new_game = True
        txtMessage.draw(screen, f"Press N for new game")
        dx = 0
        dy = 0
        BallX = 400
        BallY = 300

    # draw the bricks
    for b in bricks:
        # pygame.draw.rect(screen, b.color, b.rect)
        b.draw(screen)

    pygame.display.update()
    clock.tick(fps)  # for every second at most 60 frames (loops) can pass
    # print(clock.get_fps())

# out of the while loop
print("Game Over")
pygame.quit()
