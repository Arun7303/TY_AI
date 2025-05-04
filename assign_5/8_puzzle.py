import heapq

class PuzzleState:
    def __init__(self, state, goal_state, parent=None, move=None, depth=0):
        self.state = state
        self.goal_state = goal_state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.heuristic = self.calculate_heuristic()
        
    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(tuple(self.state))
    
    def calculate_heuristic(self):
        # Manhattan distance heuristic
        heuristic = 0
        for i in range(9):
            if self.state[i] != 0:  # Don't count the blank tile
                current_row, current_col = i // 3, i % 3
                goal_row, goal_col = self.goal_position(self.state[i])
                heuristic += abs(current_row - goal_row) + abs(current_col - goal_col)
        return heuristic
    
    def goal_position(self, value):
        # Find where this value should be in the goal state
        index = self.goal_state.index(value)
        return index // 3, index % 3
    
    def is_goal(self):
        return self.state == self.goal_state
    
    def get_blank_pos(self):
        return self.state.index(0)
    
    def generate_children(self):
        children = []
        blank_pos = self.get_blank_pos()
        row, col = blank_pos // 3, blank_pos % 3
        
        # Possible moves: up, down, left, right
        moves = []
        if row > 0: moves.append(-3)  # up
        if row < 2: moves.append(3)    # down
        if col > 0: moves.append(-1)   # left
        if col < 2: moves.append(1)    # right
        
        for move in moves:
            new_state = self.state.copy()
            new_pos = blank_pos + move
            new_state[blank_pos], new_state[new_pos] = new_state[new_pos], new_state[blank_pos]
            
            move_name = ""
            if move == -3: move_name = "Up"
            elif move == 3: move_name = "Down"
            elif move == -1: move_name = "Left"
            elif move == 1: move_name = "Right"
            
            children.append(PuzzleState(new_state, self.goal_state, self, move_name, self.depth + 1))
        
        return children
    
    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Reverse to get from start to goal

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print()

def solve_puzzle(initial_state, goal_state):
    open_list = []
    closed_set = set()
    
    initial_node = PuzzleState(initial_state, goal_state)
    heapq.heappush(open_list, initial_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if current_node.is_goal():
            return current_node.get_path()
        
        closed_set.add(current_node)
        
        for child in current_node.generate_children():
            if child in closed_set:
                continue
            
            # Calculate f(n) = g(n) + h(n)
            f_current = current_node.depth + current_node.heuristic
            f_child = child.depth + child.heuristic
            
            # Check if child is already in open list with higher cost
            in_open = False
            for open_node in open_list:
                if open_node == child and (open_node.depth + open_node.heuristic) <= f_child:
                    in_open = True
                    break
            
            if not in_open:
                heapq.heappush(open_list, child)
    
    return None  # No solution found

def get_state_input(prompt):
    print(prompt)
    print("Enter the state row by row (use 0 for the blank space)")
    state = []
    for i in range(3):
        while True:
            row_input = input(f"Row {i+1} (3 numbers separated by spaces): ").strip()
            if len(row_input.split()) == 3 and all(num.isdigit() for num in row_input.split()):
                row = [int(num) for num in row_input.split()]
                state.extend(row)
                break
            else:
                print("Invalid input. Please enter exactly 3 numbers separated by spaces.")
    return state

def is_valid_state(state):
    # Check if state has exactly 9 elements with numbers 0-8 and all unique
    return (len(state) == 9 and 
            all(0 <= num <= 8 for num in state) and 
            len(set(state)) == 9)

def main():
    print("8-Puzzle Solver using A* Algorithm")
    print("----------------------------------")
    
    # Get initial state
    while True:
        initial_state = get_state_input("Enter the initial state:")
        if is_valid_state(initial_state):
            break
        print("Invalid initial state. Please use numbers 0-8 with no duplicates.")
    
    # Get goal state
    while True:
        goal_state = get_state_input("Enter the goal state:")
        if is_valid_state(goal_state):
            break
        print("Invalid goal state. Please use numbers 0-8 with no duplicates.")
    
    print("\nInitial State:")
    print_state(initial_state)
    
    print("Goal State:")
    print_state(goal_state)
    
    print("Solving...")
    solution_path = solve_puzzle(initial_state, goal_state)
    
    if solution_path:
        print("\nSolution Found!")
        print(f"Total moves: {len(solution_path)-1}")
        print("\nSolution Path:")
        for i, node in enumerate(solution_path):
            print(f"Step {i}: {node.move}" if node.move else "Initial State")
            print(f"Heuristic (h): {node.heuristic}, Cost (g): {node.depth}, Total (f): {node.heuristic + node.depth}")
            print_state(node.state)
    else:
        print("No solution exists for the given initial and goal states.")

if __name__ == "__main__":
    main()