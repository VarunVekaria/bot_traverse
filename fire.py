import random
from neighbors import get_neighbor_cells

def spread_fire(matrix, fire_cells, q): #contains the logic behind the spread of fire.
    new_fire_cells = set()
    for r, c in fire_cells:
        neighbors = get_neighbor_cells(matrix, r, c)
        for nr, nc in neighbors:
            if matrix[nr][nc] == 0 and (nr, nc) not in fire_cells:
                K = sum((n_r, n_c) in fire_cells for n_r, n_c in get_neighbor_cells(matrix, nr, nc))
                probability = 1 - (1 - q) ** K
                if random.random() < probability:
                    new_fire_cells.add((nr, nc))
    return fire_cells.union(new_fire_cells)