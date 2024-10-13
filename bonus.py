from collections import deque
from neighbors import get_neighbor_cells

# Breadth-First Search (BFS) to compute shortest path, avoiding fire and adjacent fire cells
def bfs_bot(matrix, bot_initial_position, button_position, fire_cells, avoid_adjacent_fire=True):
    queue = deque([bot_initial_position])
    visited_cells = set([bot_initial_position])
    parent_cell = {bot_initial_position: None}
   # truly_visited_cells = set([bot_initial_position])
    while queue:
        curr_position = queue.popleft()

        if curr_position == button_position:
            path = []
            while curr_position is not None:
                path.append(curr_position)
                curr_position = parent_cell[curr_position]
            path.reverse()
            return path

        for adjacent_neighbour in get_neighbor_cells(matrix, curr_position[0], curr_position[1]):
            if matrix[adjacent_neighbour[0]][adjacent_neighbour[1]] == 0 and adjacent_neighbour not in visited_cells:
                # Avoid fire cells and adjacent fire cells if possible
                if avoid_adjacent_fire:
                    fire_adjacent = any(n in fire_cells for n in get_neighbor_cells(matrix, adjacent_neighbour[0], adjacent_neighbour[1]))
                    if adjacent_neighbour in fire_cells or fire_adjacent:
                        continue
                else:
                    if adjacent_neighbour in fire_cells:
                        continue
                queue.append(adjacent_neighbour)
                visited_cells.add(adjacent_neighbour)
                parent_cell[adjacent_neighbour] = curr_position

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
