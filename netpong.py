import pygame
from PodSixNet.Connection import connection, ConnectionListener
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import math
from random import choice
import random

class PygameEscapeTheMazeView(object):
    def __init__(self, model, screen, listener):
        """Initialize the view with the specified model"""
        self.model = model
        self.screen = screen
        self.listener = listener
        self.font1 = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)
        self.font2 = pygame.font.SysFont('sans,freesans,courier,arial', 48, True)
        self.win = False

    def draw(self):
        if self.listener.start:
            ## if the actual game has started background is grey
            self.screen.fill(pygame.Color('grey'))
            ##create the mazes for the rectangle
            for rect in self.model.lists.maze_segment_rect_list:
                pygame.draw.rect(self.screen, pygame.Color('black'), rect)

            dist = self.model.cartesian_dist()
            if dist < 255:
                color = ((192.0/255)*dist,(192.0/255)*dist,(192.0/255)*dist)
                # color = pygame.Color('black')
                pygame.draw.rect(self.screen, color, self.model.exit.rect)
                # print self.model.exit.rect
            scroll_counter = 0
            for i, rect in enumerate(self.model.lists.scroll_rect_list):
                if self.model.lists.scroll_list[i].is_visible:
                    pygame.draw.rect(self.screen, pygame.Color('gold'), rect)
                else:
                    scroll_counter += 1
            ##draw the character rectangles
            for i in range(scroll_counter):
                pygame.draw.rect(self.screen, pygame.Color('white'), (20*i + 10, 10, 15, 15))
            self.screen.blit(self.font1.render(str(scroll_counter) + '/' + str(len(model.lists.scroll_list)), True, (255,255,255)), (180, 6))

            for i in range(len(self.model.players)):
                if self.model.players[self.model.player_num].still_alive:
                    if self.model.players[i].still_alive:
                        char = self.model.players[i]
                        pygame.draw.rect(self.screen, pygame.Color(char.color), char.rect)
                else:
                    self.screen.fill((255,0,0))
                    self.screen.blit(self.font2.render("YOU GOT EATEN", True, (0,0,0)), (460, 500))

            # for rect in self.model.lists.collision_rect_list:
            #     pygame.draw.rect(self.screen, pygame.Color('green'), rect)
            
            if self.model.monster_num == self.model.player_num:
                self.screen.blit(self.font1.render("Monster", True, (0,0,0)), (460, 20))

            if self.model.player_num != self.model.monster_num:
                if self.win or (scroll_counter == len(self.model.lists.scroll_rect_list) and self.model.exit_collision):
                    self.win = True
                    self.screen.blit(self.font2.render("YOU WIN!", True, (0, 0, 255)), (500, 500))
            elif not(self.win or (scroll_counter == len(self.model.lists.scroll_rect_list))) and self.model.exit_collision:
                self.screen.blit(self.font1.render("You still need more scrolls...", True, (0, 0, 255)), (500, 500))
            
            self.model.check_game()
            pygame.display.update()

    def draw_lobby(self):
        pygame.draw.rect(self.screen, pygame.Color('red'), (50,50,50,50))
        self.screen.blit(self.font1.render('Waiting for players...', True, (0, 0, 255)), (460, 500))
        pygame.display.update()

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

class Maze(object):
    def __init__(self):
        """Initializes all attributes necessary to create a maze"""
        self.maze_segment_list = []
        self.WALL_WIDTH = 4
        self.MARGIN = 0
        self.WALL_LENGTH = 23 + self.WALL_WIDTH
        self.MATRIX_CENTERS = 53
        self.isolated_direction = 'yes'
        self.maze_matrix = []
        self.row_length = None
        self.column_length = None
        #self.maze_segment = Maze_Segment(0, 0, 0, 0)

class Maze_Segment(object):
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

class Scroll(object):
    def __init__(self, x_pos, y_pos, width, height, is_visible):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.is_visible = is_visible

