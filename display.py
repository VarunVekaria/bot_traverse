import pygame

def display_alert(screen, message, width, height): #to display any alerts i.e if bot is on fire on button is on fire or if the bot finds the button.

    font = pygame.font.Font(None, 32)
    text = font.render(message, True, (0, 0, 0)) 
    text_rect = text.get_rect(center=(width // 2, height // 2))
    box_width, box_height = text_rect.width + 20, text_rect.height + 20
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (width // 2, height // 2)
    pygame.draw.rect(screen, (50, 50, 50), box_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(4000)