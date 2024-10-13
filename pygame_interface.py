import pygame
import random
from environment import create_ship_layout
from bot1 import bfs_bot1_traversal  
from fire import spread_fire  
from constants import CELL_SIZE, GRID_MARGIN, BLACK, WHITE, SCARLET_RED, BLUE, GREEN
from bot2 import move_bot_bfs2
from bot3 import move_bot_bfs3
from bot4 import move_bot_dijkstra
from bonus import move_bot_bonus

#This functions displays alert message, depict game status.
def display_alert(screen, message, width, height):
    font = pygame.font.Font(None, 32) #Set font for the alert text
    text = font.render(message, True, (255, 255, 255)) 
    text_rect = text.get_rect(center=(width // 2, height // 2))
    box_width, box_height = text_rect.width + 20, text_rect.height + 20 #Defining alert box dimensions.
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (width // 2, height // 2) #Position the box at center
    pygame.draw.rect(screen, (50, 50, 50), box_rect) #Draws the alert rectangle.
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000) #Pause the game for a second so that alert can be seen.


def run_pygame_gui(size, q, bot_called):
    """Sets up and runs the Pygame interface."""
    pygame.init()

    # Set up the display for the main grid
    width = size * (CELL_SIZE + GRID_MARGIN)
    height = size * (CELL_SIZE + GRID_MARGIN)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bot vs Fire Simulation")
  
    # Create ship environment, i.e., bot, button, and fire locations
    matrix, bot_initial_position, button_position, fire_cells = create_ship_layout(size, q)
    clock = pygame.time.Clock()
    running = True
    button_pressed = False

    # For tracking the path bot takes
    path = []

    if(bot_called == 1):
        path = bfs_bot1_traversal(matrix, bot_initial_position, button_position, fire_cells)

        if path:
            print(f"Shortest path from Bot to Button is: {path}")
        else:
            print("No valid path! Bot trapped!")
            return  
        
    # Track bot's movement step-by-step
    current_position_step = 0

    while running and not button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spread fire
        fire_cells = spread_fire(matrix, fire_cells, q)

        # Move the bot along the path
        if bot_called == 2:
            bot_initial_position, button_pressed, path = move_bot_bfs2(matrix, bot_initial_position, button_position, fire_cells)
        if bot_called == 3:
            bot_initial_position, button_pressed, path = move_bot_bfs3(matrix, bot_initial_position, button_position, fire_cells)   
        if bot_called == 4:
            bot_initial_position, button_pressed, path = move_bot_dijkstra(matrix, bot_initial_position, button_position, fire_cells)
        if bot_called == 5:
            bot_initial_position, button_pressed, path = move_bot_bonus(matrix, bot_initial_position, button_position, fire_cells)
            # bot_initial_position = path[current_position_step]
            # current_position_step = min(current_position_step + 1, len(path) - 1)
            matrix[bot_initial_position[0]][bot_initial_position[1]] = 1
        if path and (bot_called == 1):
            bot_initial_position = path[current_position_step]
            current_position_step = min(current_position_step + 1, len(path) - 1)
            
                

        # Check if bot has stepped into fire
        if bot_initial_position in fire_cells:
            display_alert(screen, "The Bot is on fire! Game Over!!!", width, height)
            running = False
            break

        if button_position in fire_cells:
            display_alert(screen, "The Button is on fire! Game Over!", width, height)
            running = False
            break

        # Check if the button is pressed and not on fire
        if bot_initial_position == button_position:
            if button_position in fire_cells:
                display_alert(screen, "The Button is on fire! Game Over!!!", width, height)
                running = False
                break
            else:
                button_pressed = True
                display_alert(screen, "Game successful! Bot suppressed fire!!", width, height)

        #Grid drawing
        screen.fill(BLACK)
        for r in range(size):
            for c in range(size):
                color = BLACK if matrix[r][c] == 1 else WHITE
                if (r, c) == bot_initial_position:
                    color = BLUE
                elif (r, c) == button_position:
                    color = GREEN
                elif (r, c) in fire_cells:
                    color = SCARLET_RED

                pygame.draw.rect(
                    screen, 
                    color, 
                    [(GRID_MARGIN + CELL_SIZE) * c + GRID_MARGIN, (GRID_MARGIN + CELL_SIZE) * r + GRID_MARGIN, CELL_SIZE, CELL_SIZE]
                )

        pygame.display.flip()
        clock.tick(4) #setting speed of simulation

    pygame.quit()
