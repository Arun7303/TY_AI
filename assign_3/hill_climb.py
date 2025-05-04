import random
import numpy as np

def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = np.where(goal == state[i][j])
                distance += abs(i - x[0]) + abs(j - y[0])
    return distance

def get_possible_moves(state):
    moves = []
    zero_x, zero_y = np.where(state == 0)
    zero_x, zero_y = zero_x[0], zero_y[0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        new_x, new_y = zero_x + dx, zero_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = state.copy()
            new_state[zero_x, zero_y], new_state[new_x, new_y] = new_state[new_x, new_y], new_state[zero_x, zero_y]
            moves.append(new_state)
    
    return moves

def hill_climbing(initial, goal):
    current = initial.copy()
    step = 0
    
    while True:
        print(f"Step {step}:")
        print(current)
        heuristic = manhattan_distance(current, goal)
        print(f"Heuristic: {heuristic}\n")
        
        neighbors = get_possible_moves(current)
        
        best_move = None
        best_score = heuristic
        
        for neighbor in neighbors:
            score = manhattan_distance(neighbor, goal)
            if score < best_score:
                best_score = score
                best_move = neighbor
        
        if best_move is None:  # No better move found
            break
        
        current = best_move
        step += 1
    
    return current

def is_goal(state, goal):
    return np.array_equal(state, goal)

def get_user_input(prompt):
    print(prompt)
    state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        state.append(row)
    return np.array(state)

if __name__ == "__main__":
    initial_state = get_user_input("Enter initial state (3x3 grid, space-separated rows):")
    goal_state = get_user_input("Enter goal state (3x3 grid, space-separated rows):")
    
    print("Initial State:")
    print(initial_state)
    
    final_state = hill_climbing(initial_state, goal_state)
    
    print("Final State:")
    print(final_state)
    
    if is_goal(final_state, goal_state):
        print("Solution Found!")
    else:
        print("Local Maximum Reached. No Solution.")
