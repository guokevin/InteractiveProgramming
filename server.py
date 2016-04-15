import pygame
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from random import randint
import random
from Maze import create_maze
import time


class Time(object):
    def __init__(self):
        self.start_time = 0
        self.time_elapsed = 0
        self.time_started = False
    def reset_timer(self):
        if not self.time_started:
            self.start_time = int(time.clock()*1000)
            self.time_started = True
    def current_time(self):
        return int(time.clock()*1000) - self.start_time
    def reset_timer_bool(self):
        self.time_started = False

class GenerateMaze(object):
    def __init__(self, MAZE_LENGTH, MAZE_HEIGHT):
        self.MAZE_LENGTH = MAZE_LENGTH
        self.MAZE_HEIGHT = MAZE_HEIGHT
        self.MATRIX_CENTERS = 53*2
        self.maze_matrix = create_maze(self.MAZE_LENGTH, self.MAZE_HEIGHT)

class EscapeTheMazeServerModel(object):
    """Model"""
    def __init__(self, number_of_players):
        self.players = [] ##keep empty
        self.NUMBER_OF_CHARACTERS = number_of_players
        self.NUMBER_OF_SCROLLS = 1
        self.MAZE_SIZE = 2
        self.maze = GenerateMaze(self.MAZE_SIZE, self.MAZE_SIZE)
        self.char_list = []     ##this list contains a list of attributes for each character (gets sent over network)
        self.char = []          ##this creates characters for the server
        self.scroll_list = []
        self.still_alive = []
        self.exit = []
        self.is_players_ready = []

        self.count_down = False
        for i in range(self.NUMBER_OF_CHARACTERS):
            self.still_alive.append(False)
        self.connected_players = 0
        GenerateCharacterLocations(self)
        GenerateScrollLocations(self)
        GenerateExitLocation(self)

class GenerateExitLocation(object):
    """creates a random location for the exit"""
    def __init__(self,model):
        self.model = model
        self.maze = model.maze
        x = random.randint(0, self.maze.MAZE_LENGTH - 1)
        x_pos = x*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
        y = random.randint(0, self.maze.MAZE_HEIGHT - 1)
        y_pos = y*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
        exit_entity = [x_pos, y_pos]
        self.model.exit = exit_entity

class GenerateScrollLocations(object):
    """generates the location of the scrolls randomly"""
    def __init__(self, model):
        self.model = model
        self.maze = model.maze
        self.add_scroll = True
        while len(self.model.scroll_list) < self.model.NUMBER_OF_SCROLLS:
            x = random.randint(0, self.maze.MAZE_LENGTH - 1)
            x_pos = x*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            y = random.randint(0, self.maze.MAZE_HEIGHT - 1)
            y_pos = y*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            scroll_entity = [x_pos, y_pos]
            for char in self.model.char_list:
                if not(x_pos == char[0] and y_pos == char[1]):
                    if len(self.model.scroll_list) != 0:
                        for scroll in self.model.scroll_list:
                                if (x_pos == scroll[0] and y_pos == scroll[1]):
                                    self.add_scroll = False
                else:
                    self.add_scroll = False
            if self.add_scroll:
                self.model.scroll_list.append(scroll_entity)
            self.add_scroll = True
            


class GenerateCharacterLocations(object):
    """generates the location of characters randomly"""
    def __init__(self, model):
        self.model = model
        self.maze = model.maze
        self.add_char = True

        monster_int = random.randint(0,(self.model.NUMBER_OF_CHARACTERS)-1)

        while len(self.model.char_list) < self.model.NUMBER_OF_CHARACTERS:
            x = random.randint(0, self.maze.MAZE_LENGTH - 1)
            x_pos = x*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            y = random.randint(0, self.maze.MAZE_HEIGHT - 1)
            y_pos = y*self.maze.MATRIX_CENTERS*2 + self.maze.MATRIX_CENTERS
            char_entity = [x_pos, y_pos, monster_int]
            if len(self.model.char_list) != 0:
                for char in self.model.char_list:
                    if (x_pos == char[0] and y_pos == char[1]):
                        self.add_char = False
            if self.add_char:
                self.model.char_list.append(char_entity)
                char = Character(x_pos, y_pos, 20, 20)
                self.model.char.append(char)
            self.add_char = True

