import World as World

import argparse
import random
import threading
import time

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.p


class MazeSolver(object): 
    def __init__(self,world):
        self.world = world

        self.f = {}
        self.g = {}
        self.h = {}

        self.astar_discovered = {}
        self.astar_open_queue = []
        self.astar_closed_queue = []


    def astar_search(self):
        # initialize f,g,h
        self.f[self.world.player] = 0
        self.g[self.world.player] = 0
        self.h[self.world.player] = 0
        
        # add starting pos to open list, set as discovered
        self.astar_discovered[self.world.player] = 'root'
        self.astar_open_queue.append(self.world.player)

        # set color as visited
        self.world.set_cell_discovered(self.world.player)

        # run loop until end is reached
        while len(self.astar_open_queue) > 0:
            node = self.astar_open_queue[0]
            index = 0

            self.world.set_cell_discovered(node)
            for i, n in enumerate(self.astar_open_queue):
                if self.world.check_valid_move_cell(n) and n not in self.astar_discovered:
                    self.world.set_cell_discovered(node)
                    if self.f[n] < self.f[node]: 
                        node = n # set current node to best position
                        index = i

                

            self.astar_open_queue.pop(index)
            self.astar_closed_queue.append(node) # lock in node
            # self.world.set_cell_discovered(node) # set color

            if self.world.check_finish_node(node):
                return node # found ending node

            children = []
            for n in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:

                # check range
                if n[0] > (self.world.world_spec.x_width - 1) or n[0] < 0 or n[1] > (self.world.world_spec.y_width - 1) or n[1] < 0:
                    continue # jumps back to for loop
                if not self.world.check_valid_move_cell(n):
                    continue
                children.append(n)

            for c in children:
                for j in self.astar_closed_queue:
                    if c == j:
                        continue

                # g distance from start
                self.g[c] = self.g[node] + 1 

                # h estimated distance from end pythagorean theorem
                self.h[c] = ((c[0] - self.world.world_spec.specials[0][0]) ** 2) + ((c[1] - self.world.world_spec.specials[0][1]) ** 2)

                # the f = g + h for child
                self.f[c] = self.g[c] + self.h[c]

                for k in self.astar_open_queue: # compare
                    if c == k and self.g[c] > self.g[k]:
                        continue

                self.astar_open_queue.append(c)
                time.sleep(0.025)

            self.world.set_cell_visited(node)

    def astar_path(self, goal):
        """ Construct the path to traverse the maze. 

        Args:
            end: the ending cell to start the backwards path through.
        """
        path = [goal]

        while self.astar_closed_queue[path[-1]] != 'root': # -1 index reads from end of list
            path.append(self.astar_closed_queue[path[-1]])

        path.reverse()
        return path

    def do_action(self,action):
        s = self.world.player
        if action == 0:
            self.world.try_move(0, -1)
        elif action == 1:
            self.world.try_move(0, 1)
        elif action == 2:
            self.world.try_move(-1, 0)
        elif action == 3:
            self.world.try_move(1, 0)
        else:
            return
        s2 = self.world.player
        return s, s2

    def run(self):

        time.sleep(1)
        t = 1

        goal = self.astar_search()
        path = self.astar_path(goal)

        # Print out the path to the console.
        # Comment out if you don't need it.
        print("Path is: ", end="")
        print(path)

        # Execute the BFS path repeatedly.
        while True:
            for i in range(len(path)-1):
                # Find which direction the player should move.
                direction = [path[i+1][0] - path[i][0], path[i+1][1] - path[i][1]]

                action = 0
                if direction[0] == 0:
                    if direction[1] == -1:
                        # up
                        action = 0
                    else:
                        # down
                        action = 1
                else:
                    if direction[0] == -1:
                        # left
                        action = 2
                    else:
                        # right
                        action = 3

                s = self.world.player
                (s, s2) = self.do_action(action)

                # Check if the game has restarted
                t += 1.0

                if self.world.has_restarted():
                    time.sleep(2)
                    self.world.restart_game()
                    if self.world.has_restarted():
                        print(f"Maze Solved in {t} steps.")
                    t = 1.0

                # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
                time.sleep(0.1)

# Get command line arguments needed for the algorithm.
parser = argparse.ArgumentParser()
parser.add_argument("--world_file", type=str, default="world_enhanced.dat", help="World file in the worlds folder to use.")
args = parser.parse_args()

# Create a world to render the maze visually and allow 
# for maze exploration.
world = World.World(args.world_file)

# Create an instance of your maze solver. 
# The default is a breadth first search.
solver = MazeSolver(world)

# The solver is threaded separate from the graphics
# since graphics run in an infinite loop.
t = threading.Thread(target=solver.run)
t.daemon = True
t.start()

# Start the graphics loop.
world.start_game()
