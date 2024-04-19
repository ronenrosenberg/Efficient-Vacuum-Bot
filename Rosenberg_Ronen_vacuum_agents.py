#Rosenberg, Ronen
'''
Use this script file to define your robot vacuum agents.

The run function will generate a map showing the animation of the robot, and return the output of the loss function at the end of the run. The many_runs function will run the simulation multiple times without the visualization and return the average loss. 

You will need to implement a run_all function, which executes the many_runs function for all 12 of your agents (with the correct parameters) and sums up their returned losses as a single value. Your run_all function should use the following parameters for each agent: map_width=20, max_steps=50000 runs=100.
'''

from Rosenberg_Ronen_vacuum import *

directions = ['north', 'south', 'east', 'west']

#good job, little function
def manhattan_distance(agent, goal):
    (x1, y1) = agent
    (x2, y2) = goal
    return abs(x1-x2) + abs(y1-y2)

#looks at next possible steps an agent could take and returns the one that reduces the manhattan distance to the given goal
#rand is False only for entire_map_memory because it uses a slightly different strategy
prev_moves = []
stuck = False
i = 0
random_choice = None
def minimize_manhattan_distance(agent, goal, rand=True):
    global prev_moves
    global stuck
    #finds the states of the squares surrounding the agent
    surrounding = get_surrounding()
    
    #creates list of possible directions and what their manhattan distance to the goal would be
    direction_and_dist = [(random.randint(0,3), 1000)]
    for i in range(len(surrounding)):
        if surrounding[i] != 'wall':
            (x, y) = agent
            if directions[i] in ['north', 'south']:
                y += OFFSETS[directions[i]][1]
            elif directions[i] in ['east', 'west']:
                x += OFFSETS[directions[i]][0]

            direction_and_dist.append((i, manhattan_distance(goal, (x,y))))
    
    #sorts by lowest manhattan distance
    direction_and_dist.sort(key=lambda x: x[1])

    if rand:
        #half of time, makes random move, other half gives move that most optimally reduces the manhattan distance
        if random.random() < 0.5:
            return random.choice(direction_and_dist)[0]
        else:
            return direction_and_dist[0][0]
    else:
        #different strat where if has memory capacity and detects looping movement, only then will it go off in a random direction
        if stuck:
            random_choice = random.choice(direction_and_dist)[0]
            width = len(get_world())
            if i < width // 5 + random.randint(-3,3):
                i += 1
                return random_choice
            else:
                i = 0
                stuck = False
        if len(prev_moves) >= 5 and prev_moves[-1] == prev_moves[-3]:
            stuck = True
            prev_moves.append((random.randint(1,5),random.randint(1,5)))
            return random.choice(direction_and_dist)[0]
        else:
            prev_moves.append(agent)
            return direction_and_dist[0][0]
            
    
#finds dirty square nearest to the agent
def find_nearest_dirt(check_list=None):
    world = get_world()
    agent = get_agent()


    best_distance = 1000
    best_coord = None

    if check_list == None:
        for x in range(len(world)):
            for y in range(len(world)):
                coord = (x, y)
                if world[x][y] == 'dirt':
                    if best_distance > manhattan_distance(agent, coord):
                        best_distance = manhattan_distance(agent, coord)
                        best_coord = (x, y)
    else:
        for coord in check_list:
            (x, y) = coord
            if world[x][y] == 'dirt':
                if best_distance > manhattan_distance(agent, coord):
                    best_distance = manhattan_distance(agent, coord)
                    best_coord = (x, y)


    return best_coord

#gets state of all squares that surround the agent
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
#memory agents
def entire_map_memory(percept):
    global i
    global random_choice
    global nearest
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #if adjacent dirt, go there
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

    #returns move that minimizes manhattan distance to nearest dirty square
    if nearest == None or get_world()[nearest[0]][nearest[1]] == 'clean':
        nearest = find_nearest_dirt()
    return directions[minimize_manhattan_distance((x, y), nearest, False)]

i = 0
random_choice = random.choice(directions)
nearest = None
to_clean = []
def neighboring_memory(percept):
    global i
    global random_choice
    global nearest
    global to_clean
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #creates list of surrounding tiles which haven't yet been cleaned
    (x,y) = get_agent()
    if x != len(get_world())-1 and (x+1, y) not in to_clean:
        to_clean.append((x+1, y))
    if x != 0 and (x-1, y) not in to_clean:
        to_clean.append((x-1, y))
    if y != len(get_world())-1 and (x, y+1) not in to_clean:
        to_clean.append((x, y+1))
    if y != 0 and (x, y-1) not in to_clean:
        to_clean.append((x, y-1))
    for coord in to_clean:
        if get_world()[coord[0]][coord[1]] == 'clean':
            to_clean.remove(coord)

    #if adjacent dirt, go there
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


    if nearest == None or get_world()[nearest[0]][nearest[1]] == 'clean':
        nearest = find_nearest_dirt(to_clean)
        #random behavior if no known uncleaned squares
        if nearest == None:
            width = len(get_world())
            if i < width // 5 + random.randint(-3,3):
                i += 1
                return random_choice
            else:
                i = 0
        
            dont_go = None
            match directions.index(random_choice):
                case 1: dont_go = 0
                case 0: dont_go = 1
                case 2: dont_go = 3
                case 3: dont_go = 2

            random_choice = random.choice([val for val in directions if val != random_choice and val != directions[dont_go]]) # chooses different random direction
            return random_choice
    
    #direction that minimizes the manhattan distance between agent and closest known dirty square
    return directions[minimize_manhattan_distance((x, y), nearest)]
    
