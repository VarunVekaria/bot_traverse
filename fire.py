import random
from neighbors import get_neighbor_cells

#Function contains logic behind spreading of the fire.
def spread_fire(matrix, fire_cells, q): 
    new_fire_cells = set()
    for r, c in fire_cells:
        neighbors = get_neighbor_cells(matrix, r, c)
        for nr, nc in neighbors:
            if matrix[nr][nc] == 0 and (nr, nc) not in fire_cells:
                K = sum((n_r, n_c) in fire_cells for n_r, n_c in get_neighbor_cells(matrix, nr, nc))
                probability = 1 - (1 - q) ** K #Probabilty function as stated in the problem statement.
                if random.random() < probability:
                    new_fire_cells.add((nr, nc)) #adding new cells that will be on fire.
    return fire_cells.union(new_fire_cells)