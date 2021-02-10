""" Generate a maze file """
import argparse
import random


def create_walls(width, height, start_x, start_y, goal_x, goal_y):
	""" Create walls algorithmically to fit within the maze"""
	# # TODO: You will likely want to insert logic to make sure generated walls do not interfere with your start.
	#create empty list that will return the list of tuples.
	list = []

	#nested for loop to go through the height and width of the grid to create the walls
	for i in range(height):
		for j in range(width):
			#conditions that prevent the wall generator from generating a wall on the start/end as well as walls right
			#next to it as to prevent an unsolvable maze
			if i == start_x or j == start_y:
				j = j + 1
			elif i == start_x + 1 or j == start_y + 1:
				j = j + 1
			elif i == start_x - 1 or j == start_y - 1:
				j = j + 1
			elif i == goal_x - 1 and j == goal_y - 1:
				j = j + 1
			elif i == goal_x or j == goal_y:
				j = j + 1
			else:
				#after checking conditions a random int is generated with a 25% chance of creating a wall at position
				# [i][j]
				r = random.randint(1,4)
				if r == 2:
				#if r hits a 2 generate wall and add the coordinate as a tuple to the list
					list.append(tuple((i,j)))
	# Return the created walls as a list of tuples.  Each tuple is an (x,y) coordinate.
	return list

def check_positive(value):
	""" Source: https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers """
	ivalue = int(value)
	if ivalue < 0:
		raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
	return ivalue

parser = argparse.ArgumentParser()
parser.add_argument("--start_x", type=check_positive, default=random.randint(1, 79), help="x location for the player start.")
parser.add_argument("--start_y", type=check_positive, default=random.randint(1, 79), help="y location for the player start.")
parser.add_argument("--goal_x", type=check_positive, default=random.randint(10, 99), help="x location for the goal.")
parser.add_argument("--goal_y", type=check_positive, default=random.randint(10, 99), help="y location for the goal.")
parser.add_argument("--width", type=check_positive, default=100, help="width of the maze.")
parser.add_argument("--height", type=check_positive, default=100, help="height of the maze.")
parser.add_argument("--output_file", type=str, default="demo_maze_generator.dat", help="Maze output file name.")
args = parser.parse_args()

# Make sure the provided start, goal, width, and height are reasonable.
if args.start_x >= args.width:
	raise ValueError("Start of x {} is larger than the provided width {}".format(args.start_x, args.width))

if args.start_y >= args.height:
	raise ValueError("Start of y {} is larger than the provided height {}".format(args.start_y, args.height))	

if args.goal_x >= args.width:
	raise ValueError("Goal of x {} is larger than the provided width {}".format(args.goal_x, args.width))

if args.goal_y >= args.height:
	raise ValueError("Goal of y {} is larger than the provided height {}".format(args.goal_y, args.height))	

if args.goal_x == args.start_x and args.goal_y == args.start_y:
	raise ValueError("Goal of ({},{}) is identical to start of ({},{})".format(args.goal_x, args.goal_y, args.start_x, args.start_y))

# Generate your walls here, most likely create a function to generate walls and return them as a list of tuples.
walls = create_walls(args.width, args.height, args.start_x, args.start_y, args.goal_x, args.goal_y)

with open("./Worlds/{}".format(args.output_file),"w") as f:
	f.write("x_width:{}\n".format(args.width))
	f.write("y_width:{}\n".format(args.height))
	f.write("x_player_start:{}\n".format(args.start_x))
	f.write("y_player_start:{}\n".format(args.start_y))
	f.write("walls\n")
	for w in walls:
		f.write("{},{}\n".format(w[0],w[1]))
	f.write("specials\n")
	f.write("{}, {}, red, 1, False\n".format(args.goal_x, args.goal_y))
