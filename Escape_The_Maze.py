import pygame
# import network module
from PodSixNet.Connection import connection, ConnectionListener
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import sys
import math
from random import choice
import random
from pygame.locals import *

pygame.init()
##import sounds 
pygame.mixer.init(frequency=22050,size=-16,channels=4)
amnesia_sound = pygame.mixer.Sound('Amnesia_Theme.ogg')
illuminati_sound = pygame.mixer.Sound('Illuminati_Sound.ogg')
underground_sound = pygame.mixer.Sound('Underground_Theme.ogg')
sewers_sound = pygame.mixer.Sound('Sewers_Theme.ogg')
scroll_sound = pygame.mixer.Sound('Scroll_Collect.ogg')
connect_sound = pygame.mixer.Sound('Connect_Sound.ogg')
dying_sound = pygame.mixer.Sound('Dying_Sound.ogg')
class PygameEscapeTheMazeView(object):
    def __init__(self, model, screen, listener):
        """Initialize the view with the specified model"""
        self.model = model
        self.screen = screen
        self.listener = listener
        self.font1 = pygame.font.SysFont('purisa', 30, True)
        self.font2 = pygame.font.SysFont('sans,freesans,courier,arial', 48, True)
        self.font4 = pygame.font.SysFont('sans,freesans,courier,arial', 100, True)
        self.font3 = pygame.font.SysFont('purisa', 70, True)
        self.font5 = pygame.font.SysFont('sans,freesans,courier,arial', 44, True)
        self.font6 = pygame.font.SysFont('purisa', 28, True)
        self.altar_revealed = False
        self.ticker = 0
        self.played = False
        self.win_ticker = 0
        self.fog_ticker = 0
        self.lose_ticker = 0
        self.played1 = False

    def draw(self):
        if self.listener.start and self.ticker > 30:
            ## if the actual game has started background is grey
            self.screen.fill(pygame.Color('grey'))
            #is_monster = self.model.monster_num == self.model.player_num
            ##create the mazes for the rectangle
            for rect in self.model.lists.maze_segment_rect_list:
                pygame.draw.rect(self.screen, pygame.Color('black'), rect)

            ##if you are in a certain distance of the exit
            dist = self.model.cartesian_dist()
            if self.altar_revealed and not self.model.is_monster:
                altar_color = (pygame.Color('black'))
                pygame.draw.rect(self.screen, altar_color, self.model.exit.rect)
                self.altar_revealed = True
            elif not self.model.is_monster:
                if dist < 200:
                    altar_color = ((192.0/200)*dist,(192.0/200)*dist,(192.0/200)*dist)
                    ##draw the exit
                    pygame.draw.rect(self.screen, altar_color, self.model.exit.rect)
            ##play the sound if you are close
            if dist < 50 and not self.altar_revealed and not self.model.is_monster:
                self.altar_revealed = True
                illuminati_sound.play() 

            ##draw all the scrolls and borders
            for i, scroll in enumerate(self.model.lists.scroll_list):
                if scroll.is_visible:
                    rect = pygame.Rect(scroll.border_x_pos, scroll.border_y_pos, scroll.border_width, scroll.border_height)
                    pygame.draw.rect(self.screen, pygame.Color('black'), rect)
                    rect = pygame.Rect(scroll.x_pos, scroll.y_pos, scroll.width, scroll.height)
                    pygame.draw.rect(self.screen, pygame.Color('gold'), rect)

                    rect = pygame.Rect(scroll.border_nub_x_pos, scroll.border_nub2_y_pos, scroll.border_nub_size, scroll.border_nub_size)
                    pygame.draw.rect(self.screen, pygame.Color('black'), rect)
                    rect = pygame.Rect(scroll.border_nub_x_pos, scroll.border_nub1_y_pos, scroll.border_nub_size, scroll.border_nub_size)
                    pygame.draw.rect(self.screen, pygame.Color('black'), rect)

                    rect = pygame.Rect(scroll.nub_x_pos, scroll.nub2_y_pos, scroll.nub_size, scroll.nub_size)
                    pygame.draw.rect(self.screen, pygame.Color('white'), rect)
                    rect = pygame.Rect(scroll.nub_x_pos, scroll.nub1_y_pos, scroll.nub_size, scroll.nub_size)
                    pygame.draw.rect(self.screen, pygame.Color('white'), rect)

            ##draw all the characters
            for char in self.model.players:
                #if self.model.players[self.model.player_num].still_alive:
                if char.still_alive and not char.win:
                    pygame.draw.rect(self.screen, pygame.Color(char.color), char.rect)
            
            ##collision Rectangles
            #for rect in self.model.lists.collision_rect_list:
            #    pygame.draw.rect(self.screen, pygame.Color('green'), rect)

            ##create fog of war
            if not self.model.spectator:
                self.fog_ticker += 1
                self.model.fog_of_war.draw_fog_of_war(self.screen, self.model.is_monster, self.fog_ticker)
           
            ##draw the scroll hud
            scrolls_collected = self.model.lists.total_number_of_scrolls - self.model.lists.number_of_scrolls
            if self.model.lists.total_number_of_scrolls > 10:
                scrolls_total = 10
            else:
                scrolls_total = self.model.lists.total_number_of_scrolls
            if scrolls_collected > scrolls_total:
                scrolls_collected = scrolls_total
            if scrolls_collected < 0:
                scrolls_collected = 0

            if scrolls_collected == scrolls_total and self.model.monster_num != self.model.player_num and not self.model.spectator:
                self.screen.blit(self.font1.render("All Scrolls Have Been found!", True, (255,0,0)), (350, 700))
                self.screen.blit(self.font1.render("GET TO THE ALTAR BEFORE HE EATS YOU!", True, (255,0,0)), (350, 750))

            for i in range(scrolls_collected):
                pygame.draw.rect(self.screen, pygame.Color('white'), (20*i + 10, 10, 15, 15))
            self.screen.blit(self.font1.render(str(scrolls_collected) + '/' + str(scrolls_total) + 'Scrolls Collected', True, pygame.Color('blue')), (220, 6) )

            if self.model.monster_num == self.model.player_num:
                self.screen.blit(self.font1.render("You Thirst for blood!", True, (0,0,0)), (460, 50))

            if self.model.player_num != self.model.monster_num and not self.model.spectator:
                if (scrolls_collected == scrolls_total and self.model.exit_collision) and not self.model.spectator:
                    self.model.players[self.model.player_num].win = True
                    self.model.win_screen = True
                elif self.model.exit_collision:
                    self.screen.blit(self.font1.render("The Altar is still locked", True, (255,255,255)), (400, 700))
                elif not self.model.spectator:
                    self.win_ticker = 0
            if not self.model.players[self.model.player_num].still_alive:
                self.model.lose_screen = True

            if self.model.lose_screen:
                if self.lose_ticker < 200:
                    self.screen.fill((255,0,0))
                    self.screen.blit(self.font2.render("YOU GOT EATEN", True, (0,0,0)), (460, 500))
                    self.lose_ticker += 1
                else:
                    self.model.spectator = True
                    self.model.lose_screen = False

            if self.model.win_screen:
                if self.win_ticker < 200:
                    self.screen.fill(pygame.Color('black'))
                    self.screen.blit(self.font2.render("You have escaped!", True, (0, 0, 255)), (300, 500))
                    self.win_ticker += 1
                else:
                    self.model.spectator = True
                    self.model.win_screen = False
            if self.model.spectator:
                self.screen.blit(self.font2.render("Spectator", True, (0, 0, 255)), (400, 100))

            if self.model.is_monster and self.model.alive_players == 1:
                self.screen.fill(pygame.Color('black'))
                self.screen.blit(self.font2.render("You have killed all the imbeciles!", True, (255, 0, 0)), (250, 500))
            elif self.model.is_monster and (self.model.alive_players - self.model.won_players == 1):
                self.screen.fill(pygame.Color('black'))
                self.screen.blit(self.font2.render("You killed " + str(len(self.model.players) - self.model.won_players -1) + " players", True, (255, 0, 0)), (400, 450))
            if self.model.is_monster and len(self.model.players) - self.model.won_players == 1:
                self.screen.fill(pygame.Color('black'))
                self.screen.blit(self.font2.render("You have failed!", True, (255, 0, 0)), (400, 450))
                self.screen.blit(self.font2.render("You haven't killed a single person!", True, (255, 0, 0)), (250, 500))

            self.model.check_game()
            pygame.display.update()
        elif self.ticker < 31:
            self.ticker += 1

    def draw_lobby(self):
        """draw lobby before the game starts"""
        self.screen.fill(pygame.Color('black'))
        for i in range(self.model.connected_players):
            if len(self.model.is_players_ready) != 0:
                if self.model.is_players_ready[i]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (100*i + 300, 450, 70, 70))
                else:
                    if i == self.model.monster_num:
                        pygame.draw.rect(self.screen, pygame.Color('red'), (100*i + 300, 450, 70, 70))
                    else:                    
                        pygame.draw.rect(self.screen, pygame.Color('blue'), (100*i + 300, 450, 70, 70))
                if self.model.player_ready:
                    self.screen.blit(self.font1.render('Waiting for Other Players', True, (0, 255, 0)), (400, 700))
                else:
                    self.screen.blit(self.font1.render('Press SpaceBar to Ready', True, (255, 0, 0)), (400, 700))
        self.screen.blit(self.font3.render('ESCAPE THE MAZE', True, (255, 255, 255)), (200, 100))
        pygame.display.update()

    def draw_load_screen(self):
        """draws the screen before entering the story screen"""
        if not self.played:
            self.ticker = 0
            self.played = True
        self.screen.fill(pygame.Color('black'))
        for i in range(self.model.connected_players):
            if self.model.is_players_ready[i]:
                pygame.draw.rect(self.screen, pygame.Color('green'), (100*i + 300, 450, 70, 70))
        self.screen.blit(self.font3.render('ESCAPE THE MAZE', True, (255, 255, 255)), (200, 100))
        if self.ticker > 600:
            self.screen.blit(self.font4.render('0', True, (255, 255, 255)), (550, 700))
        elif self.ticker > 400:
            self.screen.blit(self.font4.render('1', True, (255, 255, 255)), (550, 700))
        elif self.ticker > 200:          
            self.screen.blit(self.font4.render('2', True, (255, 255, 255)), (550, 700))
        elif self.ticker < 200:
            self.screen.blit(self.font4.render('3', True, (255, 255, 255)), (550, 700))

        if (self.ticker < 10) or (self.ticker > 200 and self.ticker < 210) or (self.ticker > 400 and self.ticker < 410) or (self.ticker > 600 and self.ticker < 610):
            connect_sound.play()

        pygame.display.update()
        self.ticker += 1

    def draw_story(self):
        """draws the story and instructions before beginning the game"""
        self.screen.fill((0,0,0))
        if self.model.player_num == self.model.monster_num:
            self.screen.blit(self.font6.render('You have been trapped in a maze and mutated into a monster.', True, (255, 255, 255)), (10, 200))
            self.screen.blit(self.font6.render('Kill your companions before they escape.', True, (255, 255, 255)), (175, 275))

        else:
            self.screen.blit(self.font6.render('You have been trapped in a maze', True, (255, 255, 255)), (235, 200))
            self.screen.blit(self.font6.render('One of your companions starts going insane.', True, (255, 255, 255)), (145, 250))
            self.screen.blit(self.font6.render('Escape before he kills you.', True, (255, 255, 255)), (300, 325))

        self.screen.blit(self.font6.render('Move with:', True, (255,255,255)), (460, 550))
        pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(519,690,50,50))
        pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(459,750,50,50))
        pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(519,750,50,50))
        pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(579,750,50,50))
        self.screen.blit(self.font5.render('W', True, (0, 0, 0)), (524, 690))
        self.screen.blit(self.font2.render('A  S  D', True, (0, 0, 0)), (467, 747))

        pygame.display.update()