class Character(object):
    """represents the character"""
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

# class representing a sigle connection with a client
# this can also represent a player

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.model = model
    # function called when a player begin a movement
    def Network_move(self, data):
        self.char.x_pos = data['rel_x_pos']
        self.char.y_pos = data['rel_y_pos']
        # send to all other clients the information about moving
        self._server.SendToAll(data)

    def Network_update_alive(self, data):
        self._server.SendToAll(data)

    def Network_update_entities(self, data):
        self._server.SendToAll(data)

    def Network_update_win(self, data):
        self._server.SendToAll(data)

    def Network_lobby(self, data):
        self.model.is_players_ready = data['is_players_ready']
        self._server.SendToAll(data)

    def Network_update_condition(self, data):
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
        self.story = False
        # time before strating the game in milliseconds
        self.wait_to_start = -1
        # addresss and port at which server is started
        address, port = kwargs['localaddr']
        
        print 'Server started at', address, 'at port', str(port)
        print 'Now you can start the clients'
    
    # function called on every connection
    def Connected(self, player, addr):
        print 'Player connected at', addr[0], 'at port', addr[1]
        
        ## add player to the list
        self.model.players.append(player)
        self.model.connected_players = len(self.model.players)
        ## set the bar rect of the player
        player.char = self.model.char[len(self.model.players)-1]      ##add player.char to players[]
        player.Send({'action': 'number', 'num': len(self.model.players)-1})
        player.Send({'action': 'generate_maze', 'maze_matrix' : self.model.maze.maze_matrix})
        player.Send({'action': 'initialize_entities', 'char_list' : self.model.char_list, 'scroll_list' : self.model.scroll_list})
        player.Send({'action': 'exit_location', 'exit': self.model.exit})
        self.SendToAll({'action': 'ready_players', 'connected_players': self.model.connected_players})
    
    # send all clients the same data
    def SendToAll(self, data):
        [p.Send(data) for p in self.model.players]

    def Loop(self):
        t1 = Time()
        while True:
            # update server connection
            myserver.Pump()
            if self.story:
                t1.reset_timer()
                if t1.current_time() > 600:
                    self.start = True
                    self.story = False
                    self.ready = False
                self.SendToAll({'action': 'update_condition', 
                                'story' : self.story,
                                'ready': self.ready,
                                'start': self.start})
                pygame.time.wait(20)
            elif not self.start and not self.story:
                t1.reset_timer()
                ready = True
                if len(self.model.is_players_ready) == 0:
                    ready = False
                for player_ready in self.model.is_players_ready:
                    if not player_ready:
                        ready = False
                if len(self.model.is_players_ready) != self.model.NUMBER_OF_CHARACTERS:
                    ready = False
                self.ready = ready
                if self.ready:
                    self.SendToAll({'action': 'ready', 
                                    'player_ready': self.ready})
                    pygame.time.wait(20)
                else:
                    t1.reset_timer_bool()
                if t1.current_time() > 300:
                    t1.reset_timer_bool()
                    self.story = True
                    self.ready = False
                    self.SendToAll({'action': 'update_condition', 
                                    'story' : self.story,
                                    'ready': self.ready,
                                    'start': self.start})   
                    pygame.time.wait(20)

print 'Enter the ip address of the server. Normally the ip address of the computer.'
print 'example: localhost or 192.168.0.2'
print 'Empty for localhost'
# ip address of the server (normally the ip address of the computer)
#address = raw_input('Server ip: ')
address = '10.7.24.142'
number_of_players = int(raw_input('Players: '))
#control if address is empty
if address == '':
    address = 'localhost'
#address = '10.7.64.193'
# inizialize the server
model = EscapeTheMazeServerModel(number_of_players)
myserver = MyServer(model, localaddr=(address, 31500))
# start mainloop
myserver.Loop()