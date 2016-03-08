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
        self.font1 = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)
        self.font2 = pygame.font.SysFont('sans,freesans,courier,arial', 48, True)
        self.win = False

    def draw(self):
        """Draw the game state to the screen"""
        
        self.screen.fill(pygame.Color('grey'))
        ##draw the maze
        for rect in self.model.lists.maze_segment_rect_list:
            pygame.draw.rect(self.screen, pygame.Color('black'), rect)

        for scroll in self.model.lists.scroll_list:
            rect = (scroll.x_pos, scroll.y_pos, scroll.width, scroll.height)
            pygame.draw.rect(self.screen, pygame.Color('gold'), rect)

        pygame.draw.rect(self.screen, pygame.Color('blue'), self.model.exit.rect)
        #draw the maze character
        r = self.model.character.rect
        pygame.draw.rect(self.screen, pygame.Color(self.model.character.color), r)


        self.screen.blit(self.font1.render("Scrolls: " + str(self.model.lists.starting_number_of_scrolls- self.model.lists.number_of_scrolls) + "/" + str(self.model.lists.starting_number_of_scrolls), True, (0, 0, 255)), (1100, 20))
        if self.win or (self.model.lists.number_of_scrolls == 0 and self.model.collision.exit_collision == True):
            self.win = True
            self.screen.blit(self.font2.render("YOU WIN!", True, (0, 0, 255)), (500, 500))
        #self.model.fog_of_war.draw_fog_of_war(self.screen)
        #for rect in self.model.lists.collision_rect_list:
        #   pygame.draw.rect(self.screen, pygame.Color('green'), rect)
        pygame.display.update()

class Maze(object):
    def __init__(self, MAZE_LENGTH, MAZE_HEIGHT):
        """Initializes all attributes necessary to create a maze"""
        self.maze_segment_list = []
        self.WALL_WIDTH = 4
        self.MARGIN = 0
        self.WALL_LENGTH = 23 + self.WALL_WIDTH
        self.MATRIX_CENTERS = 53
        self.isolated_direction = 'yes'
        self.MAZE_LENGTH = MAZE_LENGTH
        self.MAZE_HEIGHT = MAZE_HEIGHT
        self.maze_matrix = create_maze(MAZE_LENGTH, MAZE_HEIGHT)
        self.row_length = len(self.maze_matrix)
        self.column_length = len(self.maze_matrix[0][:])
        #self.maze_segment = Maze_Segment(0, 0, 0, 0)        ##initialize maze_segment, so we can grab attributes later

class Maze_Segment(object):
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = "black"
    #def update_maze(self):
     #   self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

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
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
    #def update_scrolls(self):
     #   for i in range(len(Collision_Detection.scroll_bool_list))
     #       if Collision_Detection.scroll_bool_list[i]:
     #           Collision_Detection.scroll_
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
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
    def update_relative_positions(rel_x_pos, rel_y_pos):
        self.rel_x_pos = rel_x_pos
        self.rel_y_pos = rel_y_pos

class Exit(object):
    def __init__(self, width, height, MATRIX_CENTERS, MAZE_LENGTH, MAZE_HEIGHT):
        self.x_pos = random.randint(1, MAZE_LENGTH - 1)*MATRIX_CENTERS*2 + MATRIX_CENTERS
        self.y_pos = random.randint(1, MAZE_LENGTH - 1)*MATRIX_CENTERS*2 + MATRIX_CENTERS
        self.rect = pygame.Rect(0,0,0,0)
        self.width = width
        self.height = height
        self.center = self.update_center()

    def update_center(self):
        return [self.x_pos - self.width/2, self.y_pos - self.height/2]

    def update_exit_rect(self):
        self.rect = pygame.Rect(self.x_pos - self.width/2, self.y_pos - self.height/2, self.width, self.height)

