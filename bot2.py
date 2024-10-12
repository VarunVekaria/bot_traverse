import pygame
import random
from collections import deque
from constants import CELL_SIZE, GRID_MARGIN, BLACK, WHITE, RED, BLUE, GREEN
from neighbors import get_neighbors

# Breadth-First Search (BFS) to compute shortest path, avoiding fire and adjacent fire cells
def bfs_bot(matrix, bot_location, button_location, fire_cells):
    queue = deque([bot_location])
    visited = set([bot_location])
    parent = {bot_location: None}
    while queue:
        current = queue.popleft()

        if current == button_location:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(matrix, current[0], current[1]):
            if matrix[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited and neighbor not in fire_cells:
                if neighbor in fire_cells:
                    continue
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return []  # No path found

def move_bot_bfs2(matrix, bot_location, button_location, fire_cells):
    # Try to avoid fire cells and adjacent fire cells first
    path = bfs_bot(matrix, bot_location, button_location, fire_cells)
    if not path:
        print(f"No valid path at step, bot remains at {bot_location}")
        return bot_location, False, []  # No valid path, bot stays in place
    
    print(f"New path re-planned: {path}")  # Log the new path
    return path[1], path[1] == button_location, path  # Move to the next step in the path


