import pygame
import random
from collections import deque
from constants import CELL_SIZE, GRID_MARGIN, BLACK, WHITE, RED, BLUE, GREEN
from neighbors import get_neighbor_cells

# Breadth-First Search (BFS) to compute shortest path, avoiding fire and adjacent fire cells
def bfs_bot(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=True):
    queue = deque([bot_initial_position])
    visited_cells = set([bot_initial_position])
    parent_cell = {bot_initial_position: None}
   # truly_visited_cells = set([bot_initial_position])
    while queue:
        current_position = queue.popleft()

        if current_position == button_position:
            path = []
            while current_position is not None:
                path.append(current_position)
                current_position = parent_cell[current_position]
            path.reverse()
            return path

        for neighbor in get_neighbor_cells(matrix, current_position[0], current_position[1]):
            if matrix[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited_cells:
                # Avoid fire cells and adjacent fire cells if possible
                if avoid_adjacent_fire:
                    fire_adjacent = any(n in fire_cells for n in get_neighbor_cells(matrix, neighbor[0], neighbor[1]))
                    if neighbor in fire_cells or fire_adjacent:
                        continue
                else:
                    if neighbor in fire_cells:
                        continue
                queue.append(neighbor)
                visited_cells.add(neighbor)
                parent_cell[neighbor] = current_position

    return []  # No path found

# Move the bot every time step and re-plan path based on the fire
def move_bot_bonus(matrix, bot_initial_position, button_position, fire_cells):
    # Try to avoid fire cells and adjacent fire cells first
    path = bfs_bot(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=True)
    
    if not path:
        # If no safe path avoiding adjacent fire cells, avoid only fire cells
        path = bfs_bot(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=False)

    if not path:
        print(f"No valid path at step, bot remains at {bot_initial_position}")
        return bot_initial_position, False, []  # No valid path, bot stays in place
    
    print(f"New path re-planned: {path}")  # Log the new path
    return path[1], path[1] == button_position, path  # Move to the next step in the path