class Lists(object):
    def __init__(self, character, maze, collision):
        """This class creates all the necessary lists in order to compute collisions, update drawings, etc."""
        self.character = character
        self.collision = collision
        self.maze = maze
        self.scroll_list = []       ##holds objects of scrolls in a list
        self.scroll_rect_list = []  ##holds rectangles of scrolls in a list
        self.number_of_scrolls = 2
        self.starting_number_of_scrolls = self.number_of_scrolls
        self.create_scroll_list(self.number_of_scrolls)  ##create 4 scrolls, randomly generated
        self.maze_segment_list = [] ##create a list of objects for the maze segments
        self.maze_segment_rect_list = []    ##create rectangles to go in the list

        self.collision_rect_list = []       ##create 4 rectangles to place around the character
        self.collision_rect_is_colliding_list = []  ##create 4 bools to see if the rectangles colide with the maze
        self.scroll_is_colliding_list = []       ##create scroll boolean list

        for i in range(self.number_of_scrolls):
            self.scroll_is_colliding_list.append(False)     ##create a list of bools for scrolls
        for i in range(4):
            self.collision_rect_list.append(pygame.Rect(-5,-5,0,0))
        for i in range(4):
            self.collision_rect_is_colliding_list.append(False)

        ####################################
        ##GERENATE MAZE SEGMENT RECTANGLES##
        ####################################
        ###create rectangles for the maze to draw
        for i in range(self.maze.row_length):  ##for each of the rows
            print self.maze.maze_matrix[i][:]
            for j in range(self.maze.column_length):      ##for each of the columns
                ####four different cases here####
                if self.maze.maze_matrix[i][j] == 1:
                    if i != 0:
                        if self.maze.maze_matrix[i-1][j] == 1:        ##upper wall
                            self.maze_segment_list.append(Maze_Segment(self.maze.MARGIN + j*self.maze.MATRIX_CENTERS,
                                                 self.maze.MARGIN +i*self.maze.MATRIX_CENTERS - self.maze.WALL_LENGTH, 
                                                 self.maze.WALL_WIDTH, 
                                                 self.maze.WALL_LENGTH + self.maze.WALL_WIDTH))
                            if self.maze.isolated_direction == 'yes':
                                self.maze.isolated_direction = 'down'
                            else:
                                self.maze.isolated_direction = 'no'
                    if j != 0:
                        if self.maze.maze_matrix[i][j-1] == 1:
                            self.maze_segment_list.append(Maze_Segment(self.maze.MARGIN +j*self.maze.MATRIX_CENTERS  - self.maze.WALL_LENGTH, 
                                                self.maze.MARGIN + i*self.maze.MATRIX_CENTERS, 
                                                self.maze.WALL_LENGTH + self.maze.WALL_WIDTH, 
                                                self.maze.WALL_WIDTH))
                            if self.maze.isolated_direction == 'yes':
                                self.maze.isolated_direction = 'right'
                            else:
                                self.maze.isolated_direction = 'no'
                    if j != self.maze.column_length - 1:
                        if self.maze.maze_matrix[i][j + 1] == 1:
                            self.maze_segment_list.append(Maze_Segment(self.maze.MARGIN +j*self.maze.MATRIX_CENTERS, 
                                                self.maze.MARGIN + i*self.maze.MATRIX_CENTERS, 
                                                self.maze.WALL_LENGTH + self.maze.WALL_WIDTH, 
                                                self.maze.WALL_WIDTH))
                            if self.maze.isolated_direction == 'yes':
                                self.maze.isolated_direction = 'left'
                            else:
                                self.maze.isolated_direction = 'no'
                    if i != self.maze.row_length - 1:
                        if self.maze.maze_matrix[i+1][j] == 1:
                            self.maze_segment_list.append(Maze_Segment(self.maze.MARGIN + j*self.maze.MATRIX_CENTERS,
                                                 self.maze.MARGIN +i*self.maze.MATRIX_CENTERS, 
                                                 self.maze.WALL_WIDTH, 
                                                 self.maze.WALL_LENGTH + self.maze.WALL_WIDTH))
                            if self.maze.isolated_direction == 'yes':
                                self.maze.isolated_direction = 'up'
                            else:
                                self.maze.isolated_direction = 'no'
                    self.maze.isolated_direction = 'yes'

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

    def create_scroll_list(self, number_of_scrolls):
        """create a number of randomly generated scrolls"""

        for i in range(number_of_scrolls):
            x = random.randint(1, self.maze.MAZE_LENGTH - 1)
            x_pos = x*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            y = random.randint(1, self.maze.MAZE_HEIGHT - 1)
            y_pos = y*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            scroll = Scroll(x_pos, y_pos, 7, 20)
            self.scroll_list.append(scroll)
    def update_scroll_rect_list(self):
        """updates the scroll rectangles into a list"""
        self.number_of_scrolls = len(self.scroll_list)
        self.scroll_rect_list = []
        ## for each obj in scroll_list, create a new list of the rectangles
        for scroll in self.scroll_list:
            self.scroll_rect_list.append(pygame.Rect(scroll.x_pos, scroll.y_pos, scroll.width, scroll.height))

    def update_maze_segment_rect_list(self):
        """updates the maze_segments rectangles into a list"""
        self.maze_segment_rect_list = []
        for maze_segment in self.maze_segment_list:      ##for the objects in maze segments
            self.maze_segment_rect_list.append(pygame.Rect(maze_segment.x_pos,  ##add the rectangle to a new list
                                                            maze_segment.y_pos, 
                                                            maze_segment.width, 
                                                            maze_segment.height))
        #print len(self.maze_segment_rect_list)
    def update_collision_rect_list(self):
        """updates the collision rectangles into a list"""
        collision_rect = Collision_Rectangle(0, 0, 2, 20)
        self.collision_rect_list[0] = pygame.Rect(self.character.x_pos - collision_rect.width, 
                                                    self.character.y_pos,
                                                    collision_rect.width,
                                                    collision_rect.height)
        self.collision_rect_list[1] = pygame.Rect(self.character.x_pos + self.character.width,
                                                    self.character.y_pos,
                                                    collision_rect.width,
                                                    collision_rect.height)
        self.collision_rect_list[2] = pygame.Rect(self.character.x_pos,
                                                    self.character.y_pos - collision_rect.width,
                                                    collision_rect.height,
                                                    collision_rect.width)
        self.collision_rect_list[3] = pygame.Rect(self.character.x_pos,
                                                    self.character.y_pos + self.character.height,
                                                    collision_rect.height,
                                                    collision_rect.width)
    def update_collision_rect_is_colliding_list(self):
        """updates the booleans in the collision list"""
        #self.char_rect_is_colliding_list = []
        for i, collision_rect in enumerate(self.collision_rect_list):
            self.collision_rect_is_colliding_list[i] = self.collision.return_collision_bool(collision_rect, 
                                                                                            self.maze_segment_rect_list)
    def update_scroll_is_colliding_list(self):
        """updates the booleans for the scrolls into a list"""
        for i in range(len(self.scroll_rect_list)):
            self.scroll_is_colliding_list[i] = (1 == self.character.rect.colliderect(self.scroll_rect_list[i]))


