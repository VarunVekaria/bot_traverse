import random

def generate_blocked_cells(size): 
    """Creates a matrix filled with blocked cells (1)."""
    return [[1 for _ in range(size)] for _ in range(size)]


def get_neighbor_cells(matrix, row, col): 
    """Returns a list of valid neighbors for a given cell."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]):
            neighbors.append((nr, nc))
    return neighbors


def open_cells(matrix):
    """Opens cells in the matrix according to the specified rules."""
    # Step 1: Open a random interior cell
    row, col = random.randint(1, len(matrix) - 2), random.randint(1, len(matrix[0]) - 2)
    matrix[row][col] = 0  # 0 represents open

    # Iteratively open cells
    while True:
        valid_cells = []
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 1 and len([n for n in get_neighbor_cells(matrix, r, c) if matrix[n[0]][n[1]] == 0]) == 1:
                    valid_cells.append((r, c))

        if not valid_cells:
            break

        r, c = random.choice(valid_cells)
        matrix[r][c] = 0

    return matrix


def identify_dead_ends(matrix):
    """Identifies and returns dead end cells."""
    dead_ends = []
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == 0 and len([n for n in get_neighbor_cells(matrix, r, c) if matrix[n[0]][n[1]] == 0]) == 1:
                dead_ends.append((r, c))
    return dead_ends


def open_closed_neighbors(matrix, dead_ends):
    """Opens a random closed neighbor of dead end cells."""
    for _ in range(len(dead_ends) // 2):  # Approximately half of the dead ends
        dead_end = random.choice(dead_ends)
        neighbors = get_neighbor_cells(matrix, dead_end[0], dead_end[1])
        closed_neighbors = [(r, c) for r, c in neighbors if matrix[r][c] == 1]
        
        if closed_neighbors:
            neighbor_to_open = random.choice(closed_neighbors)
            matrix[neighbor_to_open[0]][neighbor_to_open[1]] = 0  # Open the selected closed neighbor


def initialize_button_position(matrix, bot_initial_position): 
    """Places the button at a random open location in the matrix."""
    open_cells = [(r, c) for r in range(len(matrix)) for c in range(len(matrix[0])) if matrix[r][c] == 0 and (r, c) != bot_initial_position]
    button_position = random.choice(open_cells)
    return button_position


def initialize_bot_initial_position(matrix): 
    """Places the bot at a random open location in the matrix."""
    open_cells = [(r, c) for r in range(len(matrix)) for c in range(len(matrix[0])) if matrix[r][c] == 0]
    bot_initial_position = random.choice(open_cells)
    return bot_initial_position


def initialize_fire_location(matrix, bot_initial_position, button_position): 
    """Starts the fire at a random cell on the grid."""
    open_cells = [(r, c) for r in range(len(matrix)) for c in range(len(matrix[0])) if matrix[r][c] == 0 and (r, c) != bot_initial_position and (r, c) != button_position]
    fire_location = random.choice(open_cells)
    return {fire_location}


def create_ship_layout(size, q): 
    """Creates the initial environment."""
    matrix = generate_blocked_cells(size)
    open_cells(matrix)
    dead_ends = identify_dead_ends(matrix)
    open_closed_neighbors(matrix, dead_ends)
    bot_initial_position = initialize_bot_initial_position(matrix)
    button_position = initialize_button_position(matrix, bot_initial_position)
    fire_cells = initialize_fire_location(matrix, bot_initial_position, button_position)
    return matrix, bot_initial_position, button_position, fire_cells
