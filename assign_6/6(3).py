import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Map Coloring using Backtracking
def is_valid(node, color, assignment, graph):
    for neighbor in graph[node]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack(graph, colors, assignment, nodes, idx):
    if idx == len(nodes):
        return assignment

    node = nodes[idx]
    for color in colors:
        if is_valid(node, color, assignment, graph):
            assignment[node] = color
            result = backtrack(graph, colors, assignment, nodes, idx + 1)
            if result:
                return result
            del assignment[node]

    return None

def solve_map_coloring(graph, colors):
    nodes = list(graph.keys())
    assignment = {}
    return backtrack(graph, colors, assignment, nodes, 0)

# GUI Output for Visualizing the Map Coloring Solution
def show_gui(graph, color_assignment):
    root = tk.Tk()
    root.title("Map Coloring")

    fig, ax = plt.subplots(figsize=(8, 8))
    G = nx.Graph()

    for node in graph:
        G.add_node(node)
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)
    node_colors = [color_assignment.get(node, "gray") for node in G.nodes]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_weight='bold', ax=ax, font_size=12)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

    root.mainloop()

# Terminal Input + Launch GUI
def main():
    print("=== Map Coloring Problem ===")
    num_regions = int(input("Enter number of regions: "))

    graph = {}
    for _ in range(num_regions):
        region = input("Region name: ").strip()
        neighbors = input(f"Enter neighbors of {region} (comma-separated): ").strip().split(',')
        graph[region] = [n.strip() for n in neighbors if n.strip()]

    colors_input = input("Enter available colors (comma-separated): ").strip().split(',')
    colors = [c.strip().capitalize() for c in colors_input if c.strip()]

    result = solve_map_coloring(graph, colors)

    if result:
        print("\nColor assignment:")
        for region in result:
            print(f"{region}: {result[region]}")
        show_gui(graph, result)
    else:
        print("No valid coloring possible with the given colors!")

if __name__ == "__main__":
    main()
