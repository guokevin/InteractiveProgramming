import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice

class PygameEscapeTheMazeView(object):
    """creates a escape the maze game in the pygame window"""
    def __init__(self, model, screen):
        """Initialize the view with the specified model"""
        self.model = model
        self.screen = screen

    def draw(self):
        """Draw the game state to the screen"""
        #draw the maze
        self.screen.fill(pygame.Color('grey'))
        for wall_segment in self.model.maze_segments:
            r = pygame.Rect(wall_segment.x_pos, 
                            wall_segment.y_pos, 
                            wall_segment.width, 
                            wall_segment.height)
            pygame.draw.rect(self.screen, pygame.Color(wall_segment.color), r)
        #draw the maze character
        r = self.model.character.rect
        pygame.draw.rect(self.screen, pygame.Color(self.model.character.color), r)
        pygame.display.update()

class Character(object):
    """represents the character"""
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = "red"
        self.vel = 5            #how many pixels it updates
        self.refresh_rate = 3   #how many loops before it updates the velocity

"""class Maze(object):
    #creates the matrix for the maze
    def __init__(self, maze_matrix):
        self.maze_matrix = maze_matrix"""

class GenerateMaze(object):
    def __init__(self):
        self.maze_matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                            [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1], 
                            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1], 
                            [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1], 
                            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1], 
                            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1], 
                            [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1], 
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
                            [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1], 
                            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1], 
                            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.row_length = len(self.maze_matrix)
        self.column_length = len(self.maze_matrix[0][:])

class CreateMazeSegment(object):
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = "black"
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

class EscapeTheMazeModel(object):
    def __init__(self):
        # Initialize Character location
        self.character = Character(640/2 + 20, 450, 20, 20)

        # Definte wall segment locations
        self.maze_segments = []
        self.WALL_WIDTH = 4
        self.MARGIN = 30
        self.WALL_LENGTH = 20 + self.WALL_WIDTH
        self.MATRIX_CENTERS = 48
        maze_matrix = GenerateMaze()

        ###create rectangles for the maze to draw
        for i in range(maze_matrix.row_length):  #for each of the rows
            print maze_matrix.maze_matrix[i][:]
            for j in range(maze_matrix.column_length):      #for each of the columns
                ####four different cases here####
                if maze_matrix.maze_matrix[i][j] == 1:
                    if i != 0:
                        if maze_matrix.maze_matrix[i-1][j] == 1:        ##upper wall
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN + j*self.MATRIX_CENTERS + self.WALL_WIDTH/2,
                                                 self.MARGIN +i*self.MATRIX_CENTERS + self.WALL_WIDTH - self.WALL_LENGTH, 
                                                 self.WALL_WIDTH, 
                                                 self.WALL_LENGTH))
                    if j != 0:
                        if maze_matrix.maze_matrix[i][j-1] == 1:
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN +j*self.MATRIX_CENTERS +  self.WALL_WIDTH - self.WALL_LENGTH, 
                                                self.MARGIN + i*self.MATRIX_CENTERS + self.WALL_WIDTH/2, 
                                                self.WALL_LENGTH, 
                                                self.WALL_WIDTH))
                    if j != maze_matrix.column_length - 1:
                        if maze_matrix.maze_matrix[i][j + 1] == 1:
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN +j*self.MATRIX_CENTERS +  self.WALL_WIDTH, 
                                                self.MARGIN + i*self.MATRIX_CENTERS + self.WALL_WIDTH/2, 
                                                self.WALL_LENGTH, 
                                                self.WALL_WIDTH))
                    if i != maze_matrix.row_length - 1:
                        if maze_matrix.maze_matrix[i+1][j] == 1:        ##upper wall
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN + j*self.MATRIX_CENTERS + self.WALL_WIDTH/2,
                                                 self.MARGIN +i*self.MATRIX_CENTERS + self.WALL_WIDTH, 
                                                 self.WALL_WIDTH, 
                                                 self.WALL_LENGTH))

        #initialize a list of maze segments rectangles
        self.rect = []
        for obj in self.maze_segments:
            self.rect.append(obj.rect)

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
        self.move_ticker = 0
    def handle_event(self, event):
        self.model.character.rect = pygame.Rect(self.model.character.x_pos, self.model.character.y_pos,
            self.model.character.width, self.model.character.height)

        left = False
        keys = pygame.key.get_pressed()
        #if event.type == pygame.KEYDOWN:

        #check for collisions
        collide = self.model.character.rect.collidelist(self.model.rect) != -1
        print collide

        direction_vel = [1,1,1,1]

        if keys[pygame.K_a] and collide:
            direction_vel[0] = 0
        elif keys[pygame.K_d] and collide:
            direction_vel[1] = 0
        elif keys[pygame.K_w] and collide:
            direction_vel[2] = 0
        elif keys[pygame.K_s] and collide:
            direction_vel[3] = 0
        """for diagonal movement, check diagonal first"""
        if keys[pygame.K_a] and keys[pygame.K_w]:
            if self.move_ticker > self.model.character.refresh_rate + 2:
                self.move_ticker = 0
                self.model.character.x_pos -= self.model.character.vel
                self.model.character.y_pos -= self.model.character.vel
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            if self.move_ticker > self.model.character.refresh_rate + 2:
                self.move_ticker = 0
                self.model.character.x_pos -= self.model.character.vel
                self.model.character.y_pos += self.model.character.vel
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            if self.move_ticker > self.model.character.refresh_rate + 2:
                self.move_ticker = 0
                self.model.character.x_pos += self.model.character.vel
                self.model.character.y_pos -= self.model.character.vel
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            if self.move_ticker > self.model.character.refresh_rate + 2:
                self.move_ticker = 0
                self.model.character.x_pos += self.model.character.vel
                self.model.character.y_pos += self.model.character.vel
        elif keys[pygame.K_a]: ##for horizontal, vertical movement
            if self.move_ticker > self.model.character.refresh_rate:
                self.move_ticker = 0
                self.model.character.x_pos -= self.model.character.vel
        elif keys[pygame.K_d]:
            if self.move_ticker > self.model.character.refresh_rate:
                self.move_ticker = 0
                self.model.character.x_pos += self.model.character.vel
        elif keys[pygame.K_w]:
            if self.move_ticker > self.model.character.refresh_rate:
                self.move_ticker = 0
                self.model.character.y_pos -= self.model.character.vel
        elif keys[pygame.K_s]:
            if self.move_ticker > self.model.character.refresh_rate:
                self.move_ticker = 0
                self.model.character.y_pos += self.model.character.vel
        self.move_ticker += 1

if __name__ == '__main__':
    pygame.init()
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    model = EscapeTheMazeModel()
    view = PygameEscapeTheMazeView(model, screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        controller.handle_event(event)
        view.draw()
        time.sleep(.001)