"""
@Author: Cedric Kim, Kevin Guo
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import math
from random import choice
import random
from Maze_Test import create_maze


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
        for rect in self.model.maze_rect_list:
            pygame.draw.rect(self.screen, pygame.Color('black'), rect)
        for scroll in self.model.scroll_list:
            rect = (scroll.x_pos, scroll.y_pos, scroll.width, scroll.height)
            pygame.draw.rect(self.screen, pygame.Color('gold'), rect)
        #for maze_segment in self.model.maze_segments:
        #    rect = pygame.Rect(maze_segment.x_pos, maze_segment.y_pos, maze_segment.width, maze_segment.height)
        #    pygame.draw.rect(self.screen, pygame.Color('black'), rect)
        #draw the maze character
        r = self.model.character.rect
        pygame.draw.rect(self.screen, pygame.Color(self.model.character.color), r)
        
        self.model.fog_of_war.draw_fog_of_war(self.screen)
        #for rect in self.model.collision.collision_rect_list:
        #   pygame.draw.rect(self.screen, pygame.Color('green'), rect)
        pygame.display.update()

class GenerateMaze(object):
    def __init__(self, length, height):
        ##rand_number between 0-10, 10 represents no walls, 0 represents all walls
        self.maze_matrix = create_maze(length, height)
        self.maze_matrix_test = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
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
    def update_maze(self):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
class FogOfWar(object):
    def __init__(self, character, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.character = character
    def update_fog_of_war(self):
        self.x_pos = self.character.x_pos + self.character.width/2
        self.y_pos = self.character.y_pos + self.character.height/2
    def draw_fog_of_war(self, screen):
        left_rect = pygame.Rect(0, 0, self.x_pos - self.radius, 1000)
        right_rect = pygame.Rect(self.x_pos + self.radius, 0, 1000, 1000)
        bottom_rect = pygame.Rect(0, self.y_pos + self.radius, 1000, 1000)
        top_rect = pygame.Rect(0, 0, 1000,  self.y_pos - self.radius)
        pygame.draw.rect(screen, pygame.Color('black'), left_rect)
        pygame.draw.rect(screen, pygame.Color('black'), right_rect)
        pygame.draw.rect(screen, pygame.Color('black'), bottom_rect)
        pygame.draw.rect(screen, pygame.Color('black'), top_rect)
        for i in range(50):
            ang = i * math.pi * 2.0 / 50
            dx = int(math.cos(ang) * (self.radius + 50))
            dy = int(math.sin(ang) * (self.radius + 50))
            x = self.x_pos + dx
            y = self.y_pos + dy
            pygame.draw.circle(screen, 
                            pygame.Color('black'), 
                            (x, y), 
                            50)
class Scroll(object):
    def __init__(self, width, height, MATRIX_CENTERS, MAZE_LENGTH, MAZE_HEIGHT):
        r = random.randint(1, MAZE_LENGTH - 1)
        self.x_pos = r*MATRIX_CENTERS*2 + MATRIX_CENTERS
        r = random.randint(1, MAZE_HEIGHT - 1)
        self.y_pos = r*MATRIX_CENTERS*2 + MATRIX_CENTERS
        self.width = width
        self.height = height
class Character(object):
    """represents the character"""
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rel_x_pos = x_pos
        self.rel_y_pos = y_pos
        self.width = width
        self.height = height
        self.color = "red"
        self.vel = 2           #how many pixels it updates
        self.diag_vel = 2/1.4
        self.refresh_rate = 0  #how many loops before it updates the velocity
    def update_relative_positions(rel_x_pos, rel_y_pos):
        self.rel_x_pos = rel_x_pos
        self.rel_y_pos = rel_y_pos

class Collision_Detection(object):
    def __init__(self, character, width, height, model):
        self.character = character
        self.width = width
        self.height = height
        self.scroll = model.scroll
        self.number_of_scrolls = model.number_of_scrolls
        ##create rectangle list and boolean list
        self.collision_rect_list = []
        self.collision_bool_list = []
        self.scroll_bool_list = []
        self.collision_character_bool = 'false'
        ##add four rectangles 
        for i in range(4):
            self.collision_rect_list.append(pygame.Rect(0,0,0,0))
        for i in range(4):
            self.collision_bool_list.append('False')
        for i in range(self.number_of_scrolls):
            self.scroll_bool_list.append('False')

    def return_collision_bool(self, rect, rect_list):
        ##check if rect is intersecting with elements in maze_rect_list
            return rect.collidelist(rect_list) != -1

    def update_collision(self, character, maze_rect_list, scroll_rect_list):
        #creates new collision rectangles and stores them in the list initialized
        self.collision_rect_list[0] = pygame.Rect(character.x_pos - self.width,
                                                        character.y_pos,
                                                        self.width,
                                                        self.height)
        self.collision_rect_list[1] = pygame.Rect(character.x_pos + character.width,
                                                        character.y_pos,
                                                        self.width,
                                                        self.height)
        self.collision_rect_list[2] = pygame.Rect(character.x_pos,
                                                        character.y_pos - self.width,
                                                        self.height,
                                                        self.width)
        self.collision_rect_list[3] = pygame.Rect(character.x_pos,
                                                        character.y_pos + character.height,
                                                        self.height,
                                                        self.width)
        for i in range(len(self.collision_rect_list)):
            self.collision_bool_list[i] = self.return_collision_bool(self.collision_rect_list[i],
                                                                maze_rect_list)
        self.collision_character_bool = self.return_collision_bool(self.character.rect, maze_rect_list)

        for i in range(len(scroll_rect_list)):
            self.scroll_bool_list[i] = (1 == self.character.rect.colliderect(scroll_rect_list[i]))

class EscapeTheMazeModel(object):
    def __init__(self):
        ############################
        ##GERENATE MAZE RECTANGLES##
        ############################
        self.maze_segments = []
        self.WALL_WIDTH = 4
        self.MARGIN = 0
        self.WALL_LENGTH = 23 + self.WALL_WIDTH
        self.MATRIX_CENTERS = 53
        self.isolated_direction = 'yes'
        self.MAZE_LENGTH = 10
        self.MAZE_HEIGHT = 10
        self.number_of_scrolls = 4
        maze_matrix = GenerateMaze(self.MAZE_HEIGHT, self.MAZE_LENGTH)
        ###create rectangles for the maze to draw
        for i in range(maze_matrix.row_length):  #for each of the rows
            print maze_matrix.maze_matrix[i][:]
            for j in range(maze_matrix.column_length):      #for each of the columns
                ####four different cases here####
                if maze_matrix.maze_matrix[i][j] == 1:
                    if i != 0:
                        if maze_matrix.maze_matrix[i-1][j] == 1:        ##upper wall
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN + j*self.MATRIX_CENTERS,
                                                 self.MARGIN +i*self.MATRIX_CENTERS - self.WALL_LENGTH, 
                                                 self.WALL_WIDTH, 
                                                 self.WALL_LENGTH + self.WALL_WIDTH))
                            if self.isolated_direction == 'yes':
                                self.isolated_direction = 'down'
                            else:
                                self.isolated_direction = 'no'
                    if j != 0:
                        if maze_matrix.maze_matrix[i][j-1] == 1:
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN +j*self.MATRIX_CENTERS  - self.WALL_LENGTH, 
                                                self.MARGIN + i*self.MATRIX_CENTERS, 
                                                self.WALL_LENGTH + self.WALL_WIDTH, 
                                                self.WALL_WIDTH))
                            if self.isolated_direction == 'yes':
                                self.isolated_direction = 'right'
                            else:
                                self.isolated_direction = 'no'
                    if j != maze_matrix.column_length - 1:
                        if maze_matrix.maze_matrix[i][j + 1] == 1:
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN +j*self.MATRIX_CENTERS, 
                                                self.MARGIN + i*self.MATRIX_CENTERS, 
                                                self.WALL_LENGTH + self.WALL_WIDTH, 
                                                self.WALL_WIDTH))
                            if self.isolated_direction == 'yes':
                                self.isolated_direction = 'left'
                            else:
                                self.isolated_direction = 'no'
                    if i != maze_matrix.row_length - 1:
                        if maze_matrix.maze_matrix[i+1][j] == 1:        ##upper wall
                            self.maze_segments.append(CreateMazeSegment(self.MARGIN + j*self.MATRIX_CENTERS,
                                                 self.MARGIN +i*self.MATRIX_CENTERS, 
                                                 self.WALL_WIDTH, 
                                                 self.WALL_LENGTH + self.WALL_WIDTH))
                            if self.isolated_direction == 'yes':
                                self.isolated_direction = 'up'
                            else:
                                self.isolated_direction = 'no'
                    """if self.isolated_direction == 'up':
                        self.maze_segments.append(CreateMazeSegment(self.MARGIN + j*self.MATRIX_CENTERS + self.WALL_WIDTH/2,
                                                 self.MARGIN +i*self.MATRIX_CENTERS + self.WALL_WIDTH/2 - self.WALL_LENGTH, 
                                                 self.WALL_WIDTH, 
                                                 self.WALL_LENGTH + self.WALL_WIDTH))
                    elif self.isolated_direction == 'down':
                         self.maze_segments.append(CreateMazeSegment(self.MARGIN + j*self.MATRIX_CENTERS + self.WALL_WIDTH/2,
                                                 self.MARGIN +i*self.MATRIX_CENTERS + self.WALL_WIDTH/2, 
                                                 self.WALL_WIDTH, 
                                                 self.WALL_LENGTH + self.WALL_WIDTH))
                    elif self.isolated_direction == 'left':
                        self.maze_segments.append(CreateMazeSegment(self.MARGIN +j*self.MATRIX_CENTERS +  self.WALL_WIDTH/2 - self.WALL_LENGTH, 
                                                self.MARGIN + i*self.MATRIX_CENTERS + self.WALL_WIDTH/2, 
                                                self.WALL_LENGTH + self.WALL_WIDTH, 
                                                self.WALL_WIDTH))
                    elif self.isolated_direction == 'right':
                        self.maze_segments.append(CreateMazeSegment(self.MARGIN +j*self.MATRIX_CENTERS + self.WALL_WIDTH/2, 
                                                self.MARGIN + i*self.MATRIX_CENTERS + self.WALL_WIDTH/2, 
                                                self.WALL_LENGTH + self.WALL_WIDTH, 
                                                self.WALL_WIDTH))"""
                    self.isolated_direction = 'yes'
        self.maze_rect_list = []
        ##########################
        ##END OF MAZE GENERATION##
        ##########################
        #for obj in self.maze_segments:      ##for the objects in maze segments
        #    self.maze_rect_list.append(obj.rect)    ##the rectangle to a new list
        self.character = Character(500, 500, 21, 21)    ## create a new character
        ##create scrolls
        self.create_scrolls(self.number_of_scrolls)
        ##create 4 collision rectangles
        self.collision = Collision_Detection(self.character, 4, self.character.width, self)
        ##create fog of war
        self.fog_of_war = FogOfWar(self.character, self.character.x_pos, self.character.x_pos, 100)


    def HUD(self):
        font = pygame.font('sans,freesans,courier,arial', 18, True)
        self.scrolls_collected = font.render("asd")
    def create_scrolls(self, number_of_scrolls):
        self.scroll_list = []
        for i in range(number_of_scrolls):
            self.scroll = Scroll(7, 20, self.MATRIX_CENTERS, self.MAZE_LENGTH, self.MAZE_HEIGHT)
            self.scroll_list.append(self.scroll)
    def run_model(self):
        ##we need to run this for the rectangles to update
        ##update character block
        self.character.rect = pygame.Rect(self.character.x_pos, self.character.y_pos,
            self.character.width, self.character.height)
        #update collision rectangles and detection
        #update fog of war position
        self.fog_of_war.update_fog_of_war()
        self.scroll_rect_list = []
        for scroll in self.scroll_list:
            self.scroll_rect_list.append(pygame.Rect(scroll.x_pos, 
                                                    scroll.y_pos, 
                                                    scroll.width, 
                                                    scroll.height))
        self.maze_rect_list = []
        for maze_segment in self.maze_segments:      ##for the objects in maze segments
            maze_segment.update_maze()
            self.maze_rect_list.append(maze_segment.rect)    ##add the rectangle to a new list
        self.collision.update_collision(self.character, self.maze_rect_list, self.scroll_rect_list)
        print "1=", self.collision.scroll_bool_list[0], ",    ",  "2=", self.collision.scroll_bool_list[1], ",    ","3=", self.collision.scroll_bool_list[2], ",    ","4=", self.collision.scroll_bool_list[3]
        #self.maze_rect_list = CreateMazeSegment.update_maze(self.maze_segments)
        #self.maze_rect_list = []
        #for obj in self.maze_segments:      ##for the objects in maze segments
        #    self.maze_rect_list.append(obj.rect)    ##the rectangle to a new list

    def move_maze(self, x_vel, y_vel):
        for maze_segment in self.maze_segments:
            maze_segment.x_pos += x_vel
            maze_segment.y_pos += y_vel
    def move_scrolls(self, x_vel, y_vel):
        for scroll in self.scroll_list:
            scroll.x_pos += x_vel
            scroll.y_pos += y_vel
    def move_objects(self, x_vel, y_vel):
        self.move_maze(x_vel, y_vel)
        self.move_scrolls(x_vel, y_vel)
    #def update_maze_position(self, x_vel, y_vel)
class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
        self.move_ticker = 0
        self.character = self.model.character  #set attributes of character
        self.collision = self.model.collision

    def handle_event(self, event):
        y_vel = 0
        x_vel = 0
        keys = pygame.key.get_pressed()     ##find what keys were pressed
        model.run_model() ## run the model so we can change its attributes
        if self.move_ticker > self.model.character.refresh_rate:
            ## change diagonals first
            if keys[pygame.K_a] and keys[pygame.K_s] and not self.collision.collision_character_bool:
                x_vel = -self.character.diag_vel
                y_vel = self.character.diag_vel
            elif keys[pygame.K_a] and keys[pygame.K_w] and not self.collision.collision_character_bool:
                x_vel = -self.character.diag_vel
                y_vel = -self.character.diag_vel
            elif keys[pygame.K_d] and keys[pygame.K_s] and not self.collision.collision_character_bool:
                x_vel = self.character.diag_vel
                y_vel = self.character.diag_vel
            elif keys[pygame.K_d] and keys[pygame.K_w] and not self.collision.collision_character_bool:
                x_vel = self.character.diag_vel
                y_vel = -self.character.diag_vel
            ##check horizontal/vertical after
            elif keys[pygame.K_a] and not self.collision.collision_character_bool:
                x_vel = -self.character.vel
            elif keys[pygame.K_d] and not self.collision.collision_character_bool:
                x_vel = self.character.vel
            elif keys[pygame.K_w] and not self.collision.collision_character_bool:
                y_vel = -self.character.vel
            elif keys[pygame.K_s] and not self.collision.collision_character_bool:
                y_vel = self.character.vel
            ##if there is a collision, and the key is pressed, the velocity is zero
            if self.collision.collision_bool_list[0] and keys[pygame.K_a]:
                x_vel = 0
            if self.collision.collision_bool_list[1] and keys[pygame.K_d]:
                x_vel = 0
            if self.collision.collision_bool_list[2] and keys[pygame.K_w]:
                y_vel = 0
            if self.collision.collision_bool_list[3] and keys[pygame.K_s]:
                y_vel = 0
            ##for the keys pressed, we can add the velocity to the position
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.character.rel_x_pos += x_vel
                self.model.move_objects(-x_vel, 0)
            if keys[pygame.K_s] or keys[pygame.K_w]:
                self.character.rel_y_pos += y_vel
                self.model.move_objects(0, -y_vel)
            self.move_ticker = 0
        ##if original collides, move outwards
        if self.collision.collision_character_bool:
            if self.collision.collision_bool_list[0]:
                self.model.move_objects(-1, 0)
                self.character.rel_x_pos += 1
            if self.collision.collision_bool_list[1]:
                self.model.move_objects(1, 0)
                self.character.rel_x_pos -= 1
            if self.collision.collision_bool_list[2]:
                self.model.move_objects(0, -1)
                self.character.rel_y_pos += 1
            if self.collision.collision_bool_list[3]:
                self.model.move_objects(0, 1)
                self.character.rel_y_pos -= 1
        #self.model.update_maze_position(self.character.rel_x_pos, self.character.rel_y_pos)
        print "(            " , self.character.rel_x_pos , ", " , self.character.rel_y_pos
        #self.model.character.update_relative_positions()
        self.move_ticker += 1

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    model = EscapeTheMazeModel()
    view = PygameEscapeTheMazeView(model, screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False
        controller.handle_event(event)
        view.draw()
        time.sleep(.001)