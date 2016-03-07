import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice



class PygameBrickBreakerView(object):
    """visualizes a brick breaker game in a pygame window"""
    def __init__(self, model, screen):
        """Initialize the view with the specified model"""
        self.model = model
        self.screen = screen
    def draw(self):
        """Draw the game state to the screen"""
        #draw the bricks
        self.screen.fill(pygame.Color('black'))
        for brick in self.model.bricks:
            r = pygame.Rect(brick.left, brick.top, brick.width, brick.height)
            pygame.draw.rect(self.screen, pygame.Color(brick.color), r)
        #draw the paddle
        paddle_rect = self.model.paddle_rect
        pygame.draw.rect(self.screen, pygame.Color('white'), paddle_rect)
        pygame.display.update()


class Brick(object):
    """represents a brick in our brick breaker game"""
    def __init__(self, left, top, width, height):
        self.left = left
        self.top  = top
        self.width = width
        self.height = height
        self.color = choice(["red", "green", "orange", "blue", "purple"])

class Paddle(object):
    """represents the paddle"""
    def __init__(self, left, top, width, height):
        self.left = left
        self.top  = top
        self.width = width
        self.height = height


class BrickBreakerModel(object):
    """stores came state for brick breaker game"""
    def __init__(self):
        self.bricks = []
        self.MARGIN = 5
        self.BRICK_WIDTH = 40
        self.BRICK_HEIGHT = 20
        for left in range(self.MARGIN, 
                            640 - self.BRICK_WIDTH - self.MARGIN, self.BRICK_WIDTH + self.MARGIN):
            for top in range(self.MARGIN,
                            480/2, self.BRICK_HEIGHT + self.MARGIN):
                brick = Brick(left, top, self.BRICK_WIDTH, self.BRICK_HEIGHT)
                self.bricks.append(brick)

        self.paddle = Paddle(640/2, 480 - 30, 50, 20)
        self.paddle_rect = pygame.Rect(self.paddle.left, 
                        self.paddle.top, 
                        self.paddle.width, 
                        self.paddle.height)

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle_rect.left -= 10
        if event.key == pygame.K_RIGHT:
            self.model.paddle_rect.left += 10

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    model = BrickBreakerModel()
    view = PygameBrickBreakerView(model, screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
        time.sleep(.001)