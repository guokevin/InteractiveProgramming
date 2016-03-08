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
        self.char = (Character(550, 550, 20, 20), Character(550, 580, 20, 20))
        self.still_alive = [True, True]
        self.connected_players = 0
        #locations.char_list

"""
class GenerateCharacterLocations(object):
    def __init__(self, model):
        self.model = model
        self.maze = model.maze
        for i in range(self.model.number_of_characters):
            x = random.randint(1, self.maze.MAZE_LENGTH - 1)
            x_pos = x*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            y = random.randint(1, self.maze.MAZE_HEIGHT - 1)
            y_pos = y*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            char = Character(x_pos, y_pos, 20, 20)
            self.model.players.append(char)"""
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

    def Network_alive(self, data):
        player_num = data['player_number']
        self.still_alive[player_num] = data['still_alive']
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

        self.monster = random.randint(0,1)
        self.monster_list = [False, False]
        for i in range(2):
            if i == self.monster:
                self.monster_list[i] = True
        
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
        self.model.connected_players = len(self.model.players)
        # print self.model.connected_players
        player.char = self.model.char[len(self.model.players)-1]      ##add player.char to players[]
        player.still_alive = self.model.still_alive
        # send to the player his number
        player.Send({'action': 'number', 'num': len(self.model.players)-1})
        player.Send({'action': 'monster_number', 'monster_num': self.monster})
        player.Send({'action': 'is_monster', 'monster': self.monster_list})  
        player.Send({'action': 'generate_maze', 'maze_matrix' : self.model.maze.maze_matrix})

        self.SendToAll({'action': 'ready_players', 'connected_players': self.model.connected_players})
        if len(self.model.players) == 2: #self.model.number_of_characters:
            # send to all players the ready message
            self.SendToAll({'action': 'monster_list'})
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