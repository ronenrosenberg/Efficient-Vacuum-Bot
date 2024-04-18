'''
Use this script file to define your robot vacuum agents.

The run function will generate a map showing the animation of the robot, and return the output of the loss function at the end of the run. The many_runs function will run the simulation multiple times without the visualization and return the average loss. 

You will need to implement a run_all function, which executes the many_runs function for all 12 of your agents (with the correct parameters) and sums up their returned losses as a single value. Your run_all function should use the following parameters for each agent: map_width=20, max_steps=50000 runs=100.
'''

from vacuum import *
import heapq
import math

directions = ['north', 'south', 'east', 'west']
prevdirection = 'null'


def random_agent(percept):
    if (percept):
        return 'clean'

    return random.choice(directions)

def dirty_squares_heuristic(state):
    dirty_squares = 0
    for x in get_world():
        dirty_squares += x.count("dirt")
    return dirty_squares

#good job, little function
def manhattan_distance(agent, goal):
    (x1, y1) = agent
    (x2, y2) = goal
    return abs(x1-x2) + abs(y1-y2)


#please note: this function is a piece of shit
def minimize_manhattan_distance(agent, goal, nearest):
    #finds the states of the squares surrounding the agent
    surrounding = get_surrounding()
    
    direction_and_dist = [(random.randint(0,3), 1000)]
    for i in range(len(surrounding)):
        if surrounding[i] != 'wall':
            (x, y) = agent
            if directions[i] in ['north', 'south']:
                y += OFFSETS[directions[i]][1]
            elif directions[i] in ['east', 'west']:
                x += OFFSETS[directions[i]][0]

            direction_and_dist.append((i, manhattan_distance(nearest, (x,y))))
            #print(manhattan_distance((x,y), goal))
    
    #direction index
    direction_and_dist.sort(key=lambda x: x[1])
    print("best direction index", direction_and_dist) 
    print("nearest dirt",find_nearest_dirt())
    return direction_and_dist[random.randint(0,0)][0]
    

def find_nearest_dirt():
    world = get_world()
    agent = get_agent()

    best_distance = 1000
    best_coord = None

    for x in range(len(world)):
        for y in range(len(world)):
            coord = (x, y)
            if world[x][y] == 'dirt':
                if best_distance > manhattan_distance(agent, coord):
                    best_distance = manhattan_distance(agent, coord)
                    best_coord = (x, y)

    return best_coord

def get_surrounding():
    direction_list = []
    world = get_world()
    (x, y) = get_agent()

    if y == len(world)-1: direction_list.append("wall")
    else: direction_list.append(world[x][y+1])
    if y == 0: direction_list.append("wall")
    else: direction_list.append(world[x][y-1])
    
    if x == len(world)-1: direction_list.append("wall")
    else: direction_list.append(world[x+1][y])
    if x == 0: direction_list.append("wall")
    else: direction_list.append(world[x-1][y])

    return direction_list

i = 0
nearest = None
previous_direction = -1
def entire_map_memory(percept):
    global i
    global nearest
    global previous_direction
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #gets surrounding
    surrounding = get_surrounding()
    if 'dirt' in surrounding:
        if surrounding[0] == 'dirt':
            return directions[0]
        if surrounding[2] == 'dirt':
            return directions[2]
        if surrounding[1] == 'dirt':
            return directions[1]
        if surrounding[3] == 'dirt':
            return directions[3]

    #go to nearest dirt if nothing adjacent
    #print(find_nearest_dirt())
    if nearest == None or get_world()[nearest[0]][nearest[1]] == 'clean':
        nearest = find_nearest_dirt()

    best_direction = directions[minimize_manhattan_distance((x, y), find_nearest_dirt(), nearest)]
    if previous_direction == best_direction:
        previous_direction = random.randint(0,3)
        return directions[previous_direction]
    else:
        previous_direction = best_direction
        return best_direction
    

i = 0
nearest = None
def entire_map_no_memory(percept):
    global i
    global nearest
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #gets surrounding
    surrounding = get_surrounding()
    if 'dirt' in surrounding:
        if surrounding[0] == 'dirt':
            return directions[0]
        if surrounding[2] == 'dirt':
            return directions[2]
        if surrounding[1] == 'dirt':
            return directions[1]
        if surrounding[3] == 'dirt':
            return directions[3]

    #go to nearest dirt if nothing adjacent
    #print(find_nearest_dirt())
    if nearest == None or get_world()[nearest[0]][nearest[1]] == 'clean':
        nearest = find_nearest_dirt()
    return directions[minimize_manhattan_distance((x, y), find_nearest_dirt(), nearest)]


i = 0
random_choice = random.choice(directions)
def neighboring_no_memory(percept):
    global i
    global random_choice
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #gets surrounding
    surrounding = get_surrounding()
    if 'dirt' in surrounding:
        if surrounding[0] == 'dirt':
            return directions[0]
        if surrounding[2] == 'dirt':
            return directions[2]
        if surrounding[1] == 'dirt':
            return directions[1]
        if surrounding[3] == 'dirt':
            return directions[3]

    
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
    #total += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'actions')
    #total += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'dirt')

    #neighboring, no memory
    total += many_runs(map_width, max_steps, num_runs, neighboring_no_memory, 'actions')
    total += many_runs(map_width, max_steps, num_runs, neighboring_no_memory, 'dirt')

    #no map, no memory
    total += many_runs(map_width, max_steps, num_runs, blind_no_memory, 'actions')
    total += many_runs(map_width, max_steps, num_runs, blind_no_memory, 'dirt')

    return total

print(run(20, 50000, entire_map_memory, "actions"))