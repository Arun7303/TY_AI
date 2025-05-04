import heapq
import math

class CityNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic estimate to goal
        self.f = 0  # Total cost (g + h)
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __lt__(self, other):
        return self.f < other.f

def haversine_distance(city1, city2, city_coords):
    """Calculate distance between two cities using Haversine formula"""
    lat1, lon1 = city_coords[city1]
    lat2, lon2 = city_coords[city2]
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Earth radius in km
    return c * r

def a_star(start, goal, city_coords, city_connections):
    open_set = []
    closed_set = set()
    
    start_node = CityNode(start)
    goal_node = CityNode(goal)
    
    heapq.heappush(open_set, start_node)
    
    while open_set:
        current_node = heapq.heappop(open_set)
        
        if current_node == goal_node:
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path
        
        closed_set.add(current_node.name)
        
        for neighbor in city_connections[current_node.name]:
            if neighbor in closed_set:
                continue
            
            neighbor_node = CityNode(neighbor, current_node)
            
            # Calculate distance between current city and neighbor
            distance = haversine_distance(current_node.name, neighbor, city_coords)
            neighbor_node.g = current_node.g + distance
            
            # Heuristic: straight-line distance to goal
            neighbor_node.h = haversine_distance(neighbor, goal, city_coords)
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            
            # Check if neighbor is already in open set with higher cost
            found = False
            for node in open_set:
                if node == neighbor_node and node.f <= neighbor_node.f:
                    found = True
                    break
            
            if not found:
                heapq.heappush(open_set, neighbor_node)
    
    return None  # No path found

def get_city_coordinates():
    """Get city coordinates from user"""
    city_coords = {}
    print("Enter city coordinates (latitude and longitude)")
    print("Type 'done' when finished")
    
    while True:
        city = input("City name: ").strip()
        if city.lower() == 'done':
            break
        try:
            lat = float(input(f"Latitude for {city}: "))
            lon = float(input(f"Longitude for {city}: "))
            city_coords[city] = (lat, lon)
        except ValueError:
            print("Please enter valid numbers for coordinates")
    
    return city_coords

def get_city_connections(cities):
    """Get road connections between cities from user"""
    connections = {city: [] for city in cities}
    print("\nEnter city connections (roads between cities)")
    print("Type 'done' when finished")
    
    while True:
        connection = input("Enter connection (city1-city2): ").strip()
        if connection.lower() == 'done':
            break
        if '-' not in connection:
            print("Please use format 'city1-city2'")
            continue
        
        city1, city2 = connection.split('-')[:2]
        city1 = city1.strip()
        city2 = city2.strip()
        
        if city1 not in cities or city2 not in cities:
            print("One or both cities not found in coordinates")
            continue
        
        connections[city1].append(city2)
        connections[city2].append(city1)  # Assuming bidirectional roads
    
    return connections

def main():
    print("City Path Finder using A* Algorithm")
    print("-----------------------------------")
    
    # Get city data from user
    city_coords = get_city_coordinates()
    if not city_coords:
        print("No cities entered. Exiting.")
        return
    
    city_connections = get_city_connections(city_coords.keys())
    
    # Get start and goal cities
    while True:
        start = input("\nEnter starting city: ").strip()
        goal = input("Enter destination city: ").strip()
        
        if start not in city_coords or goal not in city_coords:
            print("One or both cities not found. Try again.")
        else:
            break
    
    # Find path
    path = a_star(start, goal, city_coords, city_connections)
    
    # Display results
    if path:
        print(f"\nShortest path from {start} to {goal}:")
        print(" -> ".join(path))
        
        # Calculate total distance
        total_distance = 0
        for i in range(len(path)-1):
            total_distance += haversine_distance(path[i], path[i+1], city_coords)
        print(f"Total distance: {total_distance:.2f} km")
    else:
        print("\nNo path exists between these cities!")

if __name__ == "__main__":
    main()