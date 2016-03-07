# import pygame
import pygame
# import network module
from PodSixNet.Connection import connection, ConnectionListener
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
import math
from random import choice
import random
# from Maze_Escape import *
#from Escape_the_Maze_backup import *

# init pygame

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
            self.screen.fill(pygame.Color('grey'))
            for char in self.model.players:
                pygame.draw.rect(self.screen, pygame.Color(char.color), char.rect)

            pygame.display.update()
        else:
            self.screen.fill((0, 0, 0))

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model
        self.move_ticker = 0
        self.REFRESH_RATE = 0 #how many loops before it updates the velocity
        self.DIAG_VEL = self.model.players[self.model.player_num].DIAG_VEL
        self.VEL = self.model.players[self.model.player_num].VEL
        #self.players = self.model.players  #set attributes of players
        #self.collision = self.model.collision
        #self.lists = self.model.lists
    def handle_event(self, event):
        y_vel = 0
        x_vel = 0
        keys = pygame.key.get_pressed()     ##find what keys were pressed
        #self.model.run_model() ## run the model so we can change its attributes
        if self.move_ticker >= self.REFRESH_RATE:
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
            if keys[pygame.K_a]:
                x_vel = -self.VEL
            elif keys[pygame.K_d]:
                x_vel = self.VEL
            elif keys[pygame.K_w]:
                y_vel = -self.VEL
            elif keys[pygame.K_s]:
                y_vel = self.VEL
           
            if keys[pygame.K_a] or keys[pygame.K_d]:
                #self.character.rel_x_pos += x_vel
                #self.model.move_objects(-x_vel, 0)
                self.model.players[self.model.player_num].x_pos += x_vel
            if keys[pygame.K_s] or keys[pygame.K_w]:
                #self.character.rel_y_pos += y_vel
                #self.model.move_objects(0, -y_vel)
                self.model.players[self.model.player_num].y_pos += y_vel
            self.move_ticker = 0
        self.move_ticker += 1

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
        self.VEL = 2           #how many pixels it updates
        self.DIAG_VEL = 2/1.4
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
    def update_relative_positions(rel_x_pos, rel_y_pos):
        self.rel_x_pos = rel_x_pos
        self.rel_y_pos = rel_y_pos

class EscapeTheMazeModel(object):
    def __init__(self):
        self.players = (Character(640/2 + 20, 450, 20, 20), Character(640/2 - 20, 450, 20, 20))
        self.player_num = 1
    def run_model(self):
        self.update_character()

    def update_character(self):
        for char in self.players:
            char.rect.left = char.x_pos
            char.rect.top = char.y_pos
# class for I/O on network
# this represent the player, too
class Listener(ConnectionListener): 
    # init the player
    def __init__(self, model, host, port):
        self.Connect((host, port))
        self.model = model
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

        #self.x_pos = [0,0]
        #self.y_pos = [0,0]
    # function to manage bars movement
    def Network_move(self, data):
        if data['player'] != self.model.player_num:
            self.model.players[data['player']].x_pos = data['x']
            self.model.players[data['player']].y_pos = data['y']

        
    # get the player number
    def Network_number(self, data):
        self.model.player_num = data['num']
    
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
                # if the game is started
            """
                y_vel = 0
                x_vel = 0
                keys = pygame.key.get_pressed()     ##find what keys were pressed
                #self.model.run_model() ## run the model so we can change its attributes
                if self.move_ticker > self.refresh_rate:
                    ## change diagonals first
                    if keys[pygame.K_a] and keys[pygame.K_s]:
                        x_vel = -self.diag_vel
                        y_vel = self.diag_vel
                    elif keys[pygame.K_a] and keys[pygame.K_w]:
                        x_vel = -self.diag_vel
                        y_vel = -self.diag_vel
                    elif keys[pygame.K_d] and keys[pygame.K_s]:
                        x_vel = self.diag_vel
                        y_vel = self.diag_vel
                    elif keys[pygame.K_d] and keys[pygame.K_w]:
                        x_vel = self.diag_vel
                        y_vel = -self.diag_vel
                    ##check horizontal/vertical after
                    if keys[pygame.K_a]:
                        x_vel = -self.vel
                    elif keys[pygame.K_d]:
                        x_vel = self.vel
                    elif keys[pygame.K_w]:
                        y_vel = -self.vel
                    elif keys[pygame.K_s]:
                        y_vel = self.vel
                   
                    if keys[pygame.K_a] or keys[pygame.K_d]:
                        #self.character.rel_x_pos += x_vel
                        #self.model.move_objects(-x_vel, 0)
                        self.players[self.num].x_pos += x_vel
                    if keys[pygame.K_s] or keys[pygame.K_w]:
                        #self.character.rel_y_pos += y_vel
                        #self.model.move_objects(0, -y_vel)
                        self.players[self.num].y_pos += y_vel
                    self.move_ticker = 0
                self.move_ticker += 1"""
               
            
            # clear the screen            
            # if game is working
            if self.start:
                """n = 0
                for move in self.x_pos:
                    self.players[n].x_pos += move
                    n += 1

                n = 0
                for move in self.y_pos:
                    self.players[n].y_pos += move
                    n += 1"""
                
                # send to the server information about movement
                connection.Send({'action': 'move', 'player': self.model.player_num, 'x': self.model.players[self.model.player_num].x_pos, 'y': self.model.players[self.model.player_num].y_pos})
                
            
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

if __name__ == '__main__':
    pygame.init()

    print 'Enter the server ip address'
    print 'Empty for localhost'
    # ask the server ip address
    #server = raw_input('server ip: ')
    # control if server is empty
    #if server == '':
    #    server = 'localhost'
    server = '10.7.64.56'
    #server = 'localhost'
    # init the listener


    size = (1250, 1250)
    screen = pygame.display.set_mode(size)
    model = EscapeTheMazeModel()
    controller = PyGameKeyboardController(model)
    listener = Listener(model, server, 31500)
    view = PygameEscapeTheMazeView(model, screen, listener)
    running = True
    while running:
        model.run_model() ## run the model
        listener.update_listener()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False
        controller.handle_event(event)
        view.draw()