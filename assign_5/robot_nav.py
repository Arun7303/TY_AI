import heapq
import math
from collections import defaultdict

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) coordinates
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic estimate to goal
        self.f = 0  # Total cost (g + h)
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __hash__(self):
        return hash(self.position)

class RobotNavigation:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
    
    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0
    
    def get_neighbors(self, node):
        neighbors = []
        x, y = node.position
        
        # Possible movements (4-directional or 8-directional)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 4-directional
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position((new_x, new_y)):
                neighbors.append(Node((new_x, new_y), node))
        
        return neighbors
    
    def heuristic(self, a, b):
        # Euclidean distance
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def a_star_search(self, start, goal):
        open_set = []
        closed_set = set()
        start_node = Node(start)
        goal_node = Node(goal)
        
        heapq.heappush(open_set, start_node)
        
        while open_set:
            current_node = heapq.heappop(open_set)
            
            if current_node == goal_node:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]  # Return reversed path
            
            closed_set.add(current_node)
            
            for neighbor in self.get_neighbors(current_node):
                if neighbor in closed_set:
                    continue
                
                # Cost from start to neighbor through current
                tentative_g = current_node.g + 1  # Assuming uniform cost
                
                if neighbor not in open_set or tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor.position, goal_node.position)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
        
        return None  # No path found

def create_grid(rows, cols, obstacles):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for (x, y) in obstacles:
        if 0 <= x < rows and 0 <= y < cols:
            grid[x][y] = 1  # 1 represents obstacle
    return grid

def print_grid(grid, path=None):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if path and (i, j) in path:
                print("P", end=" ")  # Path
            elif grid[i][j] == 1:
                print("#", end=" ")  # Obstacle
            else:
                print(".", end=" ")  # Free space
        print()

def main():
    print("Robot Navigation Problem using A* Algorithm")
    print("-------------------------------------------")
    
    # Grid configuration
    rows = 10
    cols = 10
    obstacles = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (4, 5), (5, 5), (6, 5), (7, 5)]
    
    grid = create_grid(rows, cols, obstacles)
    
    print("\nGrid Layout ('.' = free, '#' = obstacle):")
    print_grid(grid)
    
    # Get start and goal positions
    while True:
        try:
            start = tuple(map(int, input("\nEnter start position (row col): ").split()))
            goal = tuple(map(int, input("Enter goal position (row col): ").split()))
            
            if not (0 <= start[0] < rows and 0 <= start[1] < cols):
                print("Start position out of bounds!")
                continue
            if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
                print("Goal position out of bounds!")
                continue
            if grid[start[0]][start[1]] == 1:
                print("Start position is an obstacle!")
                continue
            if grid[goal[0]][goal[1]] == 1:
                print("Goal position is an obstacle!")
                continue
            break
        except ValueError:
            print("Please enter two numbers separated by space!")
    
    # Solve the problem
    solver = RobotNavigation(grid)
    path = solver.a_star_search(start, goal)
    
    # Display results
    if path:
        print("\nPath found ({} steps):".format(len(path)-1))
        print(" -> ".join([str(pos) for pos in path]))
        
        print("\nVisualization (P = path):")
        print_grid(grid, path)
    else:
        print("\nNo path exists to the goal!")

if __name__ == "__main__":
    main()