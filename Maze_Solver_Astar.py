import World as World

import argparse
import random
import threading
import time

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other): # for comparing to other node objects with '==' op
        return self.position == other.position

class MazeSolver(object):
    def __init__(self,world):
        self.world = world
        self.astar_open_queue = []
        self.astar_closed_queue = []

    def astar_search(self):
        start_node = Node(None, self.world.player)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(None, (self.world.world_spec.specials[0][0], self.world.world_spec.specials[0][1]))
        goal_node.g = goal_node.h = goal_node.f = 0

        # add starting pos to open list of moves
        self.astar_open_queue.append(start_node)

        # set color
        self.world.set_cell_discovered(start_node.position)

        # run loop until goal node is reached
        while len(self.astar_open_queue) > 0:
            # time.sleep(0.2)
            current_node = self.astar_open_queue[0] # node is current position
            index = 0
            self.world.set_cell_visited_twice(current_node.position)
            for i, move in enumerate(self.astar_open_queue):
                if move.f < current_node.f:
                    current_node = move # set current node to best position
                    index = i
                    if self.world.check_finish_node(current_node.position):
                        return current_node # found goal

            self.astar_closed_queue.append(current_node) # add node to path
             # pop out open move after moving into closed moves
            self.astar_open_queue.pop(index)

            children = []
            for new_pos in [
                (current_node.position[0]-1, current_node.position[1]),
                (current_node.position[0]+1, current_node.position[1]),
                (current_node.position[0], current_node.position[1]-1),
                (current_node.position[0], current_node.position[1]+1)
                ]:
                    if not self.world.check_valid_move_cell(new_pos):
                        continue # skip invalid child/position

                    new_node = Node(current_node, new_pos)
                    children.append(new_node)
                    self.world.set_cell_discovered(new_pos)

            for child in children:
                for closed_child in self.astar_closed_queue:
                    if child == closed_child:
                        continue

                # g distance from start
                child.g = current_node.g + 1 

                # h estimated distance from goal with pythagorean theorem shorthand
                child.h = ((child.position[0] - goal_node.position[0]) ** 2) + ((child.position[1] - goal_node.position[1]) ** 2)

                # calculate f value
                child.f = child.g + child.h

                # if if child is already in open moves, check if child has better pathing (lower g) skip otherwise
                try: 
                    found_node = self.astar_open_queue[self.astar_open_queue.index(child)]
                    if child.g > found_node.g:
                        continue
                except ValueError:  # not in open_nodes
                    pass

                self.astar_open_queue.append(child)
                self.world.set_cell_visited(child.position)

    def astar_path(self, goal):
        """ Construct the path to traverse the maze. 

        Args:
            end: the ending cell to start the backwards path through.
        """
        if goal.position == (self.world.world_spec.specials[0][0], self.world.world_spec.specials[0][1]):
            path = []
            current = goal

            while current is not None: # None meaning no parent aka start
                path.append(current.position)
                current = current.parent
            
            return path[::-1] # reverse path

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

        # Execute the path repeatedly.
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
                time.sleep(0.01)

# Get command line arguments needed for the algorithm.
parser = argparse.ArgumentParser()
parser.add_argument("--world_file", type=str, default="demo_maze_generator.dat", help="World file in the worlds folder to use.")
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
