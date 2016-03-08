# Excuse me for the my bad English, I hope you can understand my comments
# pygame site: www.pygame.org

# import pygame
import pygame
# import network modules
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
# random module to randomize the initial ball direction
from random import randint
import random
from Maze_Test import create_maze
#from Escape_the_Maze_backup import *

# function which return a random value between -1 and -3
# or between 1 and 3
# this in userful for set the initial ball direction

class GenerateMaze(object):
    def __init__(self, MAZE_LENGTH, MAZE_HEIGHT):
        self.MAZE_LENGTH = MAZE_LENGTH
        self.MAZE_HEIGHT = MAZE_HEIGHT
        self.MATRIX_CENTERS = 53
        self.maze_matrix = create_maze(self.MAZE_LENGTH, self.MAZE_HEIGHT)

class EscapeTheMazeServerModel(object):
    def __init__(self):
        self.players = [] ##keep empty
        self.number_of_characters = 2   
        self.maze = GenerateMaze(10, 10)
        #locations = GenerateCharacterLocations(self)
        self.char_list = []     ##this list contains a list of attributes for each character (gets sent over network)
        self.char = []          ##this creates characters for the server
        #locations.char_list
        GenerateCharacterLocations(self)


class GenerateCharacterLocations(object):
    def __init__(self, model):
        self.model = model
        self.maze = model.maze
        for i in range(self.model.number_of_characters):
            x = random.randint(1, self.maze.MAZE_LENGTH - 1)
            x_pos = x*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            y = random.randint(1, self.maze.MAZE_HEIGHT - 1)
            y_pos = y*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            char_entity = [x_pos, y_pos, 20, 20]
            self.model.char_list.append(char_entity)
            print char_entity
            char = Character(x_pos, y_pos, 20, 20)
            self.model.char.append(char)
class Character(object):
    """represents the character"""
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rel_x_pos = x_pos
        self.rel_y_pos = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

# class representing a sigle connection with a client
# this can also represent a player

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        # self.Character = None
    
    # function called when a player begin a movement
    def Network_move(self, data):
        self.char.x_pos = data['rel_x_pos']
        self.char.y_pos = data['rel_y_pos']
        # send to all other clients the information about moving
        self._server.SendToAll(data)

# class representing the server
class MyServer(Server):
    channelClass = ClientChannel
    
    # Start the server
    def __init__(self, model, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        
        self.model = model
        # if self.start is True the game is working 
        self.start = False
        # time before strating the game in milliseconds
        self.wait_to_start = -1
        
        #self.characters = (Character(640/2 + 20, 450, 20, 20),Character(640/2 - 20, 450, 20, 20))
        
        # addresss and port at which server is started
        address, port = kwargs['localaddr']
        
        print 'Server started at', address, 'at port', str(port)
        print 'Now you can start the clients'
    
    # function called on every connection
    def Connected(self, player, addr):
        print 'Player connected at', addr[0], 'at port', addr[1]
        
        # add player to the list
        self.model.players.append(player)
        # set the bar rect of the player
        player.char = self.model.char[len(self.model.players)-1]      ##add player.char to players[]
        #player.Char = self.characters[len(self.players)-1]
        # send to the player his number
        player.Send({'action': 'number', 'num': len(self.model.players)-1})
        player.Send({'action': 'generate_maze', 'maze_matrix' : self.model.maze.maze_matrix})
        player.Send({'action': 'generate_players', 'char_list' : self.model.char_list})
        # if there are two player we can start the game
        print len(self.model.players)
        print self.model.number_of_characters
        if len(self.model.players) == 2: #self.model.number_of_characters:
            # send to all players the ready message
            self.SendToAll({'action': 'ready'}) 
            # wait 4 seconds before starting the game
            self.wait_to_start = 300
    
    # send all clients the same data
    def SendToAll(self, data):
        [p.Send(data) for p in self.model.players]
    
    def Loop(self):
        # infinite loop
        while True:
            # update server connection
            myserver.Pump()
            # if the game is started
            # wait 25 milliseconds
            #pygame.time.wait(2)
            # reduce wait to start time if necessary
            if self.wait_to_start > 0:
                self.wait_to_start -= 25
            # if time = 0 start the game
            elif self.wait_to_start == 0:
                self.start = True
                self.wait_to_start = -1
                # send to all player the start message
                self.SendToAll({'action': 'start'})

print 'Enter the ip address of the server. Normally the ip address of the computer.'
print 'example: localhost or 192.168.0.2'
print 'Empty for localhost'
# ip address of the server (normally the ip address of the computer)
#address = raw_input('Server ip: ')

# control if address is empty
#if address == '':
address = 'localhost'
#address = '10.7.24.168'
# inizialize the server
model = EscapeTheMazeServerModel()
myserver = MyServer(model, localaddr=(address, 31500))
# start mainloop
myserver.Loop()