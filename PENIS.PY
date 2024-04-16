import heapq

class State:
    def __init__(self, grid, agent_pos):
        self.grid = grid
        self.agent_pos = agent_pos

    def __eq__(self, other):
        return self.grid == other.grid and self.agent_pos == other.agent_pos

    def __lt__(self, other):
        # Implement less than comparison based on heuristic values
        return heuristic(self) < heuristic(other)

    def __hash__(self):
        return hash((tuple(map(tuple, self.grid)), self.agent_pos))

def get_actions(state):
    actions = []
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for move in moves:
        new_pos = (state.agent_pos[0] + move[0], state.agent_pos[1] + move[1])
        if 0 <= new_pos[0] < len(state.grid) and 0 <= new_pos[1] < len(state.grid[0]) and state.grid[new_pos[0]][new_pos[1]] != 'X':
            actions.append(new_pos)
    return actions

def heuristic(state):
    dirty_squares = 0
    for row in state.grid:
        dirty_squares += row.count('D')
    return dirty_squares



def greedy_best_first_search(initial_state):
    open_list = [(heuristic(initial_state), initial_state)]
    visited = set()
    while open_list:
        _, state = heapq.heappop(open_list)
        print_state(state)  # Print the current state
        if is_goal_state(state):
            return state
        visited.add(state)
        for action in get_actions(state):
            new_grid = [row[:] for row in state.grid]
            new_grid[action[0]][action[1]] = '.'
            new_state = State(new_grid, action)
            if new_state not in visited:
                heapq.heappush(open_list, (heuristic(new_state), new_state))
    return None


def print_state(state):
    for row in state.grid:
        print(' '.join(row))
    print("Agent position:", state.agent_pos)
    print()
def is_goal_state(state):
    for row in state.grid:
        if 'D' in row:
            return False
    return True

# Example usage
grid = [
    ['.', '.', '.', 'D', 'D'],
    ['.', 'X', '.', 'X', '.'],
    ['.', '.', 'D', '.', '.'],
    ['X', '.', 'D', 'X', '.'],
    ['.', '.', '.', '.', 'D']
]
initial_state = State(grid, (0, 0))
goal_state = greedy_best_first_search(initial_state)
print(goal_state.agent_pos)  # Output: (0, 4)
