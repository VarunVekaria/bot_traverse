def get_neighbors(matrix, row, col): #for a given cell it is able to get its neighbors
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in dir:
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]):
            neighbors.append((nr, nc))
    return neighbors