class Collision_Rectangle(object):
    """defines the collision rectangle"""
    def __init__(self, x_pos, y_pos, width = 2, height = 20):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

class Collision_Detection(object):
    """defines collisions"""
    def __init__(self, character, model):
        self.character = character
        self.model = model
        self.char_is_colliding = False
        self.exit_collision = False
        ##create rectangle list and boolean list
        #def create_collision_rectangle():
    def return_collision_bool(self, rect, rect_list):
        """check if rect is intersecting with elements in maze_rect_list"""
        return rect.collidelist(rect_list) != -1

    def update_character_collision(self):
        """"sees if the character collides with the maze"""
        self.char_is_colliding = self.return_collision_bool(self.character.rect, self.model.lists.maze_segment_rect_list)
    def update_exit_collision(self):
        self.exit_collision = self.character.rect.colliderect(self.model.exit.rect) == 1

class EscapeTheMazeModel(object):
    def __init__(self):
        self.character = Character(500, 500, 21, 21)    ## create a new character
        self.collision = Collision_Detection(self.character, self)
        self.maze = Maze(10, 10)                        ##creates the maze
        self.lists = Lists(self.character, self.maze, self.collision)
        self.fog_of_war = FogOfWar(self.character,         ##create fog of war
                                    self.character.x_pos, 
                                    self.character.x_pos, 100)
        self.exit = Exit(30, 30, self.maze.MATRIX_CENTERS, self.maze.MAZE_LENGTH, self.maze.MAZE_HEIGHT)

    def HUD(self):
        font = pygame.font('sans,freesans,courier,arial', 18, True)
        self.scrolls_collected = font.render("asd")

    def run_model(self):
        """runs all the updates so we can update the rectangles"""
        ##update character block

        #update collision rectangles and detection
        #update fog of war position
        self.fog_of_war.update_fog_of_war()
        self.update_entities()
        #self.lists.maze_segment_rect_list = []
        #self.collision.update_collision(self.character, self.lists.maze_segment_rect_list, self.lists.scroll_rect_list)
        # scroll_collided = self.collision.scroll_bool_list
        #print len(self.collision.scroll_is_colliding_list)
        # print "1=", self.collision.scroll_is_colliding_list[0], ",    ",  "2=", self.collision.scroll_is_colliding_list[1], ",    ","3=", self.collision.scroll_is_colliding_list[2], ",    ","4=", self.collision.scroll_is_colliding_list[3]
        #self.maze_rect_list = CreateMazeSegment.update_maze(self.maze_segments)
        #self.maze_rect_list = []
        #for obj in self.maze_segments:      ##for the objects in maze segments
        #    self.maze_rect_list.append(obj.rect)    ##the rectangle to a new list

    def move_maze(self, x_vel, y_vel):
        """moves the maze"""
        """for maze_segment in self.lists.maze_segment_list:
            maze_segment.x_pos += x_vel
            maze_segment.y_pos += y_vel"""
        pass

    def move_scrolls(self, x_vel, y_vel):
        """same as move_maze"""
        """for scroll in self.lists.scroll_list:
            scroll.x_pos += x_vel
            scroll.y_pos += y_vel"""
        pass

    def move_exit(self, x_vel, y_vel):
        """self.exit.x_pos += x_vel
        self.exit.y_pos += y_vel"""
        pass

    def move_objects(self, x_vel, y_vel):
        """moves scroll and maze together"""
        self.move_maze(x_vel, y_vel)
        self.move_scrolls(x_vel, y_vel)
        self.move_exit(x_vel, y_vel)
    def update_character(self):
        self.character.rect.left = self.character.x_pos
        self.character.rect.top = self.character.y_pos

    def update_scrolls(self):
        collision_scroll_index = -1
        if self.character.rect.collidelist(self.lists.scroll_rect_list) != -1:
            for i in range(self.lists.number_of_scrolls):
                if self.lists.scroll_is_colliding_list[i]:
                    collision_scroll_index = i
        if collision_scroll_index != -1:
            self.lists.scroll_list.pop(collision_scroll_index)
        #print len(self.lists.scroll_list)

    def update_entities(self):
        """updates everything"""
        self.update_character()
        self.collision.update_character_collision() ##changes bool if character collides with maze
        self.lists.update_maze_segment_rect_list()  ##updates the  maze_segment rectangles
        self.lists.update_scroll_rect_list()        ##updates the scroll rectangles
        self.lists.update_collision_rect_list()     ##updates the collision rectangles
        self.lists.update_collision_rect_is_colliding_list()    ##updates the collision booleans
        self.lists.update_scroll_is_colliding_list()            ##updates the scroll collision booleans
        self.collision.update_exit_collision()
        self.update_scrolls()
        self.exit.update_exit_rect()

    #def update_maze_position(self, x_vel, y_vel)
