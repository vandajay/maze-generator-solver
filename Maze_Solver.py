import World as World

import argparse
import random
import threading
import time

class MazeSolver(object): 
    def __init__(self, world):
        self.world = world

        #T search
        self.t_discovered = {}
        self.t_discovered_twice = {}
        self.t_queue = []
        self.t_reverse = []

    def t_search(self):
        self.t_discovered[self.world.player] = 'root'
        self.t_queue.append(self.world.player)
        self.t_reverse.append(self.world.player)
        self.world.set_cell_discovered(self.world.player)

        while len(self.t_queue) > 0:
            node = self.t_queue.pop(0)

            if self.world.check_finish_node(node):
                print(node)
                return node
  
            

            for n in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
                if  self.world.check_valid_move_cell(n) and n not in self.t_discovered:
                    self.t_discovered[n] = node
                    self.t_queue.append(n)     
                    self.t_reverse.append(n) 
                    # Set the color of the cell since it has been discovered.
                    self.world.set_cell_discovered(n)
                    # Sleep in order to show the exploration.
                    # Comment line out if you want it to just go.
                    # Adjust float value lower if you want it to go faster.
                    time.sleep(0.15)
                    break
                else:
                    if self.stuck(node):
                        new_node = self.t_reverse.pop(len(self.t_reverse)-1)
                        self.t_queue.append(new_node) 
                        self.t_discovered_twice[n] = new_node
                        self.world.set_cell_visited_twice(new_node) 
                        time.sleep(0.15)
                        break

                    
                        
                    
    def stuck(self,n):

        num_stuck = 0

        if(not self.world.check_valid_move_cell((n[0]-1,n[1])) or (n[0]-1,n[1]) in self.t_discovered_twice or (n[0]-1,n[1]) in self.t_discovered):
            num_stuck += 1

        if(not self.world.check_valid_move_cell((n[0]+1,n[1])) or (n[0]+1,n[1]) in self.t_discovered_twice or (n[0]+1,n[1]) in self.t_discovered):
            num_stuck += 1

        if(not self.world.check_valid_move_cell((n[0],n[1]-1)) or (n[0],n[1]-1) in self.t_discovered_twice or (n[0],n[1]-1) in self.t_discovered):
            num_stuck += 1

        if(not self.world.check_valid_move_cell((n[0],n[1]+1)) or (n[0],n[1]+1) in self.t_discovered_twice or (n[0],n[1]+1) in self.t_discovered):
            num_stuck += 1

        if(num_stuck == 4):
            return True
        return False
                        
            




    def t_path(self, end):
        """ Construct the path to traverse the maze. 

        Args:
            end: the ending cell to start the backwards path through.
        """
        path = [end]

        while self.t_discovered[path[-1]] != 'root':
            path.append(self.t_discovered[path[-1]])

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

        goal = self.t_search()
        path = self.t_path(goal)

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
parser.add_argument("--world_file", type=str, default="demo_test.dat", help="World file in the worlds folder to use.")
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