class FogOfWar(object):
    """Class creates fog around the character"""
    def __init__(self, character, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.character = character
    def update_fog_of_war(self):
        self.x_pos = self.character.x_pos + self.character.width/2
        self.y_pos = self.character.y_pos + self.character.height/2
    def draw_fog_of_war(self, screen, is_monster, time):
        if is_monster:  ##if you are the monster, fog of war expands over time
            radius = 200 + time**2/300000
            circle_radius = 80 + time/100
            color = 'red'
        else:
            color = 'black'
            radius = 300
            circle_radius = 80

        left_rect = pygame.Rect(0, 0, self.x_pos - radius, 1100)
        right_rect = pygame.Rect(self.x_pos + radius, 0, 1100, 1100)
        bottom_rect = pygame.Rect(0, self.y_pos + radius, 1100, 1100)
        top_rect = pygame.Rect(0, 0, 1100,  self.y_pos - radius)
        pygame.draw.rect(screen, pygame.Color(color), left_rect)
        pygame.draw.rect(screen, pygame.Color(color), right_rect)
        pygame.draw.rect(screen, pygame.Color(color), bottom_rect)
        pygame.draw.rect(screen, pygame.Color(color), top_rect)
        for i in range(70):
            ang = i * math.pi * 2.0 / 70
            dx = int(math.cos(ang) * (radius + 80))
            dy = int(math.sin(ang) * (radius + 80))
            x = self.x_pos + dx
            y = self.y_pos + dy
            pygame.draw.circle(screen, 
                            pygame.Color(color), 
                            (int(x), int(y)), 
                            circle_radius)

class Maze(object):
    def __init__(self):
        """Initializes all attributes necessary to create a maze"""
        self.maze_segment_list = []
        self.WALL_WIDTH = 4
        self.MARGIN = 0
        self.WALL_LENGTH = 48 + self.WALL_WIDTH
        self.MATRIX_CENTERS = 53*2
        self.isolated_direction = 'yes'
        self.maze_matrix = []
        self.row_length = None
        self.column_length = None
        #self.maze_segment = Maze_Segment(0, 0, 0, 0)

class Maze_Segment(object):
    def __init__(self, x_pos, y_pos, width, height):
        """holds the attributes for the maze"""
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

class Scroll(object):
    def __init__(self, x_pos, y_pos, width, height, is_visible):
        """holds the attributes for the scroll"""
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.BORDER_MARGIN = 2
        self.width = width
        self.height = height
        self.border_x_pos = self.x_pos - self.BORDER_MARGIN
        self.border_y_pos = self.y_pos - self.BORDER_MARGIN
        self.border_width = self.width + self.BORDER_MARGIN*2
        self.border_height = self.height + self.BORDER_MARGIN*2
        self.nub_size = 6
        self.NUB_MARGIN = 2
        self.nub_x_pos = self.x_pos + (self.width - self.nub_size)/2
        self.nub1_y_pos = self.y_pos - self.nub_size - self.NUB_MARGIN
        self.nub2_y_pos = self.y_pos + self.height + self.NUB_MARGIN
        self.border_nub_x_pos = self.nub_x_pos - self.NUB_MARGIN
        self.border_nub1_y_pos = self.nub1_y_pos - self.NUB_MARGIN
        self.border_nub2_y_pos = self.nub2_y_pos - self.NUB_MARGIN
        self.border_nub_size = self.nub_size + self.NUB_MARGIN*2
        self.is_visible = is_visible

class Exit(object):
    def __init__(self, x_pos, y_pos):
        """attributes for the exit"""
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = 60
        self.height = 60
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
        self.color = "blue"
        self.VEL = 3           #how many pixels it updates
        self.DIAG_VEL = 3/1.4
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.monster = False
        self.still_alive = True
        self.win = False
        self.center = self.update_center()

    def update_center(self):
        return [self.x_pos - self.width/2, self.y_pos - self.height/2]

    def update_relative_positions(rel_x_pos, rel_y_pos):
        """updates the relative position of the character"""
        self.rel_x_pos = rel_x_pos
        self.rel_y_pos = rel_y_pos

class Lists():
    def __init__(self, character, collision, maze):
        """lists has a bunch of lists of different attributes, (collision, scrolls, etc.)"""
        self.character = character
        self.collision = collision
        self.maze = maze
        self.maze_segment_list = [] ##create a list of objects for the maze segments
        self.maze_segment_rect_list = []    ##create rectangles to go in the list
        self.collision_rect_list = [0,0,0,0]       ##create 4 rectangles to place around the character
        self.collision_rect_is_colliding_list = [False, False, False, False]  ##create 4 bools to see if the rectangles colide with the maze
        self.scroll_is_colliding_list = [0,0,0,0]
        self.scroll_rect_list = []
        self.number_of_scrolls = 0
        self.total_number_of_scrolls = 0
        self.scroll_list = []
        ####################################
        ##GERENATE MAZE SEGMENT RECTANGLES##
        ####################################
        ###create rectangles for the maze to draw
        for i in range(self.maze.row_length):  ##for each of the rows
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

    def update_collision_rect_list(self, is_monster):
        """updates the collision rectangles into a list"""
        if is_monster:  ##if you are the monster, your collision rectangles are bigger
            collision_rect = CollisionRectangle(0, 0, 3, 60)   
        else:
            collision_rect = CollisionRectangle(0, 0, 3, self.character.width)
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
        for i, collision_rect in enumerate(self.collision_rect_list):
            self.collision_rect_is_colliding_list[i] = self.collision.return_collision_bool(collision_rect, 
                                                                                            self.maze_segment_rect_list)

class CollisionRectangle(object):
    """defines the collision rectangle"""
    def __init__(self, x_pos, y_pos, width = 2, height = 40):
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
    """CREATE MODEL FOR CLIENT"""
    def __init__(self):
        self.WINDOW_WIDTH = 1100
        self.WINDOW_HEIGHT = 1100
        self.players = []
        self.collision = None
        self.player_num = 0
        self.maze = Maze()
        self.lists = None ##initiate lists object
        self.char_list = None
        self.scroll_entity_list = []
        self.scroll_collision_index = -1
        self.temp_scroll_collision_index = -1
        self.scroll_removed = True
        self.fog_of_war = None
        self.exit = None
        self.connected_players = 0
        self.ticker = 0
        self.player_ready = False
        self.is_players_ready = []
        self.win_screen = False
        self.spectator = False
        self.run_once = False
        self.lose_screen = False
        self.alive_players = -1
        self.won_players = -1
        self.is_monster = -1
    def run_model(self):
        self.fog_of_war.update_fog_of_war()

    def update_monster(self):
        if self.ticker >20:
            self.is_monster = (self.monster_num == self.player_num)
            ##if you collide with the monster, still_alive = false
            if self.players[self.player_num].rect.colliderect(self.monster.rect) and self.player_num != self.monster_num and not self.spectator and not self.win_screen:
                self.players[self.player_num].still_alive = False
                if not self.run_once:
                    pygame.mixer.stop()
                    dying_sound.play()
                    self.run_once = True
        if self.ticker < 21:
            self.ticker += 1

    def update_exit_collision(self):
        self.exit_collision = self.players[self.player_num].rect.colliderect(self.exit.rect) == 1

    def update_characters(self):
        for char in self.players:
            char.rect.left = char.x_pos
            char.rect.top = char.y_pos

    def update_entities(self):
        ##updates all the things
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

    def update_scrolls(self):
        """if you hit a scroll, set its visibility to false, and send the index of the scroll to the other players"""
        if self.player_num != self.monster_num  and not self.spectator:
            self.scroll_collision_index = self.players[self.player_num].rect.collidelist(self.lists.scroll_rect_list)
        if self.temp_scroll_collision_index != -1:
            if(self.lists.scroll_list[self.temp_scroll_collision_index].is_visible):
                scroll_sound.play()
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
        """moves the maze when hitting wasd"""
        for maze_segment in self.lists.maze_segment_list:
            maze_segment.x_pos += x_vel
            maze_segment.y_pos += y_vel

    def move_scrolls(self, x_vel, y_vel):
        """moves scrolls relative to player"""
        for scroll in self.lists.scroll_list:
            scroll.x_pos += x_vel
            scroll.y_pos += y_vel
            scroll.border_x_pos += x_vel
            scroll.border_y_pos += y_vel
            scroll.nub_x_pos += x_vel
            scroll.nub1_y_pos += y_vel
            scroll.nub2_y_pos += y_vel
            scroll.border_nub1_y_pos += y_vel
            scroll.border_nub2_y_pos += y_vel
            scroll.border_nub_x_pos +=x_vel

    def move_exit(self, x_vel, y_vel):
        """moves exit relative to player"""
        self.exit.x_pos += x_vel
        self.exit.y_pos += y_vel

    def move_objects(self, x_vel, y_vel):
        """moves scroll, exit, and maze together"""
        self.move_maze(x_vel, y_vel)
        self.move_scrolls(x_vel, y_vel)
        self.move_exit(x_vel,y_vel)

    def edit_maze_position(self):
        """initializes the position of the maze to be relative to the character"""
          ##this is run once on initilization
        for maze_segment in self.lists.maze_segment_list:
            maze_segment.x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
            maze_segment.y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos

    def edit_scroll_position(self):
        """initializes the position of the scrolls to be relative to the character"""
        for scroll in self.lists.scroll_list:
            scroll.x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
            scroll.y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos
            scroll.border_x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
            scroll.border_y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos

            scroll.nub_x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
            scroll.nub1_y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos
            scroll.nub2_y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos
            scroll.border_nub1_y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos
            scroll.border_nub2_y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos
            scroll.border_nub_x_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_x_pos

    def edit_exit_position(self):
        """initializes the position of the exit to be relative to the character"""
        self.exit.x_pos += self.WINDOW_WIDTH/2 - self.players[self.player_num].rel_x_pos
        self.exit.y_pos += self.WINDOW_HEIGHT/2 - self.players[self.player_num].rel_y_pos

    def create_fog_of_war(self):
        """creates fog of war"""
        self.fog_of_war = FogOfWar(self.players[self.player_num],         ##create fog of war
                            self.players[self.player_num].x_pos, 
                            self.players[self.player_num].x_pos, 100)

    def create_players(self):
        """creates a character"""
        for char_entity in self.char_list:
            ##create a new character in players for each entity in char_list
            new_char = Character(self.WINDOW_WIDTH/2, 
                                self.WINDOW_HEIGHT/2, 
                                char_entity[0], 
                                char_entity[1],
                                40, 
                                40)
            self.monster_num = char_entity[2]
            self.players.append(new_char)
            ##turns character entities into a Character to add to player

    def cartesian_dist(self):
        """creates a distance between the player and exit"""
        return math.sqrt((self.players[self.player_num].update_center()[0] - self.exit.update_center()[0])**2 +
                        (self.players[self.player_num].update_center()[1] - self.exit.update_center()[1])**2)

    def create_scrolls(self, scroll_entity_list):
        """edits the scroll_list based off of server input"""
        for scroll_entity in scroll_entity_list:
            ##create a new scroll in scroll_list for each entity in the list
            self.lists.scroll_list.append(Scroll(scroll_entity[0], scroll_entity[1], 10, 25, True))  ##adds a scroll into scroll_list, with width 7, height 20
        self.lists.total_number_of_scrolls = len(self.lists.scroll_list)
        self.lists.number_of_scrolls = len(self.lists.scroll_list)

    def create_scroll_is_visible(self):
        """Initializes the scroll_is_visible list to be true"""
        self.scroll_is_visible = []
        for i in range(self.lists.number_of_scrolls):
            self.scroll_is_visible.append(True)

    def check_game(self):
        """checks the number of players alive"""
        self.alive_players = 0
        for character in self.players:
            if character.still_alive:
                self.alive_players += 1
        self.won_players = 0
        for character in self.players:
            if character.win:
                self.won_players += 1

    def create_monster(self):
        self.players[self.monster_num].width = self.players[self.monster_num].width*1.5
        self.players[self.monster_num].height = self.players[self.monster_num].height*1.5
        self.players[self.monster_num].color = "red"
        self.players[self.monster_num].rect = pygame.Rect(self.players[self.monster_num].x_pos,
                                                                    self.players[self.monster_num].y_pos,
                                                                    self.players[self.monster_num].width,
                                                                    self.players[self.monster_num].height)
        self.monster = self.players[self.monster_num]

# class for I/O on network
# this represent the player, too
class Listener(ConnectionListener): 
    # init the player
    def __init__(self, model, host, port):
        self.Connect((host, port))
        self.model = model
        self.ran_initiations = False
        # True if the server sended the ready message
        self.ready = False
        self.load_screen = False
        self.story = False
        # True if the game is working
        self.start = False
        self.running = True
        self.spectator = True
        # font for writing the scores
        self.font = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)
        self.played2 = False
        self.played3 = False

    # function to manage character movement
    def Network_move(self, data):
        if data['player_number'] != self.model.player_num:
            self.model.players[data['player_number']].x_pos = 550 - self.model.players[self.model.player_num].rel_x_pos + data['rel_x_pos']
            self.model.players[data['player_number']].y_pos = 550 - self.model.players[self.model.player_num].rel_y_pos + data['rel_y_pos']

    def Network_generate_maze(self, data):
        self.model.maze.maze_matrix = data['maze_matrix']
        self.model.maze.row_length = len(self.model.maze.maze_matrix)
        self.model.maze.column_length = len(self.model.maze.maze_matrix[0][:])

    # get the player number
    def Network_number(self, data):
        self.model.player_num = data['num']
    def Network_initialize_entities(self, data):
        #self.model.test = data['char_list']
        self.model.char_list = data['char_list']
        self.model.scroll_entity_list = data['scroll_list']
        self.model.create_players()
        self.model.create_fog_of_war()

    def Network_exit_location(self,data):
        exit_location = data['exit']
        self.model.exit = Exit(exit_location[0],exit_location[1])

    def Network_update_win(self, data):
        self.model.players[data['player_number']].win = data['won']

    def Network_update_entities(self, data):
        #if data['player_number'] != self.model.player_num:
        self.model.temp_scroll_collision_index = data['scroll_collision_index']

    def Network_update_alive(self, data):
        self.model.players[data['player_number']].still_alive = data['still_alive']
    
    # def Network_monster_number(self,data):
    #     self.model.monster_num = data['monster_num']
    def Network_ready_players(self, data):
        self.model.connected_players = data['connected_players']
        self.model.is_players_ready = []
        for i in range(self.model.connected_players):
            self.model.is_players_ready.append(False)

    def Network_lobby(self, data):
        #self.model.connected_players = data['connected_players']   
        player_ready = data['p_ready']
        self.model.is_players_ready[data['player_number']] = player_ready

    def Network_update_condition(self, data):
        self.story = data['story']
        self.load_screen = data['ready']
        self.start = data['start']

    # if the game is ready
    def Network_ready(self, data):
        self.load_screen = True

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
                self.ready = False
                if not self.ran_initiations:
                    sound_int = random.randint(0,2)
                    if sound_int == 0:
                        amnesia_sound.play(-1)
                    if sound_int == 1:
                        underground_sound.play(-1)
                    if sound_int == 2:
                        sewers_sound.play(-1)
                    self.model.collision = CollisionDetection(self.model.players[self.model.player_num], self.model)
                    self.model.lists = Lists(self.model.players[self.model.player_num], self.model.collision, self.model.maze)
                    self.model.create_scrolls(self.model.scroll_entity_list)
                    self.model.edit_maze_position()
                    self.model.edit_scroll_position()
                    self.model.edit_exit_position()
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
                self.model.lists.update_collision_rect_list(self.model.player_num == self.model.monster_num)
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

                if not self.model.players[self.model.player_num].still_alive: #and not self.played2:
                    connection.Send({'action': 'update_alive', 
                                    'player_number': self.model.player_num,
                                    'still_alive': False})
                    self.played2 = True
                if self.model.players[self.model.player_num].win and not self.played3:
                    connection.Send({'action': 'update_win', 
                                    'player_number': self.model.player_num,
                                    'won': True})
                    self.played3 = True
            else:
                connection.Send({'action': 'lobby', 
                                'player_number': self.model.player_num, 
                                'p_ready': self.model.player_ready,
                                'is_players_ready': self.model.is_players_ready})        ##this part for server
    

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
        self.move_ticker = 0
        self.REFRESH_RATE = 0 #how many loops before it updates the velocity
        self.DIAG_VEL = 6/1.4
        self.VEL = 6
        self.pressed = False
    def handle_event(self, event):
        if self.model.spectator:
            self.DIAG_VEL = 9/1.4
            self.VEL = 9

        y_vel = 0
        x_vel = 0
        keys = pygame.key.get_pressed()     ##find what keys were pressed
        #self.model.run_model() ## run the model so we can change its attributes
        if self.move_ticker > self.REFRESH_RATE and not self.model.win_screen:
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
            elif keys[pygame.K_a] and (not self.model.collision.char_is_colliding or self.model.spectator):
                x_vel = -self.VEL
            elif keys[pygame.K_d] and (not self.model.collision.char_is_colliding or self.model.spectator):
                x_vel = self.VEL
            elif keys[pygame.K_w] and (not self.model.collision.char_is_colliding or self.model.spectator):
                y_vel = -self.VEL
            elif keys[pygame.K_s] and (not self.model.collision.char_is_colliding or self.model.spectator):
                y_vel = self.VEL
           ##if there is a collision, and the key is pressed, the velocity is zero
            if (self.model.lists.collision_rect_is_colliding_list[0] and not self.model.spectator) and keys[pygame.K_a]:
                x_vel = 0
            if (self.model.lists.collision_rect_is_colliding_list[1] and not self.model.spectator) and keys[pygame.K_d]:
                x_vel = 0
            if (self.model.lists.collision_rect_is_colliding_list[2] and not self.model.spectator) and keys[pygame.K_w]:
                y_vel = 0
            if (self.model.lists.collision_rect_is_colliding_list[3] and not self.model.spectator) and keys[pygame.K_s]:
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
        if self.model.collision.char_is_colliding and not self.model.spectator:
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

    def handle_lobby_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE  and not self.pressed:     ##if space is pressed,
                self.model.player_ready = not self.model.player_ready   ##ready is swapped (false- true, true- false)
                self.pressed = True
        else:
            self.pressed = False

if __name__ == '__main__':
    pygame.init()

    print 'Enter the server ip address'
    print 'Empty for localhost'
    #ask the server ip addresss
    server = raw_input('server ip: ')
    # control if server is empty
    if server == '':
        server = 'localhost'
    #server = '10.7.64.193'
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
        elif listener.load_screen:
            controller.handle_lobby_event(event)
            view.draw_load_screen()
            for boolean in model.is_players_ready:
                if boolean == False:
                    view.played = False
                    view.ticker = 0
                    listener.load_screen = False
        elif listener.story:
            view.draw_story()
        else:
            controller.handle_lobby_event(event)
            view.draw_lobby()