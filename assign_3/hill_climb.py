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
    while True:
        neighbors = get_possible_moves(current)
        
        best_move = None
        best_score = manhattan_distance(current, goal)
        
        for neighbor in neighbors:
            score = manhattan_distance(neighbor, goal)
            if score < best_score:
                best_score = score
                best_move = neighbor
        
        if best_move is None:  # No better move found
            break
        
        current = best_move
    
    return current

def is_goal(state, goal):
    return np.array_equal(state, goal)

if __name__ == "__main__":
    initial_state = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    print("Initial State:")
    print(initial_state)
    
    final_state = hill_climbing(initial_state, goal_state)
    
    print("Final State:")
    print(final_state)
    
    if is_goal(final_state, goal_state):
        print("Solution Found!")
    else:
        print("Local Maximum Reached. No Solution.")