class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
        self.move_ticker = 0
        self.character = self.model.character  #set attributes of character
        self.collision = self.model.collision
        self.lists = self.model.lists
    def handle_event(self, event):
        y_vel = 0
        x_vel = 0
        keys = pygame.key.get_pressed()     ##find what keys were pressed
        if self.move_ticker >= self.model.character.refresh_rate:
            ## change diagonals first
            if keys[pygame.K_a] and keys[pygame.K_s] and not self.collision.char_is_colliding:
                x_vel = -self.character.diag_vel
                y_vel = self.character.diag_vel
            elif keys[pygame.K_a] and keys[pygame.K_w] and not self.collision.char_is_colliding:
                x_vel = -self.character.diag_vel
                y_vel = -self.character.diag_vel
            elif keys[pygame.K_d] and keys[pygame.K_s] and not self.collision.char_is_colliding:
                x_vel = self.character.diag_vel
                y_vel = self.character.diag_vel
            elif keys[pygame.K_d] and keys[pygame.K_w] and not self.collision.char_is_colliding:
                x_vel = self.character.diag_vel
                y_vel = -self.character.diag_vel
            ##check horizontal/vertical after
            elif keys[pygame.K_a] and not self.collision.char_is_colliding:
                x_vel = -self.character.vel
            elif keys[pygame.K_d] and not self.collision.char_is_colliding:
                x_vel = self.character.vel
            elif keys[pygame.K_w] and not self.collision.char_is_colliding:
                y_vel = -self.character.vel
            elif keys[pygame.K_s] and not self.collision.char_is_colliding:
                y_vel = self.character.vel
            ##if there is a collision, and the key is pressed, the velocity is zero
            if self.lists.collision_rect_is_colliding_list[0] and keys[pygame.K_a]:
                x_vel = 0
            if self.lists.collision_rect_is_colliding_list[1] and keys[pygame.K_d]:
                x_vel = 0
            if self.lists.collision_rect_is_colliding_list[2] and keys[pygame.K_w]:
                y_vel = 0
            if self.lists.collision_rect_is_colliding_list[3] and keys[pygame.K_s]:
                y_vel = 0
            ##for the keys pressed, we can add the velocity to the position
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.character.rel_x_pos += x_vel
                self.model.move_objects(-x_vel, 0)
                self.character.x_pos += x_vel
            if keys[pygame.K_s] or keys[pygame.K_w]:
                self.character.rel_y_pos += y_vel
                self.model.move_objects(0, -y_vel)
                self.character.y_pos += y_vel
            self.move_ticker = 0
        ##if original collides, move outwards
        if self.collision.char_is_colliding:
            if self.lists.collision_rect_is_colliding_list[0]:
                self.model.move_objects(-1, 0)
                self.character.rel_x_pos += 1
                self.character.x_pos += 1
            if self.lists.collision_rect_is_colliding_list[1]:
                self.model.move_objects(1, 0)
                self.character.rel_x_pos -= 1
                self.character.x_pos -= 1
            if self.lists.collision_rect_is_colliding_list[2]:
                self.model.move_objects(0, -1)
                self.character.rel_y_pos += 1
                self.character.y_pos += 1
            if self.lists.collision_rect_is_colliding_list[3]:
                self.model.move_objects(0, 1)
                self.character.rel_y_pos -= 1
                self.character.y_pos -= 1
        #self.model.update_maze_position(self.character.rel_x_pos, self.character.rel_y_pos)
        print "(            " , self.character.rel_x_pos , ", " , self.character.rel_y_pos
        #self.model.character.update_relative_positions()
        self.move_ticker += 1

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    size = (1250, 1250)
    screen = pygame.display.set_mode(size)
    model = EscapeTheMazeModel()
    view = PygameEscapeTheMazeView(model, screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        model.run_model() ## run the model
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False
        controller.handle_event(event)
        view.draw()
        time.sleep(.001)