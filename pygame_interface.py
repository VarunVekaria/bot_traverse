import pygame
import random
from environment import create_environment
from bot1 import bfs_bot1  # Assuming bfs_bot is defined in another file
from fire import spread_fire  # Assuming fire simulation is in another file
from constants import CELL_SIZE, GRID_MARGIN, BLACK, WHITE, RED, BLUE, GREEN
from bot2 import move_bot_bfs2
from bot3 import move_bot_bfs3
from bot4 import move_bot_dijkstra_multiple

def display_alert(screen, message, width, height):
    """Displays an alert message in the middle of the screen."""
    font = pygame.font.Font(None, 30)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def run_pygame_gui(size, q, bot_called):
    """Sets up and runs the Pygame interface."""
    pygame.init()

    # Set up the display for the grid
    width = size * (CELL_SIZE + GRID_MARGIN)
    height = size * (CELL_SIZE + GRID_MARGIN)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bot vs Fire Simulation")
  
    # Create environment, i.e., bot, button, and fire locations
    matrix, bot_location, button_location, fire_cells = create_environment(size, q)
    clock = pygame.time.Clock()
    running = True
    button_pressed = False

    # For tracking bot path
    path = []

    if(bot_called == 1):
        path = bfs_bot1(matrix, bot_location, button_location, fire_cells)

        if path:
            print(f"Shortest path from Bot to Button is: {path}")
        else:
            print("No valid path! Bot trapped!")
            return  # Exit if no path exists

    # Track bot's movement step-by-step
    current_step = 0

    while running and not button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spread fire
        fire_cells = spread_fire(matrix, fire_cells, q)

        # Move the bot along the path
        if bot_called == 2:
            bot_location, button_pressed, path = move_bot_bfs2(matrix, bot_location, button_location, fire_cells)
        if bot_called == 3:
            bot_location, button_pressed, path = move_bot_bfs3(matrix, bot_location, button_location, fire_cells)   
        if bot_called == 4:
            bot_location, button_pressed = move_bot_dijkstra_multiple(matrix, bot_location, button_location, fire_cells)
        
        if path and bot_called == 1:
            bot_location = path[current_step]
            current_step = min(current_step + 1, len(path) - 1)

        # Check if bot has stepped into fire
        if bot_location in fire_cells:
            display_alert(screen, "The Bot is on fire! Game Over!", width, height)
            running = False
            break

        # Check if the button is pressed and not on fire
        if bot_location == button_location:
            if button_location in fire_cells:
                display_alert(screen, "The Button is on fire! Game Over!", width, height)
                running = False
                break
            else:
                button_pressed = True
                display_alert(screen, "Game successful! Bot suppressed fire!", width, height)

        # Draw the grid
        screen.fill(BLACK)
        for r in range(size):
            for c in range(size):
                color = BLACK if matrix[r][c] == 1 else WHITE
                if (r, c) == bot_location:
                    color = BLUE
                elif (r, c) == button_location:
                    color = GREEN
                elif (r, c) in fire_cells:
                    color = RED

                pygame.draw.rect(
                    screen, 
                    color, 
                    [(GRID_MARGIN + CELL_SIZE) * c + GRID_MARGIN, (GRID_MARGIN + CELL_SIZE) * r + GRID_MARGIN, CELL_SIZE, CELL_SIZE]
                )

        pygame.display.flip()

        # Speed of simulation
        clock.tick(4)

    pygame.quit()
