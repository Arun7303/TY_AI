def water_jug_dfs(x, y, target):
    print("\nSolving using Depth First Search (DFS)...")
    print("Rules:")
    print("1. You can fill either Jug 1 or Jug 2 to full capacity.")
    print("2. You can empty either Jug completely.")
    print("3. You can pour water from one Jug to another until it is full or the first Jug is empty.")
    print("-" * 50)

    stack = [(0, 0)]
    visited = set()
    path = []

    while stack:
        a, b = stack.pop()

        if (a, b) in visited:
            continue

        path.append((a, b))
        visited.add((a, b))

        if a == target or b == target:
            return path

        # Possible moves
        next_states = [
            (x, b), (a, y),  # Fill jugs
            (0, b), (a, 0),  # Empty jugs
            (a - min(a, y - b), b + min(a, y - b)),  # Pour Jug 1 -> Jug 2
            (a + min(b, x - a), b - min(b, x - a))   # Pour Jug 2 -> Jug 1
        ]

        for state in next_states:
            if state not in visited:
                stack.append(state)

    return "No solution"

# Taking input from user
x = int(input("Enter capacity of Jug 1: "))
y = int(input("Enter capacity of Jug 2: "))
target = int(input("Enter target amount: "))

print("DFS Solution:", water_jug_dfs(x, y, target))
