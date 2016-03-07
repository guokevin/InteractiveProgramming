# Excuse me for the my bad English, I hope you can understand my comments
# pygame site: www.pygame.org

# import pygame
import pygame
# import network modules
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
# random module to randomize the initial ball direction
from random import randint
from Escape_The_Maze import *

# function which return a random value between -1 and -3
# or between 1 and 3
# this in userful for set the initial ball direction

# class representing a sigle connection with a client
# this can also represent a player
class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        # self.Character = None
    
    # function called when a player begin a movement
    def Network_move(self, data):
        self.Char.x_pos = data['x']
        self.Char.y_pos = data['y']
        # send to all other clients the information about moving
        self._server.SendToAll(data)

# class representing the server
class MyServer(Server):
    channelClass = ClientChannel
    
    # Start the server
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        
        # if self.start is True the game is working 
        self.start = False
        # time before strating the game in milliseconds
        self.wait_to_start = -1
        
        self.characters = (Character(640/2 + 20, 450, 20, 20),Character(640/2 - 20, 450, 20, 20))
        # players
        self.players = []
        
        # addresss and port at which server is started
        address, port = kwargs['localaddr']
        
        print 'Server started at', address, 'at port', str(port)
        print 'Now you can start the clients'
    
    # function called on every connection
    def Connected(self, player, addr):
        print 'Player connected at', addr[0], 'at port', addr[1]
        
        # add player to the list
        self.players.append(player)
        # set the bar rect of the player
        player.Char = self.characters[len(self.players)-1]
        # send to the player his number
        player.Send({'action': 'number', 'num': len(self.players)-1})       
        # if there are two player we can start the game
        if len(self.players) == 2:
            # send to all players the ready message
            self.SendToAll({'action': 'ready'})
            # wait 4 seconds before starting the game
            self.wait_to_start = 300
    
    # send all clients the same data
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Loop(self):
        # infinite loop
        while True:
            # update server connection
            myserver.Pump()
            # if the game is started
            # wait 25 milliseconds
            pygame.time.wait(25)
            
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
# address = raw_input('Server ip: ')

# control if address is empty
# if address == '':
address = 'localhost'

# inizialize the server
myserver = MyServer(localaddr=(address, 31500))
# start mainloop
myserver.Loop()