class Exit(object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(self.x_pos - self.width/2, self.y_pos - self.height/2, self.width, self.height)
        self.center = self.update_center()

    def update_center(self):
        return [self.x_pos - self.width/2, self.y_pos - self.height/2]

class Character(object):
    """represents the character"""
    def __init__(self, x_pos, y_pos, rel_x_vel, rel_y_vel, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rel_x_pos = rel_x_vel
        self.rel_y_pos = rel_y_vel
        self.width = width
        self.height = height
        self.color = "red"
        self.VEL = 3           #how many pixels it updates
        self.DIAG_VEL = 3/1.4
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.monster = False
        self.still_alive = True
        self.center = self.update_center()

    def update_center(self):
        return [self.x_pos - self.width/2, self.y_pos - self.height/2]

    def update_relative_positions(rel_x_pos, rel_y_pos):
        self.rel_x_pos = rel_x_pos
        self.rel_y_pos = rel_y_pos

class Lists():
    def __init__(self, character, collision, maze):
        self.character = character
        self.collision = collision
        self.maze = maze
        self.maze_segment_list = [] ##create a list of objects for the maze segments
        self.maze_segment_rect_list = []    ##create rectangles to go in the list
        self.collision_rect_list = [0,0,0,0]       ##create 4 rectangles to place around the character
        self.collision_rect_is_colliding_list = [False, False, False, False]  ##create 4 bools to see if the rectangles colide with the maze
        self.scroll_is_colliding_list = [0,0,0,0]
        self.scroll_rect_list = []
        #self.scroll_is_visible = [True, True]
        self.number_of_scrolls = 0
        self.scroll_list = []
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
        for maze_segment in self.maze_segment_list:      ##for the objects in maze segments
            self.maze_segment_rect_list.append(pygame.Rect(maze_segment.x_pos,  ##add the rectangle to a new list
                                                            maze_segment.y_pos, 
                                                            maze_segment.width, 
                                                            maze_segment.height))

    def update_maze_segment_rect_list(self):
        """updates the maze_segments rectangles into a list"""
        self.maze_segment_rect_list = []
        for maze_segment in self.maze_segment_list:      ##for the objects in maze segments
            self.maze_segment_rect_list.append(pygame.Rect(maze_segment.x_pos,  ##add the rectangle to a new list
                                                            maze_segment.y_pos, 
                                                            maze_segment.width, 
                                                            maze_segment.height))

    def update_collision_rect_list(self):
        """updates the collision rectangles into a list"""
        collision_rect = CollisionRectangle(0, 0, 2, 20)
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

    def update_scroll_rect_list(self):
        """updates the scroll rectangles into a list"""
        self.scroll_rect_list = []
        ## for each obj in scroll_list, create a new list of the rectangles
        for scroll in self.scroll_list:
            self.scroll_rect_list.append(pygame.Rect(scroll.x_pos, scroll.y_pos, scroll.width, scroll.height))

    def update_collision_rect_is_colliding_list(self):
        """updates the booleans in the collision list"""
        #self.char_rect_is_colliding_list = []
        for i, collision_rect in enumerate(self.collision_rect_list):
            self.collision_rect_is_colliding_list[i] = self.collision.return_collision_bool(collision_rect, 
                                                                                            self.maze_segment_rect_list)

class CollisionRectangle(object):
    """defines the collision rectangle"""
    def __init__(self, x_pos, y_pos, width = 2, height = 20):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

class CollisionDetection(object):
    """defines collisions"""
    def __init__(self, character, model):
        self.character = character
        self.model = model
        self.char_is_colliding = False
        # self.exit_collision = False
        ##create rectangle list and boolean list
        #def create_collision_rectangle():
    def return_collision_bool(self, rect, rect_list):
        """check if rect is intersecting with elements in maze_rect_list"""
        return rect.collidelist(rect_list) != -1

    def update_character_collision(self):
        """"sees if the character collides with the maze"""
        self.char_is_colliding = self.return_collision_bool(self.character.rect, self.model.lists.maze_segment_rect_list)

class EscapeTheMazeClientModel(object):
    def __init__(self):
        self.WINDOW_WIDTH = 1100
        self.WINDOW_HEIGHT = 1100
        self.players = []#[Character(550, 550, 20, 20), Character(550, 550, 20, 20)]
        self.collision = None
        self.player_num = 0
        self.maze = Maze()
        self.lists = None ##initiate lists object
        self.char_list = None
        self.scroll_entity_list = []
        self.scroll_collision_index = -1
        # self.exit_collision = False
        self.temp_scroll_collision_index = -1
        self.scroll_removed = True
        self.fog_of_war = None
        self.exit = None
        self.connected_players = 0
        self.ticker = 0

    def run_model(self):
        self.fog_of_war.update_fog_of_war()

    def update_monster(self):
        if self.ticker >10:
            self.monster = self.players[self.monster_num]
            # print "player: ", self.player_num, self.players[self.player_num].rect, "monster: ", self.monster_num, self.players[self.monster_num].rect
            if self.players[self.player_num].rect.colliderect(self.monster.rect) and self.player_num != self.monster_num:
                # print 'collided'
                # print self.player_num, self.players[self.player_num].rect, self.monster_num, self.players[self.monster_num].rect
                self.players[self.player_num].still_alive = False
        if self.ticker < 11:
            self.ticker += 1

    def update_exit_collision(self):
        self.exit_collision = self.players[self.player_num].rect.colliderect(self.exit.rect) == 1

    def update_characters(self):
        for char in self.players:
            char.rect.left = char.x_pos
            char.rect.top = char.y_pos

    def update_entities(self):
        self.update_scrolls()
        self.lists.update_scroll_rect_list()
        self.update_exit()
        self.collision.update_character_collision()
        self.update_exit_collision()
        self.lists.update_maze_segment_rect_list()
        self.update_characters()
        self.update_monster()
        self.lists.update_collision_rect_list()
        self.lists.update_collision_rect_is_colliding_list()
        #self.lists.update_scroll_is_colliding_list()

    def update_scrolls(self):
        if self.player_num != self.monster_num:
            self.scroll_collision_index = self.players[self.player_num].rect.collidelist(self.lists.scroll_rect_list)
        if self.temp_scroll_collision_index != -1:
            self.lists.scroll_list[self.temp_scroll_collision_index].is_visible = False
            self.temp_scroll_collision_index = -1
        number_of_scrolls = 0
        for scroll in self.lists.scroll_list:
            if scroll.is_visible:
                number_of_scrolls += 1
        self.lists.number_of_scrolls = number_of_scrolls

    def update_exit(self):
        self.exit.rect = pygame.Rect(self.exit.x_pos - self.exit.width/2, self.exit.y_pos - self.exit.height/2, self.exit.width, self.exit.height)

    def move_maze(self, x_vel, y_vel):
        """moves the maze"""
        for maze_segment in self.lists.maze_segment_list:
            maze_segment.x_pos += x_vel
            maze_segment.y_pos += y_vel
    def move_scrolls(self, x_vel, y_vel):
        for scroll in self.lists.scroll_list:
            scroll.x_pos += x_vel
            scroll.y_pos += y_vel

    def move_exit(self, x_vel, y_vel):
        self.exit.x_pos += x_vel
        self.exit.y_pos += y_vel

    def move_objects(self, x_vel, y_vel):
        """moves scroll and maze together"""
        self.move_maze(x_vel, y_vel)
        self.move_scrolls(x_vel, y_vel)
        self.move_exit(x_vel,y_vel)

    def edit_maze_position(self):      ##this is run once on initilization
        for maze_segment in self.lists.maze_segment_list:
            maze_segment.x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
            maze_segment.y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos

    def edit_scroll_position(self):
        for scroll in self.lists.scroll_list:
            scroll.x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
            scroll.y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos

    def edit_exit_position(self):
        self.exit.x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
        self.exit.y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos

    def create_fog_of_war(self):
        self.fog_of_war = FogOfWar(self.players[self.player_num],         ##create fog of war
                            self.players[self.player_num].x_pos, 
                            self.players[self.player_num].x_pos, 100)

    def create_players(self):
        # print self.char_list
        for char_entity in self.char_list:
            ##create a new character in players for each entity in char_list
            new_char = Character(self.WINDOW_WIDTH/2, 
                                self.WINDOW_HEIGHT/2, 
                                char_entity[0], 
                                char_entity[1],
                                20, 
                                20)
            self.monster_num = char_entity[2]
            self.players.append(new_char)
            # print new_char.rect
            ##turns character entities into a Character to add to player

    def cartesian_dist(self):
        return math.sqrt((self.players[self.player_num].update_center()[0] - self.exit.update_center()[0])**2 +
                        (self.players[self.player_num].update_center()[1] - self.exit.update_center()[1])**2)

    def create_scrolls(self, scroll_entity_list):
        for scroll_entity in scroll_entity_list:
            ##create a new scroll in scroll_list for each entity in the list
            self.lists.scroll_list.append(Scroll(scroll_entity[0], scroll_entity[1], 7, 20, True))  ##adds a scroll into scroll_list, with width 7, height 20
        self.lists.number_of_scrolls = len(self.lists.scroll_list)

    def create_scroll_is_visible(self):
        self.scroll_is_visible = []
        for i in range(self.lists.number_of_scrolls):
            self.scroll_is_visible.append(True)
        #print len(self.lists.scroll_is_visible)

    def check_game(self):
        alive_players = 0
        for character in self.players:
            if character.still_alive:
                alive_players += 1

        # if alive_players == 1:
        #     pass
        #     # print "Game Over"
        # end_game()

        # alive_players = 0
        # for character_alive in self.still_alive:
        #     if character_alive:
        #         alive_players += 1


    def create_monster(self):
        self.players[self.monster_num].width = self.players[self.monster_num].width*1.5
        self.players[self.monster_num].height = self.players[self.monster_num].height*1.5
        self.players[self.monster_num].color = "black"
        self.players[self.monster_num].rect = pygame.Rect(self.players[self.monster_num].x_pos,
                                                                    self.players[self.monster_num].y_pos,
                                                                    self.players[self.monster_num].width,
                                                                    self.players[self.monster_num].height)
        self.monster = self.players[self.monster_num]
        # print "player: ", self.players[self.player_num].rect , "monster: ", self.monster.rect

# class for I/O on network
# this represent the player, too
class Listener(ConnectionListener): 
    # init the player
    def __init__(self, model, host, port):
        self.Connect((host, port))
        self.model = model
        self.ran_initiations = False
        # set the window
        #self.model = EscapeTheMazeModel()
        # self.view = PygameEscapeTheMazeView(self.model,self.screen)
        #self.controller = PyGameKeyboardController(self.model)
        
        # player number. this can be 0 (left player) or 1 (right player)
        #self.num = None
        # players' rects
       # self.players = (Character(640/2 + 20, 450, 20, 20),Character(640/2 - 20, 450, 20, 20))

        # True if the server sended the ready message
        self.ready = False
        # True if the game is working
        self.start = False
        self.running = True
        # font for writing the scores
        self.font = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)

    # function to manage character movement
    def Network_move(self, data):
        if data['player_number'] != self.model.player_num:
            self.model.players[data['player_number']].x_pos = 550 - self.model.players[self.model.player_num].rel_x_pos + data['rel_x_pos']
            self.model.players[data['player_number']].y_pos = 550 - self.model.players[self.model.player_num].rel_y_pos + data['rel_y_pos']

    def Network_generate_maze(self, data):
        self.model.maze.maze_matrix = data['maze_matrix']
        self.model.maze.row_length = len(self.model.maze.maze_matrix)
        #print self.model.maze.row_length
        self.model.maze.column_length = len(self.model.maze.maze_matrix[0][:])
        #print self.model.maze.column_length

    # get the player number
    def Network_number(self, data):
        self.model.player_num = data['num']
        #print data['num']
    def Network_initialize_entities(self, data):
        #self.model.test = data['char_list']
        self.model.char_list = data['char_list']
        self.model.scroll_entity_list = data['scroll_list']
        self.model.create_players()

    def Network_exit_location(self,data):
        exit_location = data['exit']
        self.model.exit = Exit(exit_location[0],exit_location[1])

    def Network_update_entities(self, data):
        #if data['player_number'] != self.model.player_num:
        self.model.temp_scroll_collision_index = data['scroll_collision_index']

    def Network_update_alive(self, data):
        self.model.players[data['player_number']].still_alive = data['still_alive']
    
    # def Network_monster_number(self,data):
    #     self.model.monster_num = data['monster_num']
    
    def Network_ready_players(self, data):
        self.model.connected_players = data['connected_players']

    # if the game is ready
    def Network_ready(self, data):
        self.ready = not self.ready

    # start the game
    def Network_start(self, data):
        self.ready = False
        self.start = True
    
    # mainloop
    def update_listener(self):
        if self.running:
            # update connection
            connection.Pump()
            # update the listener
            self.Pump()

            if self.start:
                if not self.ran_initiations:
                    print 'before lists'
                    #print self.model.player_number
                    self.model.collision = CollisionDetection(self.model.players[self.model.player_num], self.model)
                    self.model.lists = Lists(self.model.players[self.model.player_num], self.model.collision, self.model.maze)
                    self.model.create_scrolls(self.model.scroll_entity_list)
                    self.model.edit_maze_position()
                    self.model.edit_scroll_position()
                    self.model.edit_exit_position()
                    #self.model.create_scroll_is_visible()
                    self.model.create_fog_of_war()
                    self.ran_initiations = True
                    self.model.create_monster()
                # send to the server information about movement
                self.model.update_exit()
                self.model.update_scrolls()
                self.model.lists.update_scroll_rect_list()
                self.model.collision.update_character_collision()
                connection.Send({'action': 'move', 
                                    'player_number': self.model.player_num, 
                                    'rel_x_pos': self.model.players[self.model.player_num].rel_x_pos, 
                                    'rel_y_pos': self.model.players[self.model.player_num].rel_y_pos})
                self.model.lists.update_maze_segment_rect_list()
                self.model.update_characters()
                self.model.update_exit_collision()
                connection.Send({'action': 'move', 
                                    'player_number': self.model.player_num, 
                                    'rel_x_pos': self.model.players[self.model.player_num].rel_x_pos, 
                                    'rel_y_pos': self.model.players[self.model.player_num].rel_y_pos})
                self.model.lists.update_collision_rect_list()
                self.model.lists.update_collision_rect_is_colliding_list()
                self.model.update_monster()
                connection.Send({'action': 'move', 
                                    'player_number': self.model.player_num, 
                                    'rel_x_pos': self.model.players[self.model.player_num].rel_x_pos, 
                                    'rel_y_pos': self.model.players[self.model.player_num].rel_y_pos})
                
                if self.model.scroll_collision_index != -1:
                    connection.Send({'action': 'update_entities', 
                                    'player_number': self.model.player_num, 
                                    'scroll_collision_index': self.model.scroll_collision_index})

                if not self.model.players[self.model.player_num].still_alive:
                    connection.Send({'action': 'update_alive', 'player_number': self.model.player_num,
                                'still_alive': False})

                
            #print self.model.maze.maze_matrix
            # # if self.ready is True
            # if self.ready:
            #   # write some text
            #   self.screen.blit(self.font.render('Ready', True, (0, 0, 255)), (400-self.font.size('Ready')[0]/2, 290))
            #   # update the screen
            #   pygame.display.flip()
            # # print 'Waiting for players...'
            # elif not self.start:
            #   # write some text
            #   self.screen.blit(self.font.render('Waiting for players...', True, (255, 255, 255)), (400-self.font.size('Waiting for players...')[0]/2, 290))
            #   # update the screen
            #   pygame.display.flip()
    
            # wait 25 milliseconds
            #pygame.time.wait(1)

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
        self.move_ticker = 0
        self.REFRESH_RATE = 0 #how many loops before it updates the velocity
        self.DIAG_VEL = 3/1.4 #self.model.players[self.model.player_num].DIAG_VEL
        self.VEL = 3 #self.model.players[self.model.player_num].VEL
        #self.players = self.model.players  #set attributes of players
        #self.collision = self.model.collision
        #self.lists = self.model.lists
    def handle_event(self, event):
        if not self.model.players[self.model.player_num].still_alive:
            return
        y_vel = 0
        x_vel = 0
        keys = pygame.key.get_pressed()     ##find what keys were pressed
        #self.model.run_model() ## run the model so we can change its attributes
        if self.move_ticker > self.REFRESH_RATE:
            ## change diagonals first
            if keys[pygame.K_a] and keys[pygame.K_s]:
                x_vel = -self.DIAG_VEL
                y_vel = self.DIAG_VEL
            elif keys[pygame.K_a] and keys[pygame.K_w]:
                x_vel = -self.DIAG_VEL
                y_vel = -self.DIAG_VEL
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                x_vel = self.DIAG_VEL
                y_vel = self.DIAG_VEL
            elif keys[pygame.K_d] and keys[pygame.K_w]:
                x_vel = self.DIAG_VEL
                y_vel = -self.DIAG_VEL
            ##check horizontal/vertical after
            elif keys[pygame.K_a] and not self.model.collision.char_is_colliding:
                x_vel = -self.VEL
            elif keys[pygame.K_d] and not self.model.collision.char_is_colliding:
                x_vel = self.VEL
            elif keys[pygame.K_w] and not self.model.collision.char_is_colliding:
                y_vel = -self.VEL
            elif keys[pygame.K_s] and not self.model.collision.char_is_colliding:
                y_vel = self.VEL
           ##if there is a collision, and the key is pressed, the velocity is zero
            if self.model.lists.collision_rect_is_colliding_list[0] and keys[pygame.K_a]:
                x_vel = 0
            if self.model.lists.collision_rect_is_colliding_list[1] and keys[pygame.K_d]:
                x_vel = 0
            if self.model.lists.collision_rect_is_colliding_list[2] and keys[pygame.K_w]:
                y_vel = 0
            if self.model.lists.collision_rect_is_colliding_list[3] and keys[pygame.K_s]:
                y_vel = 0
            ##for the keys pressed, we can add the velocity to the position
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.model.players[self.model.player_num].rel_x_pos += x_vel
                self.model.move_objects(-x_vel, 0)
                #self.model.players[self.model.player_num].x_pos += x_vel
            if keys[pygame.K_s] or keys[pygame.K_w]:
                self.model.players[self.model.player_num].rel_y_pos += y_vel
                self.model.move_objects(0, -y_vel)
                #self.model.players[self.model.player_num].y_pos += y_vel
            self.move_ticker = 0

            ##if original collides, move outwards
        if self.model.collision.char_is_colliding:
            if self.model.lists.collision_rect_is_colliding_list[0]:
                self.model.move_objects(-1, 0)
                self.model.players[self.model.player_num].rel_x_pos += 1
                #self.model.players[self.model.player_num].x_pos += 1
            if self.model.lists.collision_rect_is_colliding_list[1]:
                self.model.move_objects(1, 0)
                self.model.players[self.model.player_num].rel_x_pos -= 1
                #self.model.players[self.model.player_num].x_pos -= 1
            if self.model.lists.collision_rect_is_colliding_list[2]:
                self.model.move_objects(0, -1)
                self.model.players[self.model.player_num].rel_y_pos += 1
                #self.model.players[self.model.player_num].y_pos += 1
            if self.model.lists.collision_rect_is_colliding_list[3]:
                self.model.move_objects(0, 1)
                self.model.players[self.model.player_num].rel_y_pos -= 1
                #self.model.players[self.model.player_num].y_pos -= 1
        #self.model.players[self.model.player_num].update_relative_positions(rel_x_pos, rel_y_pos)
        self.move_ticker += 1

if __name__ == '__main__':
    pygame.init()

    print 'Enter the server ip address'
    print 'Empty for localhost'
    # ask the server ip address
    #server = raw_input('server ip: ')
    # control if server is empty
    #if server == '':
    #    server = 'localhost'
    #server = '10.7.24.168'
    server = 'localhost'
    # init the listener



    model = EscapeTheMazeClientModel()
    size = (model.WINDOW_WIDTH, model.WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    controller = PyGameKeyboardController(model)
    listener = Listener(model, server, 31500)
    view = PygameEscapeTheMazeView(model, screen, listener)
    running = True
    while running:
        listener.update_listener()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False
        if listener.start:
            model.run_model() ## run the model
            controller.handle_event(event)
        view.draw()