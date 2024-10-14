import heapq
from neighbors import get_neighbor_cells
# Here, we use Manhattan distance to aid in selection of the path from multiple paths
# The shortest distance from the cells of distinct path to the fire cell is stored. Let it be named A 
# The path which has maximum A value is selected, which basically helps to avoid fire.
# Function to calculate the Manhattan distance 
# Manhattan distance = |x1 - x2| + |y1 - y2|
def manhattan_distance(path_cell, fire_cell):
    return abs(path_cell[0] - fire_cell[0]) + abs(path_cell[1] - fire_cell[1])

# Find the closest Manhattan distance from the path to any fire cell.
def closest_distance_to_fire(path, fire_cells):
    # Calculates the minimum distance between cells in the path and fire cells.
    return min(manhattan_distance(cell, fire) for cell in path for fire in fire_cells)

# Function to select the best possible path.
def choose_best_path(possible_paths, fire_cells):
    final_path = None # Stores the final path chosen.
    max_min_distance = -1

    for path in possible_paths:
        min_distance_to_fire = closest_distance_to_fire(path, fire_cells)
        if min_distance_to_fire > max_min_distance:
            max_min_distance = min_distance_to_fire
            final_path = path

    return final_path # Returns the best path considering safety of the bot.

# Using Dijkstra's algorithm to compute multiple paths
def dijkstra(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=True):
    queue = []
    heapq.heappush(queue, (0, bot_initial_position, [bot_initial_position]))  # (distance, current_position, path)
    visited_cells = {bot_initial_position: 0}  # To track visited_cells nodes and their shortest distance
    possible_paths = []  # To store all paths

    while queue:
        current_position_dist, current_position_pos, path = heapq.heappop(queue)
        for adjacent_neighbour in get_neighbor_cells(matrix, current_position_pos[0], current_position_pos[1]):
            if matrix[adjacent_neighbour[0]][adjacent_neighbour[1]] == 0:
                # Avoid fire cells and adjacent fire cells if possible
                if avoid_adjacent_fire:
                    fire_adjacent = any(n in fire_cells for n in get_neighbor_cells(matrix, adjacent_neighbour[0], adjacent_neighbour[1]))
                    if adjacent_neighbour in fire_cells or fire_adjacent:
                        continue

                new_dist = current_position_dist + 1  
                
                # If the adjacent_neighbour is the button location, store the path
                if adjacent_neighbour == button_position:
                    possible_paths.append(path + [adjacent_neighbour])
                    # Continue to search for more paths
            
                if adjacent_neighbour not in visited_cells or new_dist < visited_cells[adjacent_neighbour]:
                    visited_cells[adjacent_neighbour] = new_dist
                    heapq.heappush(queue, (new_dist, adjacent_neighbour, path + [adjacent_neighbour]))

    return possible_paths

# Move the bot by selecting one of the multiple paths generated by Dijkstra's algorithm
def move_bot_dijkstra(matrix, bot_initial_position, button_position, fire_cells):
   # Avoid fire cells and adjacent fire cells only if possible
    possible_paths = dijkstra(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=True)

    if not possible_paths:
        # If no safe path avoiding adjacent fire cells, avoid only fire cells.
        possible_paths = dijkstra(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=False)

    if not possible_paths:
        print(f"No valid path is found, bot remains at {bot_initial_position}")
        return bot_initial_position, False, []  # No valid path, bot stays in place

    print(f"All possible paths found: {possible_paths}")  
    # Select the best path based on distance to fire cells
    final_path = choose_best_path(possible_paths, fire_cells)
    return final_path[1], final_path[1] == button_position, final_path  # Move to the next step in the best path computed

