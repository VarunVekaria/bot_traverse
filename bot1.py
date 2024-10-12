from collections import deque
from neighbors import get_neighbors

def bfs_bot1(matrix, bot_location, button_location, fire_cells): #uses BFS to compute the shortest path. The bot traverses only through that path.
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
            print(path)
            return path

        for neighbor in get_neighbors(matrix, current[0], current[1]):
            if matrix[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited and neighbor not in fire_cells:
                print(fire_cells)
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

        

    return []
