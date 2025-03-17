from collections import deque

def water_jug_bfs(cap_a, cap_b, target):
    queue = deque()
    visited = set()
    queue.append((0, 0))  # Initial state: both jugs empty
    parent = {}
    rule_applied = {}  # Track which rule was applied to reach each state
    parent[(0, 0)] = None
    rule_applied[(0, 0)] = None

    rules = [
        "1: Fill Jug A",
        "2: Fill Jug B",
        "3: Empty Jug A",
        "4: Empty Jug B",
        "5: Pour from Jug A to B",
        "6: Pour from Jug B to A"
    ]
    
    while queue:
        state = queue.popleft()
        a, b = state
        
        if state in visited:
            continue
        visited.add(state)
        
        print("\nCurrent state:")
        print(f"Jug A = {a}, Jug B = {b}")
        
        if a == target or b == target:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            path.reverse()
            
            print("\nSolution path:")
            for p in path:
                print(f"Jug A = {p[0]}, Jug B = {p[1]}")
            return
        
        # Generate next possible states and track rules
        next_states = [
            ((cap_a, b), rules[0]),  # Fill Jug A
            ((a, cap_b), rules[1]),  # Fill Jug B
            ((0, b), rules[2]),      # Empty Jug A
            ((a, 0), rules[3]),      # Empty Jug B
            ((a - min(a, cap_b - b), b + min(a, cap_b - b)), rules[4]),  # Pour A -> B
            ((a + min(b, cap_a - a), b - min(b, cap_a - a)), rules[5])   # Pour B -> A
        ]

        for new_state, rule in next_states:
            if new_state not in visited:
                print(f"Applying Rule: {rule}")
                queue.append(new_state)
                parent[new_state] = state
                rule_applied[new_state] = rule
    
    print("No solution found")

if __name__ == "__main__":
    cap_a = int(input("Enter capacity of Jug A: "))
    cap_b = int(input("Enter capacity of Jug B: "))
    target = int(input("Enter target amount of water: "))
    
    water_jug_bfs(cap_a, cap_b, target)
