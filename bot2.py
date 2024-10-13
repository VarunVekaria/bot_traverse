from collections import deque
from neighbors import get_neighbor_cells

#Shortest path computed using Breadth-First Search (BFS).
#At each time-step it recalculates the route in order to avoid fire cells. 
def bfs_bot(matrix, bot_initial_position, button_position, fire_cells):
    queue = deque([bot_initial_position])
    visited_cells = set([bot_initial_position]) #Storing visited cells
    parent_cell = {bot_initial_position: None}  #Bots initial position has no parent thus assigned none.
    while queue:
        curr_position = queue.popleft()

        if curr_position == button_position:
            path = []
            while curr_position is not None:
                path.append(curr_position) #Keeping track of the path bot traversed through.
                curr_position = parent_cell[curr_position]
            path.reverse()
            return path  #Return path

        for adjacent_neighbour in get_neighbor_cells(matrix, curr_position[0], curr_position[1]):
            
            #Checking if neighbour cell is valid.
            #Checking if its open, not in visited and not currently a fire cell.
            if matrix[adjacent_neighbour[0]][adjacent_neighbour[1]] == 0 and adjacent_neighbour not in visited_cells and adjacent_neighbour not in fire_cells:
                if adjacent_neighbour in fire_cells:
                    continue
                queue.append(adjacent_neighbour)
                visited_cells.add(adjacent_neighbour)
                parent_cell[adjacent_neighbour] = curr_position

    return []  # No path found

def move_bot_bfs2(matrix, bot_initial_position, button_position, fire_cells):
    # Try to avoid the initial fire cell and current fire cells.
    path = bfs_bot(matrix, bot_initial_position, button_position, fire_cells)
    if not path:
        print(f"No valid path is found, bot remains at {bot_initial_position}")
        return bot_initial_position, False, []  # No valid path was found so the bot stays in place
    
    # print(f"New path re-planned: {path}")  # Tries to look for a new path
    return path[1], path[1] == button_position, path  # Move to the next step in the path


