

import random
import sys
from os import path

#X = 5
#Y = 5

class Grouper(object):
   def __init__(self, init=[]):
      mapping = self._mapping = {}
      for x in init:
         mapping[x] = [x]
        
   def join(self, a, *args):
      """Join given arguments into the same set.
Accepts one or more arguments."""
      mapping = self._mapping
      set_a = mapping.setdefault(a, [a])

      for arg in args:
         set_b = mapping.get(arg)
         if set_b is None:
            set_a.append(arg)
            mapping[arg] = set_a
         elif set_b is not set_a:
            if len(set_b) > len(set_a):
               set_a, set_b = set_b, set_a
            set_a.extend(set_b)
            for elem in set_b:
               mapping[elem] = set_a

   def joined(self, a, b):
      """Returns True if a and b are members of the same set."""
      mapping = self._mapping
      try:
          return mapping[a] is mapping[b]
      except KeyError:
          return False

   def __iter__(self):
      """Returns an iterator returning each of the disjoint sets as a list."""
      seen = set()
      for elem, group in self._mapping.iteritems():
          if elem not in seen:
              yield group
              seen.update(group)

class Cell():
    """Represents a cell in the maze, with an x and y coordinate and its
    right hand wall and downwards wall.

    """
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.right_wall = self.down_wall = None

class Wall():
    """Represents a wall in the maze with its two neighbouring cells.
    """
    def __init__(self):
        self.neighbours = None
        self.active = True

def popchoice(seq):
    """Takes an iterable and pops a random item from it.
    """
    return seq.pop(random.randrange(len(seq)))

def create_maze(X, Y):
    # A mapping of coord tuple to Cell object    
    cells = {}
    # A list of all the non-edge walls
    walls = []

    # Generate cells
    for y in range(Y):
        for x in range(X):
            cells[(x, y)] = Cell(x, y)

    # Generate walls and add to the neighbouring cells
    for y in range(Y):
        for x in range(X):
            current_cell = cells[(x,y)]
            down_wall = Wall()
            current_cell.down_wall = down_wall
            right_wall = Wall()
            current_cell.right_wall = right_wall
            if y != Y-1:
                down_wall.neighbours = (current_cell, cells[(x,y+1)])
                walls.append(down_wall)

            if x != X-1:
                right_wall.neighbours = (current_cell, cells[(x+1,y)])
                walls.append(right_wall)

    grouper = Grouper()
    # Get a list of all the cell objects to give to the Grouper            
    cell_list = [cells[key] for key in cells]

    maze = Grouper(cell_list)

    for _ in range(len(walls)):
        # Pop a random wall from the list and get its neighbours
        wall = popchoice(walls)
        cell_1, cell_2 = wall.neighbours
        # If the cells on either side of the wall aren't already connected,
        # destroy the wall
        if not maze.joined(cell_1, cell_2):
            wall.active = False
            maze.join(cell_1, cell_2)

    # Draw the maze

    maze_map = []

    x_max = (X*2)+1
    y_max = (Y*2)+1

    # Make an empty maze map with True for wall and False for space
    # Make top wall
    maze_map.append([True for _ in range(x_max)])
    for y in range(1, y_max):
        # Make rows with left side wall
        maze_map.append([True]+[False for _ in range(1, x_max)])

    # Add the down and right walls from each cell to the map
    for coords, cell in cells.items():
        x, y = coords
        # Add the intersection wall for each cell (down 1 right 1)
        maze_map[(y*2)+2][(x*2)+2] = True
        if cell.right_wall.active:
            maze_map[(y*2)+1][(x*2)+2] = True
        if cell.down_wall.active:
            maze_map[(y*2)+2][(x*2)+1] = True

    # Print the map
    maze = []
    for i in range(len(maze_map)):
        a = 0
        b = 0
        c = 0
        while(a == b or a == b or c == b):
          a = random.randint(0, X*2)
          b = random.randint(0, X*2)
          c = random.randint(0, X*2)

        maze_row = []
        for j in range(len(maze_map[0])):
            #if(n >= rand_number or j == X or j == 0 or i == 0 or i == Y):
            if maze_map[i][j] and ((j != a and j!= b and j!= c) or j == 2*X or j == 0 or i == 0 or i == 2*Y):
              maze_row.append(1)
            else:
              maze_row.append(0)
        maze.append(maze_row)
        #print maze_row
    return maze
