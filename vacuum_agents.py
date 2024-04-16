'''
Use this script file to define your robot vacuum agents.

The run function will generate a map showing the animation of the robot, and return the output of the loss function at the end of the run. The many_runs function will run the simulation multiple times without the visualization and return the average loss. 

You will need to implement a run_all function, which executes the many_runs function for all 12 of your agents (with the correct parameters) and sums up their returned losses as a single value. Your run_all function should use the following parameters for each agent: map_width=20, max_steps=50000 runs=100.
'''

from vacuum import *
import heapq

directions = ['north', 'south', 'east', 'west']
prevdirection = 'null'


def random_agent(percept):
    if (percept):
        return 'clean'

    return random.choice(directions)

def get_adjacent(coord):
    world = get_world()
    agent = get_agent()
    (x, y) = agent
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

def dirty_squares_heuristic(state):
    dirty_squares = 0
    for x in get_world():
        dirty_squares += x.count("dirt")
    return dirty_squares

i = 0

def get_surrounding():
    x_start = x-1
    if x_start == -1: 
        x_start = 0
    return surrounding = [row[x-1:x+2] for row in get_world()[y-1:y+2]]

random_choice = random.choice(directions)
def neighboring_no_memory(percept):
    global i
    global random_choice
    (x, y) = get_agent()
    
    #gets the surrounding grid

    
    print()

    if (percept):
        return 'clean'
     
    width = len(get_world())
    if i < width // 5 + random.randint(-3,3):
        i += 1
        return random_choice
    else:
        i = 0
        random_choice = random.choice([val for val in directions if val != random_choice]) # chooses different random direction
        return random_choice

i = 0
random_choice = random.choice(directions)
def blind_no_memory(percept):
    global i
    global random_choice

    if (percept):
        return 'clean'
     
    width = len(get_world())
    if i < width // 5 + random.randint(-3,3):
        i += 1
        return random_choice
    else:
        i = 0
        random_choice = random.choice([val for val in directions if val != random_choice]) # chooses different random direction
        return random_choice
    
## input args for run: map_width, max_steps, agent_function, loss_function

# run(20, 50000, random_agent, 'actions')

## input args for many_runs: map_width, max_steps, runs, agent_function, loss_function

def run_all():
    #standard parameter
    map_width=20
    max_steps=50000
    num_runs=100

    #sums the total loss from all agents
    total = 0

    #entire map, no memory
    total += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'actions')
    total += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'dirt')

    #no map, no memory
    total += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'actions')
    total += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'dirt')

    return total

run(20, 50000, neighboring_no_memory, "dirt")