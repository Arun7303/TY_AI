from queue import PriorityQueue

def best_first_search(start, goal, get_neighbors, heuristic):
    open_list = PriorityQueue()
    open_list.put((heuristic(start, goal), start, [start], 0))  # Added total cost
    closed_set = set()
    
    while not open_list.empty():
        _, current_state, path, total_cost = open_list.get()
        if current_state in closed_set:
            continue
        closed_set.add(current_state)
        
        if current_state == goal:
            return path, total_cost
        
        for neighbor, cost in get_neighbors(current_state):
            if neighbor not in closed_set:
                open_list.put((heuristic(neighbor, goal), neighbor, path + [neighbor], total_cost + cost))
    
    return None, None  # No path found

# User Input Functions
def get_puzzle_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    moves = {
        0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
        3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
        6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
    }
    for move in moves[zero_index]:
        new_state = list(state)
        new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
        neighbors.append((tuple(new_state), 1))
    return neighbors

def puzzle_heuristic(state, goal):
    return sum(s != g for s, g in zip(state, goal))  # Misplaced tiles heuristic

def get_robot_neighbors(position):
    x, y = position
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [((x + dx, y + dy), 1) for dx, dy in moves]

def robot_heuristic(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])  # Manhattan distance

def get_city_neighbors(city):
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 2), ('E', 5)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 2), ('E', 1)],
        'E': [('B', 5), ('D', 1), ('F', 2)],
        'F': [('C', 3), ('E', 2)]
    }
    return graph.get(city, [])

def city_heuristic(city, goal):
    heuristics = {'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1}
    return heuristics.get(city, float('inf'))

# User Input
choice = int(input("Choose a problem:\n1. 8 Puzzle\n2. Robot Navigation\n3. Cities Shortest Path\nEnter choice: "))

if choice == 1:
    start_state = tuple(map(int, input("Enter start state (9 numbers separated by space, 0 for empty tile): ").split()))
    goal_state = tuple(map(int, input("Enter goal state (9 numbers separated by space, 0 for empty tile): ").split()))
    path, _ = best_first_search(start_state, goal_state, get_puzzle_neighbors, puzzle_heuristic)
    print("8 Puzzle Path:", path)

elif choice == 2:
    start_x, start_y = map(int, input("Enter robot start position (x y): ").split())
    goal_x, goal_y = map(int, input("Enter goal position (x y): ").split())
    path, _ = best_first_search((start_x, start_y), (goal_x, goal_y), get_robot_neighbors, robot_heuristic)
    print("Robot Navigation Path:", path)

elif choice == 3:
    start_city = input("Enter start city: ")
    goal_city = input("Enter goal city: ")
    path, cost = best_first_search(start_city, goal_city, get_city_neighbors, city_heuristic)
    print("Cities Shortest Path:", path, "with total cost:", cost)

else:
    print("Invalid choice!")