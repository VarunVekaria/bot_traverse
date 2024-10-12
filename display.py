import pygame

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
