from collections import deque
from neighbors import get_neighbor_cells

#Shortest path computed using BFS. The bot traverses only through this path.
def bfs_bot1_traversal(matrix, bot_initial_position, button_position, fire_cells): 
    queue = deque([bot_initial_position])
    visited_cells = set([bot_initial_position])
    parent_cell = {bot_initial_position: None}
    initial_fire_cell=fire_cells #Storing the initial cell that is on fire.

    while queue:
        current_position = queue.popleft()

        if current_position == button_position:
            path = []
            while current_position is not None:
                path.append(current_position)
                current_position = parent_cell[current_position]
            path.reverse()
            print(path)
            return path

        for neighbor in get_neighbor_cells(matrix, current_position[0], current_position[1]):
            if matrix[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited_cells and neighbor not in initial_fire_cell:
                print(initial_fire_cell)
                queue.append(neighbor)
                visited_cells.add(neighbor)
                parent_cell[neighbor] = current_position
    
    return []
