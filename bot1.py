from collections import deque
from neighbors import get_neighbor_cells

#Shortest path computed using Breadth-First Search (BFS).
#The bot traverses only through this path. Avoiding the initial fire cell.
def bfs_bot1_traversal(matrix, bot_initial_position, button_position, fire_cells): 
    queue = deque([bot_initial_position])
    visited_cells = set([bot_initial_position]) #Storing visited cells
    parent_cell = {bot_initial_position: None} #Bots initial position has no parent thus assigned none.
    initial_fire_cell=fire_cells #Storing the initial cell that is on fire.

    while queue:
        curr_position = queue.popleft()

        if curr_position == button_position:
            path = []
            while curr_position is not None:
                path.append(curr_position) #Keeping track of the path bot traversed through.
                curr_position = parent_cell[curr_position]
            path.reverse()
            print(path)

            return path #Return path
        

        for adjacent_neighbour in get_neighbor_cells(matrix, curr_position[0], curr_position[1]):
            #Checking if neighbour cell is open
            #Checking if neighbour is not in visited and neighbour is not the initial fire cell.
            if matrix[adjacent_neighbour[0]][adjacent_neighbour[1]] == 0 and adjacent_neighbour not in visited_cells and adjacent_neighbour not in initial_fire_cell:
                queue.append(adjacent_neighbour)
                visited_cells.add(adjacent_neighbour)
                parent_cell[adjacent_neighbour] = curr_position
    
    return []
