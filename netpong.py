# import pygame
import pygame
# import network module
from PodSixNet.Connection import connection, ConnectionListener
from Escape_The_Maze import *

# init pygame
pygame.init()

# class for I/O on network
# this represent the player, too
class Listener(ConnectionListener):
    # init the player
    def __init__(self, host, port):
        self.Connect((host, port))
        
        # set the window
        self.screen = pygame.display.set_mode((1000, 1000))
        self.model = EscapeTheMazeModel()
        self.view = PygameEscapeTheMazeView(self.model,self.screen)
        self.controller = PyGameKeyboardController(self.model)
        
        # player number. this can be 0 (left player) or 1 (right player)
        self.num = None
        # players' rects
        self.players = (Character(640/2 + 20, 450, 20, 20),Character(640/2 - 20, 450, 20, 20))

        # True if the server sended the ready message
        self.ready = False
        # True if the game is working
        self.start = False
        self.running = True
        # font for writing the scores
        self.font = pygame.font.SysFont('sans,freesans,courier,arial', 18, True)

        self.x_pos = [0,0]
        self.y_pos = [0,0]
        # self.move_ticker = 0
        # self.refresh_rate = 3
        # self.vel = 5

    # function to manage bars movement
    def Network_move(self, data):
        if data['player'] != self.num:
            self.players[data['player']].x_pos = data['x']
            self.players[data['player']].y_pos = data['y']

        
    # get the player number
    def Network_number(self, data):
        self.num = data['num']
    
    # if the game is ready
    def Network_ready(self, data):
        self.ready = not self.ready

    # start the game
    def Network_start(self, data):
        self.ready = False
        self.start = True
    
    # mainloop
    def Loop(self):
        while self.running:
            # update connection
            connection.Pump()
            # update the listener
            self.Pump()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == QUIT:
                    self.running = False
            self.controller.handle_event(event)
            self.view.draw()
            time.sleep(.001)
            


            # for event in pygame.event.get():
            #     if event.type == QUIT:
            #         running = False
            #     controller.handle_event(event)
            #     view.draw()
            #     time.sleep(.001)
            # for event in pygame.event.get():
            #     # end the game in necessary
            #     if event.type == pygame.QUIT:
            #         exit(0)
                # elif self.start:
                #     if event.type == pygame.KEYDOWN:
                #         keys = pygame.key.get_pressed()
                        # if keys[pygame.K_ESCAPE]:
                            # running = False

                        # if keys[pygame.K_a] and keys[pygame.K_w]:
                        #     if self.move_ticker > self.refresh_rate + 2:
                        #         self.move_ticker = 0
                        #         self.x_pos[self.num] -= self.vel
                        #         self.y_pos[self.num] -= self.vel
                        # elif keys[pygame.K_a] and keys[pygame.K_s]:
                        #     if self.move_ticker > self.refresh_rate + 2:
                        #         self.move_ticker = 0
                        #         self.x_pos[self.num] -= self.vel
                        #         self.y_pos[self.num] += self.vel
                        # elif keys[pygame.K_d] and keys[pygame.K_w]:
                        #     if self.move_ticker > self.refresh_rate + 2:
                        #         self.move_ticker = 0
                        #         self.x_pos[self.num] += self.vel
                        #         self.y_pos[self.num] -= self.vel
                        # elif keys[pygame.K_d] and keys[pygame.K_s]:
                        #     if self.move_ticker > self.refresh_rate + 2:
                        #         self.move_ticker = 0
                        #         self.x_pos[self.num] += self.vel
                        #         self.y_pos[self.num] += self.vel
                        # elif keys[pygame.K_a]:
                        #     if self.move_ticker > self.refresh_rate:
                        #         self.move_ticker = 0
                        #         self.x_pos[self.num] -= self.vel
                        # elif keys[pygame.K_d]:
                        #     if self.move_ticker > self.refresh_rate:
                        #         self.move_ticker = 0
                        #         self.x_pos[self.num] += self.vel
                        # elif keys[pygame.K_w]:
                        #     if self.move_ticker > self.refresh_rate:
                        #         self.move_ticker = 0
                        #         self.y_pos[self.num] -= self.vel
                        # elif keys[pygame.K_s]:
                        #     if self.move_ticker > self.refresh_rate:
                        #         self.move_ticker = 0
                        #         self.y_pos[self.num] += self.vel
                        # self.move_ticker += 1
                    # elif event.type == pygame.KEYUP:
                    #     self.x_pos[self.num] = 0
                    #     self.y_pos[self.num] = 0

            # control user input
            """for event in pygame.event.get():
                # end the game in necessary
                if event.type == pygame.QUIT:
                    exit(0)

                # if the game is started
                elif self.start:
                
                    # control user keyboard input
                    if event.type == pygame.KEYDOWN:
                        if event.unicode == 'a':
                            self.x_pos[self.num] = -10
                        elif event.unicode == 'd':
                            self.x_pos[self.num] = 10
                        elif event.unicode == 'w':
                            self.y_pos[self.num] = -10
                        elif event.unicode == 's':
                            self.y_pos[self.num] = 10
                    
                    elif event.type == pygame.KEYUP:
                        self.x_pos[self.num] = 0
                        self.y_pos[self.num] = 0"""

            
            # clear the screen
            self.screen.fill((0, 0, 0))
            
            # if game is working
            if self.start:
                n = 0
                for move in self.x_pos:
                    self.players[n].x_pos += move
                    n += 1

                n = 0
                for move in self.y_pos:
                    self.players[n].y_pos += move
                    n += 1
                
                # send to the server information about movement
                connection.Send({'action': 'move', 'player': self.num, 'x': self.players[self.num].x_pos, 'y': self.players[self.num].y_pos})
                
                for Char in self.players:
                    pygame.draw.rect(self.screen, pygame.Color(Char.color), pygame.Rect(Char.x_pos, Char.y_pos, Char.width, Char.height))

                # update the screen
                pygame.display.flip()
            
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
            pygame.time.wait(2)
        

print 'Enter the server ip address'
print 'Empty for localhost'
# ask the server ip address
# server = raw_input('server ip: ')
# control if server is empty
# if server == '':
    # server = 'localhost'

server = 'localhost'
# init the listener
listener = Listener(server, 31500)
# start the mainloop
listener.Loop()
