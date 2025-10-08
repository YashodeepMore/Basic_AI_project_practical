import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------
# Graph setup with more cities
# -------------------------------
graph = {
    'A': {'B': 6, 'F': 3},
    'B': {'A': 6, 'C': 3, 'D': 2},
    'C': {'B': 3, 'D': 1, 'E': 5},
    'D': {'B': 2, 'C': 1, 'E': 8, 'H': 4},
    'E': {'C': 5, 'D': 8, 'G': 5, 'I': 7},
    'F': {'A': 3, 'G': 7, 'J': 4},
    'G': {'E': 5, 'F': 7, 'I': 3},
    'H': {'D': 4, 'I': 4},
    'I': {'E': 7, 'G': 3, 'H': 4, 'J': 6},
    'J': {'F': 4, 'I': 6}
}

# Coordinates for visualization (city positions)
coords = {
    'A': (0, 0),
    'B': (2, 3),
    'C': (4, 4),
    'D': (6, 2),
    'E': (8, 3),
    'F': (1, -2),
    'G': (10, 0),
    'H': (7, 5),
    'I': (10, 4),
    'J': (3, -3)
}

# -------------------------------
# Heuristic Function
# -------------------------------
def heuristic(a, b):
    """Euclidean distance heuristic"""
    (x1, y1), (x2, y2) = coords[a], coords[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# -------------------------------
# Best-First Search
# -------------------------------
def best_first_search(start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start))
    came_from = {start: None}
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            break
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_list, (heuristic(neighbor, goal), neighbor))
    return came_from

# -------------------------------
# A* Search
# -------------------------------
def a_star(start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_list:
        _, cost, current = heapq.heappop(open_list)
        if current == goal:
            break
        for neighbor, weight in graph[current].items():
            new_cost = g_score[current] + weight
            if neighbor not in g_score or new_cost < g_score[neighbor]:
                g_score[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (priority, new_cost, neighbor))
                came_from[neighbor] = current
    return came_from, g_score.get(goal, float('inf'))

# -------------------------------
# Path Reconstruction
# -------------------------------
def reconstruct(came_from, start, goal):
    node = goal
    path = []
    while node:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path

# -------------------------------
# Interactive Selection Function
# -------------------------------
def select_city(event):
    global clicks, selected
    for city, (x, y) in coords.items():
        if abs(event.xdata - x) < 0.5 and abs(event.ydata - y) < 0.5:
            selected.append(city)
            print(f"Selected: {city}")
            clicks += 1
            if clicks == 2:
                plt.close()
            break

# -------------------------------
# Visualization Function
# -------------------------------
def visualize(graph, path1, path2):
    G = nx.Graph()
    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = coords
    plt.figure(figsize=(10, 7))

    # Draw base map
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=800, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})

    # Draw paths
    if path1:
        nx.draw_networkx_edges(G, pos, edgelist=[(path1[i], path1[i+1]) for i in range(len(path1)-1)],
                               edge_color='blue', width=3, label="Best-First Search Path")
    if path2:
        nx.draw_networkx_edges(G, pos, edgelist=[(path2[i], path2[i+1]) for i in range(len(path2)-1)],
                               edge_color='green', width=3, label="A* Search Path")

    plt.legend()
    plt.title("Interactive City Route Finder (Click to Select Start & Goal)")
    plt.show()

# -------------------------------
# MAIN PROGRAM
# -------------------------------
selected = []
clicks = 0

# Show map for user to select start and goal
plt.figure(figsize=(10, 7))
G = nx.Graph()
for node, edges in graph.items():
    for neighbor, weight in edges.items():
        G.add_edge(node, neighbor, weight=weight)

pos = coords
nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=800, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
plt.title("Click to Select Start and Goal City (2 clicks)")
plt.gcf().canvas.mpl_connect('button_press_event', select_city)
plt.show()

# After selection
if len(selected) == 2:
    start, goal = selected
    print(f"\nStart: {start}, Goal: {goal}")

    # Run algorithms
    bfs_came = best_first_search(start, goal)
    astar_came, astar_cost = a_star(start, goal)

    bfs_path = reconstruct(bfs_came, start, goal)
    astar_path = reconstruct(astar_came, start, goal)

    print("\n🔹 Best-First Search Path:", " → ".join(bfs_path))
    print("🔹 A* Search Path:", " → ".join(astar_path))
    print(f"✅ Total Cost (A*): {astar_cost}")

    # Show final paths
    visualize(graph, bfs_path, astar_path)
else:
    print("You must select two cities (Start & Goal).")