#this one works, but is worse so for my blind memory one I'm going to also use my one that holds nothing in it's memory
i = 0
stop = 0
random_choice = random.choice(directions)
prev_cleaned = []
just_cleaned = False
def blind_memory(percept):
    global i
    global random_choice
    global prev_cleaned
    global just_cleaned

    agent = get_agent()
    
    if (percept):
        if get_agent() not in prev_cleaned:
            prev_cleaned.append(get_agent())
        just_cleaned = True
        return 'clean'
    
    width = len(get_world())

    dont_go = None
    match directions.index(random_choice):
        case 1: dont_go = 0
        case 0: dont_go = 1
        case 2: dont_go = 3
        case 3: dont_go = 2
    
    if i < width // 3 + random.randint(-3,3):
        if (agent[0]+OFFSETS[random_choice][0], agent[1]+OFFSETS[random_choice][1]) in prev_cleaned and just_cleaned:
            just_cleaned = False
            i = 0
            
            random_choice = random.choice([val for val in directions if val != random_choice and val != directions[dont_go]]) # chooses different random direction
            return random_choice
        i += 1
        return random_choice
    else:
        just_cleaned = False
        i = 0
        random_choice = random.choice([val for val in directions if val != random_choice and val != directions[dont_go]]) # chooses different random direction
        return random_choice


#no memory agents
i = 0
nearest = None
def entire_map_no_memory(percept):
    global i
    global nearest
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #if adjacent dirt, go there
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

    #minimize manhattan distance to nearest dirty square
    if nearest == None or get_world()[nearest[0]][nearest[1]] == 'clean':
        nearest = find_nearest_dirt()
    return directions[minimize_manhattan_distance((x, y), nearest)]

i = 0
random_choice = random.choice(directions)
def neighboring_no_memory(percept):
    global i
    global random_choice
    (x, y) = get_agent()

    if (percept):
        return 'clean'
    
    #if adjacent dirt, go there
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
        i=0
        dont_go = None
        match directions.index(random_choice):
            case 1: dont_go = 0
            case 0: dont_go = 1
            case 2: dont_go = 3
            case 3: dont_go = 2

        #go in different orthagonal direction
        random_choice = random.choice([val for val in directions if val != random_choice and val != directions[dont_go]]) # chooses different random direction
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
        
        dont_go = None
        match directions.index(random_choice):
            case 1: dont_go = 0
            case 0: dont_go = 1
            case 2: dont_go = 3
            case 3: dont_go = 2

        #go in different orthagonal direction
        random_choice = random.choice([val for val in directions if val != random_choice and val != directions[dont_go]]) # chooses different random direction

        return random_choice

#runs all other functions
def run_all():
    #standard parameters
    map_width=20
    max_steps=50000
    num_runs=100

    #sums the total loss from all agents
    total = 0
    loss_list = [0 for i in range(12)]

    #no memory agents
    #entire map, no memory
    loss_list[0] += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'actions')
    loss_list[1] += many_runs(map_width, max_steps, num_runs, entire_map_no_memory, 'dirt')
    print("entire_map_no_memory actions:", loss_list[0])
    print("entire_map_no_memory dirt:", loss_list[1])
    print()


    #neighboring, no memory
    loss_list[2] += many_runs(map_width, max_steps, num_runs, neighboring_no_memory, 'actions')
    loss_list[3] += many_runs(map_width, max_steps, num_runs, neighboring_no_memory, 'dirt')
    print("neighboring_no_memory actions:", loss_list[2])
    print("neighboring_no_memory dirt:", loss_list[3])
    print()

    #no map, no memory
    loss_list[4] += many_runs(map_width, max_steps, num_runs, blind_no_memory, 'actions')
    loss_list[5] += many_runs(map_width, max_steps, num_runs, blind_no_memory, 'dirt')
    print("blind_no_memory actions:", loss_list[4])
    print("blind_no_memory dirt:", loss_list[5])
    print()

    #memory agents
    #entire map, memory
    loss_list[6] += many_runs(map_width, max_steps, num_runs, entire_map_memory, 'actions')
    loss_list[7] += many_runs(map_width, max_steps, num_runs, entire_map_memory, 'dirt')
    print("entire_map_memory actions:", loss_list[6])
    print("entire_map_memory dirt:", loss_list[7])
    print()
    
    #neighboring, memory
    loss_list[8] += many_runs(map_width, max_steps, num_runs, neighboring_memory, 'actions')
    loss_list[9] += many_runs(map_width, max_steps, num_runs, neighboring_memory, 'dirt')
    print("neighboring_memory actions:", loss_list[8])
    print("neighboring_memory dirt:", loss_list[9])
    print()

    #no map, memory
    loss_list[10] += many_runs(map_width, max_steps, num_runs, blind_no_memory, 'actions')
    loss_list[11] += many_runs(map_width, max_steps, num_runs, blind_no_memory, 'dirt')
    print("blind_memory actions (choosing to use no memory):", loss_list[10])
    print("blind_memory dirt (choosing to use no memory):", loss_list[11])
    print()

    print("Total loss:", sum(loss_list))

run_all()
